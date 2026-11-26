# Heart Disease paper case package

This directory contains the English paper case on cross-review of local models across the Cleveland, Hungarian and VA partitions of the UCI Heart Disease dataset. Like the Lean and CUDA cases in the SciForge paper, it follows a concrete research question through review, a change in interpretation, and the evidence supporting the final conclusion.

## Add to the Overleaf project

Copy this directory to `cases/case-02-heart-disease/` in the paper project, preserving all filenames. Then include:

```tex
\input{cases/case-02-heart-disease/body}
\input{cases/case-02-heart-disease/appendix}
```

`body.tex` is the approximately 200-word Results summary. `appendix.tex` contains the complete case narrative, operation records, quantitative interpretation, collaboration value, and data/code availability statement.

## Assets

- `figures/fig5_heart_disease.drawio` — editable source for the two-panel scientific figure.
- `figures/fig5_heart_disease.svg` — vector preview and web-compatible export.
- `figures/fig5_heart_disease.pdf` — publication export referenced by `appendix.tex`.
- `screenshots/project-handoff.png` — task handoff and accepted local reports.
- `screenshots/metric-review.png` — shared-note review of the VA metrics.

These two operation-record panels appear together in the manuscript's SciForge operation-record figure.

The scientific figure uses small vector icons for data, reports, review, revision and the VA audit. Its upper panel describes the original collaboration; the lower panel separately dates the supplementary computation. All Draw.io shapes, icon strokes, labels and connectors are native editable objects. The accuracy bars share a zero-based 0–100% scale.

To regenerate matching vector sources from the common layout:

```bash
python scripts/build_paper_figure.py
python scripts/build_paper_figure.py --pdf
```

The first command needs only Python's standard library. PDF export additionally requires Chrome or Chromium (`--chrome PATH` can select the executable). Regeneration replaces manual edits to the exported Draw.io file; keep any independently edited version separately.

## Numerical evidence

The case text and figure are derived from versioned repository evidence:

- `results/original/cleveland.json`
- `results/original/hungarian.json`
- `results/original/va.json`
- `results/supplementary/va-test-distribution-20261122.json`
- `provenance/reproduction-verification-20261124.json`

The main table reports positivity across all retained samples; AUROC and accuracy are local test-set metrics. The VA label and prediction counts were recomputed on **2026-11-22**, after the original collaboration demonstration, from the hash-verified analysis script and public source data. They are presented as supplementary evidence, not as a result available during the original review.

## Verification

From the repository root:

```bash
python scripts/reproduce.py
python -m unittest tests.test_paper_case -v
```

The first command reproduces all three local baselines and the VA supplementary distribution. The second validates package structure, evidence values, LaTeX labels, screenshot provenance, and consistency between the Draw.io and SVG figure sources. A minimal local wrapper is used for LaTeX compilation and visual inspection before release.

## Scope

One operator controlled three SciForge accounts on one Windows device. Separate working directories and aggregate-only handoffs were operating conventions in this demonstration; they do not establish institutional or cryptographic isolation. The custom NumPy baseline did not perform federated training, official FLamby evaluation, repeated splits, confidence intervals, joint-versus-local comparison, or clinical validation.
