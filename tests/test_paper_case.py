import json
import html
import re
import struct
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import mock

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

    def assert_existing_contract_detects_mutation(self, body: str, appendix: str, methods: tuple[str, ...]):
        """Run selected contract checks against mutated in-memory artifacts."""
        with tempfile.TemporaryDirectory(dir=ROOT / ".superpowers") as folder:
            temp = Path(folder)
            body_path = temp / "body.tex"
            appendix_path = temp / "appendix.tex"
            body_path.write_text(body, encoding="utf-8")
            appendix_path.write_text(appendix, encoding="utf-8")
            module = sys.modules[__name__]
            failures = 0
            with mock.patch.object(module, "BODY", body_path), mock.patch.object(module, "APPENDIX", appendix_path):
                for method in methods:
                    result = unittest.TestResult()
                    type(self)(method).run(result)
                    failures += len(result.failures) + len(result.errors)
        self.assertGreater(failures, 0, "contract accepted a known-invalid mutation")

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
        expected_rows = {
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

        table = re.search(r"\\begin\{tabular\}.*?\\end\{tabular\}", appendix, re.DOTALL)
        self.assertIsNotNone(table, "baseline table is missing")
        rows = re.findall(
            r"(?m)^\s*(Cleveland|Hungarian|VA)\s*&\s*(\d+)\s*&\s*(\d+\s*/\s*\d+)\s*&\s*([0-9.]+)\s*&\s*([0-9.]+)\s*&\s*([0-9.]+)\s*\\\\",
            table.group(0),
        )
        observed_rows = {row[0].lower(): row for row in rows}
        self.assertEqual(observed_rows, expected_rows)

        caption = re.search(
            r"\\caption\{Local logistic-regression baselines(.*?)\}", appendix, re.DOTALL
        )
        self.assertIsNotNone(caption)
        scoped_text = caption.group(1).lower()
        self.assertRegex(scoped_text, r"positiv(?:e proportion|ity).*all retained samples")
        self.assertRegex(scoped_text, r"auroc and accuracy.*(?:test set|test-set)")

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
        body_audit = next(
            (paragraph for paragraph in body.split("\n\n") if "later recomputation" in paragraph.lower()),
            "",
        )
        appendix_audit = next(
            (
                paragraph
                for paragraph in appendix.split("\n\n")
                if "supplementary recomputation" in paragraph.lower() and "35" in paragraph
            ),
            "",
        )
        self.assertTrue(body_audit, "body audit passage is missing")
        self.assertTrue(appendix_audit, "appendix audit passage is missing")
        for value in ("2026-11-22", "35", "45", "77.78", "38", "75.56", "0.5629"):
            self.assertIn(value, body_audit)
            self.assertIn(value, appendix_audit)
        self.assertIn("84.44", appendix_audit)

    def test_collaboration_claims_respect_demonstration_boundary(self):
        """Catches claims of federated training or institutional isolation that were not tested."""
        body = self.read_case_file(BODY)
        appendix = self.read_case_file(APPENDIX)
        combined = (body + "\n" + appendix).lower()
        self.assertIn("one operator", combined)
        self.assertRegex(combined, r"(?:one windows device|single-device)")
        self.assertNotRegex(combined, r"(?:completed|successful|performed) federated training")
        self.assertNotRegex(combined, r"(?:validated|proved|established) institutional (?:data )?isolation")
        self.assertRegex(combined, r"(?:not federated training|did not perform federated training)")
        self.assertRegex(combined, r"(?:not .*institutional data isolation|did not .*institutional isolation)")

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

        combined = body + "\n" + appendix
        labels = re.findall(r"\\label\{([^}]+)\}", combined)
        self.assertEqual(len(labels), len(set(labels)), "duplicate LaTeX label")
        references = re.findall(r"\\ref\{([^}]+)\}", combined)
        self.assertFalse(set(references) - set(labels), "undefined LaTeX reference")

        prefix = "cases/case-02-heart-disease/"
        graphics = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", combined)
        self.assertTrue(graphics)
        for target in graphics:
            self.assertTrue(target.startswith(prefix), f"non-portable graphics root: {target}")
            local = CASE_DIR / target.removeprefix(prefix)
            self.assertTrue(local.is_file(), f"missing graphics target: {target}")

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

    def test_operation_screenshots_exist_and_are_readable(self):
        """Catches missing or unreadable operation evidence."""
        screenshots = CASE_DIR / "screenshots"
        for name in ("project-handoff.png", "metric-review.png"):
            path = screenshots / name
            self.assertTrue(path.is_file(), f"missing screenshot: {path.relative_to(ROOT)}")
            data = path.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(data[12:16], b"IHDR")
            width, height = struct.unpack(">II", data[16:24])
            self.assertGreaterEqual(width, 1200)
            self.assertGreaterEqual(height, 700)

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

    def test_contract_rejects_partition_value_swaps(self):
        body = BODY.read_text(encoding="utf-8")
        appendix = APPENDIX.read_text(encoding="utf-8")
        appendix = appendix.replace(
            "Cleveland & 303 & 199 / 104 & 45.87 & 0.8787 & 0.7788",
            "Cleveland & 303 & 199 / 104 & 45.87 & 0.9044 & 0.7788",
        ).replace(
            "Hungarian & 261 & 171 / 90 & 37.55 & 0.9044 & 0.8333",
            "Hungarian & 261 & 171 / 90 & 37.55 & 0.8787 & 0.8333",
        )
        self.assert_existing_contract_detects_mutation(
            body, appendix, ("test_versioned_baselines_are_reported_with_their_scopes",)
        )

    def test_contract_rejects_displaced_audit_date(self):
        body = BODY.read_text(encoding="utf-8").replace("2026-11-22", "2026-11-13")
        appendix = APPENDIX.read_text(encoding="utf-8").replace("2026-11-22", "2026-11-13")
        appendix += "\nEvidence package availability date: 2026-11-22.\n"
        self.assert_existing_contract_detects_mutation(
            body, appendix, ("test_va_supplementary_recomputation_is_temporally_separated",)
        )

    def test_contract_rejects_collaboration_overclaims(self):
        body = BODY.read_text(encoding="utf-8").replace(
            "This single-device demonstration tested collaborative interpretation, not federated training or institutional data isolation.",
            "This multi-institutional deployment completed federated training and validated institutional data isolation.",
        )
        appendix = APPENDIX.read_text(encoding="utf-8")
        self.assert_existing_contract_detects_mutation(
            body,
            appendix,
            (
                "test_reference_matched_narrative_structure",
                "test_cross_references_use_the_migrated_case_labels",
                "test_va_supplementary_recomputation_is_temporally_separated",
                "test_collaboration_claims_respect_demonstration_boundary",
            ),
        )

    def test_contract_rejects_broken_graphics_and_undefined_refs(self):
        body = BODY.read_text(encoding="utf-8")
        appendix = APPENDIX.read_text(encoding="utf-8").replace(
            "cases/case-02-heart-disease/figures/", "cases/missing/figures/"
        )
        appendix += "\nSee Fig.~\\ref{fig:undefined}.\n"
        self.assert_existing_contract_detects_mutation(
            body, appendix, ("test_cross_references_use_the_migrated_case_labels",)
        )

    def test_publication_assets_preserve_legibility_at_manuscript_width(self):
        """Catches source type and screenshot layouts that collapse below readable size."""
        svg = (CASE_DIR / "figures" / "fig5_heart_disease.svg").read_text(encoding="utf-8")
        source_font_sizes = [int(value) for value in re.findall(r"font:(?:700 )?(\d+)px", svg)]
        self.assertTrue(source_font_sizes)
        self.assertGreaterEqual(min(source_font_sizes), 20)

        appendix = APPENDIX.read_text(encoding="utf-8")
        self.assertNotIn(r"{0.49\textwidth}", appendix)
        for name in ("project-handoff.png", "metric-review.png"):
            options = re.search(
                rf"\\includegraphics\[([^]]+)\]\{{cases/case-02-heart-disease/screenshots/{re.escape(name)}\}}",
                appendix,
            )
            self.assertIsNotNone(options)
            self.assertIn("trim=", options.group(1))
            self.assertIn("clip", options.group(1))


if __name__ == "__main__":
    unittest.main()
