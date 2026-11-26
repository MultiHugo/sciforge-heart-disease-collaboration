# When 75.56% accuracy was worse than a one-class baseline

Case author: Zeyu Zhang (张泽宇 / MultiHugo)

## Research setting

This case used the Cleveland, Hungarian, and VA partitions of the UCI Heart Disease dataset to ask whether cross-review could expose a misleading local-model result. One operator enacted three roles through separate SciForge accounts and working directories: Role B analyzed Cleveland and maintained the shared record, Role C analyzed Hungarian and reviewed the submissions, and Role D analyzed VA. The project exchanged method descriptions, aggregate outputs, and review comments rather than patient-level rows.

## Execution process

All roles ran the same custom NumPy logistic-regression workflow with random seed 43, a class-stratified train/test split, and standardization estimated from training data only. Roles C and D submitted their Hungarian and VA summaries through project tasks. Role B checked the declared protocol, accepted both materials, and integrated the three local baselines into one research record.

In the original November 12–13, 2026 demonstration, Role C questioned why the VA model reached 0.7556 test accuracy while its AUROC was only 0.5629. The question changed the report: accuracy and AUROC were shown together, retained-cohort positivity was distinguished from test-set metrics, and repeated splits or confidence intervals were named as the next analysis. The original project did not retain VA test-label counts or thresholded predictions, so it raised the prevalence question without yet answering it numerically.

![Shared note and cross-review](../figures/02-peer-review.png)

**Figure 1.** Original shared-note review of the VA accuracy–AUROC discrepancy.

## Main results

The local baselines are shown below. Positivity was calculated over all retained samples after cleaning; AUROC and accuracy were calculated on each partition’s own test split. Because the cohorts and test sets differ, the rows describe local results rather than a controlled model ranking.

| Partition | Retained samples | Train / test | Positivity, all retained samples | Test AUROC | Test accuracy |
|---|---:|---:|---:|---:|---:|
| Cleveland | 303 | 199 / 104 | 45.87% | 0.8787 | 0.7788 |
| Hungarian | 261 | 171 / 90 | 37.55% | 0.9044 | 0.8333 |
| VA | 130 | 85 / 45 | 77.69% | 0.5629 | 0.7556 |

A separately dated, hash-verified reconstruction on 2026-11-22 tested the VA concern. Among 45 test cases, 35 were positive (77.78%); the model predicted 38 positives (84.44%) and classified 34 cases correctly. The confusion counts were 31 true positives, four false negatives, three true negatives, and seven false positives. Thus, model accuracy was 75.56%, below the 77.78% obtained by predicting every case as positive, while AUROC remained 0.5629.

![Cross-review and follow-up analysis of the VA result](../paper/case-02-heart-disease/figures/fig5_heart_disease.svg)

**Figure 2.** Panel a shows the original collaborative path; panel b shows the separately dated VA diagnostic.

## Case value and boundaries

The case shows how cross-review can turn a reassuring score into a falsifiable evaluation question: before comparing local and collaborative training, harmonize preprocessing, repeat the split over multiple seeds, report uncertainty, and inspect threshold-dependent errors. It does not establish why VA discrimination was weak. The demonstration used one operator, one Windows device, three test accounts, and a custom NumPy model; it did not validate institutional isolation, run federated training or the official FLamby benchmark, compare joint and local models, or perform clinical validation. Data and reproduction materials are available through the [UCI Heart Disease dataset](https://doi.org/10.24432/C52P4X), the [public case repository](https://github.com/MultiHugo/sciforge-heart-disease-collaboration), and [METHODS.md](../METHODS.md); publication assets are collected in the [paper-ready LaTeX package](../paper/case-02-heart-disease/README.md).
