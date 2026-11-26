# Cross-review of local models across Heart Disease partitions

Case author: Zeyu Zhang (张泽宇 / MultiHugo)

The [paper-ready LaTeX case package](../paper/case-02-heart-disease/README.md) follows the structure and asset conventions of the SciForge 2.0 manuscript.

## Research setting and roles

This case used the Cleveland, Hungarian, and VA partitions of the UCI Heart Disease dataset to establish local classification baselines and test whether cross-review could reveal a misleading interpretation. One operator controlled three SciForge accounts on one Windows device: Role B analyzed Cleveland and maintained the shared record, Role C analyzed Hungarian and reviewed the submissions, and Role D analyzed VA. The roles worked in separate directories and handed off method summaries and aggregate results rather than patient-level rows.

## Analysis and cross-review

All roles used the same custom NumPy logistic-regression workflow: random seed 43, a class-stratified train/test split, and standardization estimated from training data only. After local CPU analysis, Roles C and D submitted their methods and aggregate results. Role B accepted the two reports and integrated all three baselines into the shared research record (Figure 1).

Cross-review centred on one discrepancy: VA reached 0.7556 test accuracy but only 0.5629 AUROC. Role C asked whether prevalence was making the accuracy look more reassuring than the model's discrimination. The shared record was revised to report prevalence, accuracy and AUROC together and to identify repeated splits and uncertainty estimates as the next experiment (Figure 2). The original demonstration did not preserve the VA test-label and prediction counts; those counts were recomputed later, on 2026-11-22, from the hash-verified script and public source data.

## Main results

The table reports positivity across all retained samples after cleaning. AUROC and accuracy come from each partition's own test set, so the rows describe local baselines rather than a controlled model ranking.

| Partition | Retained samples | Train / test | Positivity, all retained samples | Test AUROC | Test accuracy |
|---|---:|---:|---:|---:|---:|
| Cleveland | 303 | 199 / 104 | 45.87% | 0.8787 | 0.7788 |
| Hungarian | 261 | 171 / 90 | 37.55% | 0.9044 | 0.8333 |
| VA | 130 | 85 / 45 | 77.69% | 0.5629 | 0.7556 |

### Representative finding: VA accuracy masked weak discrimination

The later recomputation found 35 positive labels among 45 VA test samples (77.78%). At a threshold of 0.5, the model predicted 38 positives (84.44%), with 31 true positives, four false negatives, three true negatives and seven false positives. Its 75.56% accuracy was below the 77.78% obtained by predicting every sample as positive, while AUROC remained 0.5629. The review therefore converted a seemingly acceptable accuracy into a specific evaluation question: before comparing local and collaborative training strategies, align preprocessing, repeat the split and quantify uncertainty.

## Collaboration outcome and scope

The three local analyses, accepted reports, review question and revised interpretation remained attached to one project. The case demonstrates a traceable collaborative handoff and a concrete scientific adjustment, not a federated-learning result. It used one operator, one device and a custom NumPy implementation; it did not validate institutional isolation, run official FLamby evaluation, compare federated and local models, or estimate confidence intervals.

## Figures

![Project tasks and submissions](../figures/01-project-board.png)

Figure 1. The lead reviews completed Hungarian and VA tasks and submitted materials.

![Shared note and cross-review](../figures/02-peer-review.png)

Figure 2. Members discuss VA metric interpretation, the scope of shared materials, and future evaluation. This original screenshot does not contain the later 2026-11-22 recomputation.

See [METHODS.md](../METHODS.md) and the [repository overview](../README.md) for data attribution and reproduction instructions.
