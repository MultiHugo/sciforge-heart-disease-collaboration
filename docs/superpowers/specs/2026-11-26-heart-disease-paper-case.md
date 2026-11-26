# Heart Disease Paper Case Design

## Objective

Create an English, publication-ready Heart Disease case package that can be copied into the migrated SciForge 2.0 Overleaf project and that matches the structure, density, and asset conventions of the existing pediatric-sepsis case.

## Reference structure

The migrated paper stores each case as `body.tex`, `appendix.tex`, a `figures/` directory, and a `screenshots/` directory. The pediatric-sepsis reference uses:

- an approximately 200-word main-text case summary;
- a two-page appendix with six subsections: research setting and roles, handoff review and analytical workflow, SciForge operation records, key results and interpretation, collaboration value, and data/code availability;
- one editable scientific figure shipped as `.drawio`, `.svg`, and `.pdf`;
- one operation-record figure assembled from authentic product screenshots;
- one quantitative results table.

## Heart Disease package

Create `paper/case-02-heart-disease/` with the same organization:

- `body.tex`: 180--230 English words and one paragraph, suitable for inclusion in the paper's Results section.
- `appendix.tex`: 900--1,300 English words, the same subsection ordering as the reference case, one operation-record figure, one quantitative figure, and one table.
- `figures/fig5_heart_disease.drawio`, `.svg`, and `.pdf`: a two-panel editable figure. Panel a traces the three local partitions, aggregate-only handoffs, integration, and cross-review. Panel b explains the VA diagnostic result using the verified test composition and metrics.
- `screenshots/`: two authentic screenshots showing project/task handoff and the shared-note review. Prefer a faithful English-UI recapture when the historical project remains accessible. If that cannot be reproduced, retain the original Chinese evidence and state that fact in the caption; do not translate or fabricate historical user content.
- `README.md`: inclusion instructions, asset provenance, and the distinction between original demonstration evidence and the 2026-11-22 supplementary recomputation.

## Scientific content

The paper must report the verified Cleveland, Hungarian, and VA local baselines. Positivity for the main table is computed over all retained samples, while AUROC and accuracy are test-set metrics. The key scientific finding is the VA discrepancy: 35 of 45 test samples were positive (77.78%); the model predicted 38 positive (84.44%); its accuracy was 75.56%, below the 77.78% all-positive baseline; AUROC was 0.5629. The VA distribution analysis was recomputed on 2026-11-22, after the original collaboration demonstration, and must be labeled as such.

## Evidence boundaries

- One operator controlled three SciForge test accounts on one Windows device.
- Separate working directories did not prove institutional, operating-system, or cryptographic isolation.
- The demonstration exchanged aggregate reports and notes, but did not validate an enforceable data-governance boundary.
- No federated training, FedAvg, official FLamby benchmark, joint-versus-local model comparison, confidence interval, significance test, or external clinical validation was performed.
- The model was a custom NumPy logistic regression baseline and is not for clinical use.
- Screenshot captions distinguish original evidence from any reconstructed English-interface view.

## Acceptance criteria

1. Main-text length and appendix organization match the migrated reference case.
2. Every reported number matches the repository's versioned JSON evidence.
3. The key VA finding is prominent and the supplementary date is explicit.
4. The scientific figure opens in Draw.io and has visually equivalent SVG and PDF exports.
5. Screenshots are authentic, pointer-free, legible, and accurately labeled.
6. LaTeX paths, labels, references, and captions are portable into the migrated Overleaf tree.
7. Existing bilingual case reports and historical evidence remain intact.
