import json
import re
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
