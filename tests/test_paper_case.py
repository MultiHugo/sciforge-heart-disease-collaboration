import json
import html
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "paper" / "case-02-heart-disease"
BODY = CASE_DIR / "body.tex"
APPENDIX = CASE_DIR / "appendix.tex"


def prose_word_count(source: str) -> int:
    """Count English prose words while ignoring LaTeX control sequences."""
    source = re.sub(r"(?m)(?<!\\)%.*$", "", source)
    source = re.sub(r"\$[^$]*\$", " ", source)
    source = re.sub(r"\\(?:begin|end)\{[^}]+\}", " ", source)
    source = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", source)
    return len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", source))


class PaperCaseContractTests(unittest.TestCase):
    def read_case_file(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"missing paper-case file: {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8")

    def test_reference_matched_narrative_structure(self):
        """Catches missing, undersized, or structurally incompatible case text."""
        body = self.read_case_file(BODY)
        appendix = self.read_case_file(APPENDIX)

        self.assertGreaterEqual(prose_word_count(body), 180)
        self.assertLessEqual(prose_word_count(body), 230)
        self.assertGreaterEqual(prose_word_count(appendix), 900)
        self.assertLessEqual(prose_word_count(appendix), 1300)

        expected_subsections = [
            "Research setting and roles",
            "Handoff review and analytical workflow",
            "SciForge operation records",
            "Key results and interpretation",
            "Collaboration value",
            "Data and code availability",
        ]
        observed = re.findall(r"\\subsection\{([^}]+)\}", appendix)
        self.assertEqual(observed, expected_subsections)
        self.assertEqual(appendix.count(r"\begin{table}"), 1)
        self.assertEqual(appendix.count(r"\begin{figure}"), 2)

    def test_versioned_baselines_are_reported_with_their_scopes(self):
        """Catches swapped partitions or retained/test-set metric scope drift."""
        appendix = self.read_case_file(APPENDIX)
        expected = {
            "cleveland": (303, 199, 104, 0.45874587458745875, 0.8787202380952381, 0.7788461538461539),
            "hungarian": (261, 171, 90, 0.37547892720306514, 0.9044117647058824, 0.8333333333333334),
            "va": (130, 85, 45, 0.7769230769230769, 0.5628571428571428, 0.7555555555555555),
        }
        display_rows = {
            "cleveland": ("Cleveland", "303", "199 / 104", "45.87", "0.8787", "0.7788"),
            "hungarian": ("Hungarian", "261", "171 / 90", "37.55", "0.9044", "0.8333"),
            "va": ("VA", "130", "85 / 45", "77.69", "0.5629", "0.7556"),
        }

        for center, values in expected.items():
            result = json.loads((ROOT / "results" / "original" / f"{center}.json").read_text(encoding="utf-8"))
            observed = (
                result["retained_rows"], result["train_rows"], result["test_rows"],
                result["positive_rate"], result["auroc"], result["accuracy"],
            )
            self.assertEqual(observed, values)
            for cell in display_rows[center]:
                self.assertIn(cell, appendix)

        scoped_text = appendix.lower()
        self.assertRegex(scoped_text, r"positiv(?:e proportion|ity).{0,180}retained", msg="retained-sample positivity scope is missing")
        self.assertRegex(scoped_text, r"auroc.{0,120}(?:test set|test-set)", msg="test-set metric scope is missing")

    def test_va_supplementary_recomputation_is_temporally_separated(self):
        """Catches backdating the later VA audit into the original demonstration."""
        body = self.read_case_file(BODY)
        appendix = self.read_case_file(APPENDIX)
        audit = json.loads(
            (ROOT / "results" / "supplementary" / "va-test-distribution-20261122.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            (
                audit["test_total"], audit["test_positive"], audit["predicted_positive"],
                audit["true_positive"], audit["false_negative"], audit["true_negative"], audit["false_positive"],
            ),
            (45, 35, 38, 31, 4, 3, 7),
        )
        combined = body + "\n" + appendix
        for value in ("2026-11-22", "35", "45", "77.78", "38", "84.44", "75.56", "0.5629"):
            self.assertIn(value, combined)
        self.assertRegex(combined, r"(?:later|subsequent|supplementary) recomput", msg="later recomputation is not distinguished")

    def test_cross_references_use_the_migrated_case_labels(self):
        """Catches labels that cannot be wired into the migrated Overleaf tree."""
        body = self.read_case_file(BODY)
        appendix = self.read_case_file(APPENDIX)
        self.assertIn(r"\ref{fig:case-heart-disease}", body)
        self.assertIn(r"\ref{app:case-heart-disease}", body)
        for label in (
            "app:case-heart-disease",
            "fig:case-heart-disease",
            "fig:case-heart-operations",
            "tab:case-heart-baselines",
        ):
            self.assertEqual(appendix.count(rf"\label{{{label}}}"), 1)

    def test_vector_sources(self):
        """Catches non-editable exports or a mismatch between Draw.io and SVG labels."""
        figures = CASE_DIR / "figures"
        drawio = figures / "fig5_heart_disease.drawio"
        svg = figures / "fig5_heart_disease.svg"
        pdf = figures / "fig5_heart_disease.pdf"
        for path in (drawio, svg, pdf):
            self.assertTrue(path.is_file(), f"missing figure asset: {path.relative_to(ROOT)}")

        drawio_root = ET.parse(drawio).getroot()
        drawio_text = " ".join(
            html.unescape(node.attrib.get("value", "")) for node in drawio_root.iter()
        )
        drawio_text = re.sub(r"<[^>]+>", " ", drawio_text)
        svg_root = ET.parse(svg).getroot()
        svg_text = " ".join(svg_root.itertext())
        required = (
            "a",
            "b",
            "Cleveland",
            "Hungarian",
            "VA",
            "aggregate results only",
            "35/45",
            "38/45",
            "75.56%",
            "77.78%",
            "AUROC 0.5629",
        )
        for label in required:
            self.assertIn(label, drawio_text)
            self.assertIn(label, svg_text)

        self.assertTrue(pdf.read_bytes().startswith(b"%PDF-"), "figure PDF is not a valid PDF stream")

    def test_operation_screenshots_exist_and_are_provenance_labelled(self):
        """Catches missing, unreadable, or ambiguously sourced operation evidence."""
        appendix = self.read_case_file(APPENDIX)
        screenshots = CASE_DIR / "screenshots"
        for name in ("project-handoff.png", "metric-review.png"):
            path = screenshots / name
            self.assertTrue(path.is_file(), f"missing screenshot: {path.relative_to(ROOT)}")
            with Image.open(path) as image:
                self.assertEqual(image.format, "PNG")
                self.assertGreaterEqual(image.width, 1200)
                self.assertGreaterEqual(image.height, 700)
            include_at = appendix.index(f"screenshots/{name}")
            panel_text = appendix[include_at:include_at + 420]
            self.assertRegex(
                panel_text,
                r"(?:original demonstration screenshot|English-interface reconstruction)",
                msg=f"{name} lacks an explicit provenance label",
            )

    def test_package_documentation_and_public_links_resolve(self):
        """Catches a complete case package that remains undiscoverable or cannot be copied."""
        package_readme = CASE_DIR / "README.md"
        self.assertTrue(package_readme.is_file(), "paper package README is missing")
        text = package_readme.read_text(encoding="utf-8")
        for required in (
            "body.tex",
            "appendix.tex",
            "figures/fig5_heart_disease.drawio",
            "figures/fig5_heart_disease.svg",
            "figures/fig5_heart_disease.pdf",
            "screenshots/project-handoff.png",
            "screenshots/metric-review.png",
            "2026-11-22",
            "results/original",
            "results/supplementary/va-test-distribution-20261122.json",
        ):
            self.assertIn(required, text)

        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        public_report = (ROOT / "docs" / "case-study.en.md").read_text(encoding="utf-8")
        self.assertIn("paper/case-02-heart-disease/README.md", root_readme)
        self.assertIn("../paper/case-02-heart-disease/README.md", public_report)


if __name__ == "__main__":
    unittest.main()
