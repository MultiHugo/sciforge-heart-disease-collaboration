# Heart Disease paper case package

This directory contains the publication-ready English case on cross-review of local models across the Cleveland, Hungarian and VA partitions of the UCI Heart Disease dataset. Its structure mirrors the pediatric-sepsis case in the migrated SciForge 2.0 paper.

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
- `screenshots/project-handoff.png` — original demonstration screenshot of task handoff and accepted local reports.
- `screenshots/metric-review.png` — original demonstration screenshot of the shared-note review; the plug-in controls are already in English, while historical note and comment content remains unchanged.

The screenshots are original, pointer-free evidence. No historical project name, task, comment, or note was translated or reconstructed. An attempted English-interface recapture on 2026-11-26 could not reproduce the historical application windows faithfully, so the original screenshots were retained and explicitly labelled in the figure caption.

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
