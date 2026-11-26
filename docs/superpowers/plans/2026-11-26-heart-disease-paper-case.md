# Heart Disease Paper Case Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a verified, publication-ready Heart Disease case package that mirrors the migrated SciForge paper's pediatric-sepsis case in structure, content density, and editable visual assets.

**Architecture:** Keep the paper package self-contained under `paper/case-02-heart-disease/`, while treating the existing JSON result files and provenance records as the only sources of numerical truth. Generate one editable two-panel scientific figure from Draw.io source and reference authentic screenshots without altering historical user content. A focused Python unittest validates structure, metric text, dates, labels, paths, and vector-source consistency.

**Tech Stack:** LaTeX, Draw.io XML, SVG, PDF, Python 3 standard library/unittest, SciForge desktop UI and computer-use capture.

**Spec:** `docs/superpowers/specs/2026-11-26-heart-disease-paper-case.md`

## Global Constraints

- The main-text case is 180--230 English words; the appendix is 900--1,300 English words.
- Use the reference subsection ordering and include exactly one results table and at most two figures.
- Main-table positivity is over all retained samples; AUROC and accuracy are test-set metrics.
- Label the VA test-distribution analysis as a 2026-11-22 supplementary recomputation, not part of the original demonstration.
- State that one operator controlled three accounts on one Windows device and that institutional isolation and federated learning were not validated.
- Do not fabricate translated historical content; reconstructed English-interface screenshots must be disclosed as reconstructions.
- Ship the scientific figure as matching `.drawio`, `.svg`, and `.pdf` files.
- Preserve all existing historical files and bilingual reports.

## Review Focus

- Metric scope: the test must distinguish retained-sample positivity from test-set AUROC and accuracy.
- Temporal provenance: the test must require the date `2026-11-22` beside the supplementary VA distribution findings.
- Collaboration claims: the test must reject wording that implies real institutional isolation or completed federated training.
- Portable inclusion: the test must resolve every local `\includegraphics` target and every figure/table reference.
- Vector equivalence: the test must find the same required labels and numerical values in Draw.io source and exported SVG, followed by manual PDF visual comparison.

---

### Task 1: Add the paper-package contract test

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_paper_case.py`

**Interfaces:**
- Consumes: `results/original/*.json`, `results/supplementary/va-test-distribution-20261122.json`, and the package contract in the approved spec.
- Produces: `PaperCaseContractTests`, the single verification entry point for later tasks.

- [ ] **Step 1: Write the failing structure and evidence tests**

Add unittest cases that require the exact package paths, a 180--230-word body, a 900--1,300-word appendix, all six reference subsections, one table, no more than two figures, and the verified Cleveland/Hungarian/VA values.

- [ ] **Step 2: Add boundary and provenance assertions**

Require `2026-11-22`, the VA `35/45`, `38/45`, `75.56%`, `77.78%`, and `0.5629` findings; require single-operator/single-device and no-federated-training language; reject unsupported claims such as completed federated learning or proven institutional isolation.

- [ ] **Step 3: Run the tests to verify they fail for the missing package**

Run: `python -m unittest tests.test_paper_case -v`

Expected: FAIL because `paper/case-02-heart-disease/body.tex` and related assets do not yet exist.

- [ ] **Step 4: Commit the contract test**

```bash
git add tests
git commit -m "test: define Heart Disease paper case contract"
```

### Task 2: Write the reference-matched LaTeX narrative

**Files:**
- Create: `paper/case-02-heart-disease/body.tex`
- Create: `paper/case-02-heart-disease/appendix.tex`

**Interfaces:**
- Consumes: the existing JSON evidence, provenance records, and Task 1 contract.
- Produces: LaTeX labels `app:case-heart-disease`, `fig:case-heart-disease`, `fig:case-heart-operations`, and `tab:case-heart-baselines` for inclusion by the migrated paper.

- [ ] **Step 1: Write the 180--230-word Results summary**

Use one paragraph that states the setting, three roles, local baseline protocol, VA review finding, supplementary recomputation, and the evidence boundary; reference the appendix and quantitative figure.

- [ ] **Step 2: Write the appendix's setting and workflow sections**

Follow the pediatric-sepsis case's paragraph density while replacing operational log language with the scientific handoff, the specific VA cross-review adjustment, and only the provenance detail needed to support the conclusion.

- [ ] **Step 3: Write the operations, results, collaboration-value, and availability sections**

Include one operation-record figure, one two-panel scientific figure, one baseline table, the later VA recomputation, concise limitations, the UCI DOI, and the public repository URL.

- [ ] **Step 4: Run the contract tests**

Run: `python -m unittest tests.test_paper_case -v`

Expected: narrative and numerical checks pass; asset checks still fail because figures and screenshots are missing.

- [ ] **Step 5: Commit the narrative**

```bash
git add paper/case-02-heart-disease/body.tex paper/case-02-heart-disease/appendix.tex
git commit -m "docs: draft Heart Disease paper case"
```

### Task 3: Build the editable scientific figure

**Files:**
- Create: `paper/case-02-heart-disease/figures/fig5_heart_disease.drawio`
- Create: `paper/case-02-heart-disease/figures/fig5_heart_disease.svg`
- Create: `paper/case-02-heart-disease/figures/fig5_heart_disease.pdf`

**Interfaces:**
- Consumes: exact metrics from `results/original/*.json` and `results/supplementary/va-test-distribution-20261122.json`.
- Produces: one two-panel figure used by `appendix.tex`; panel a is the collaboration/handoff flow, panel b is the VA diagnostic comparison.

- [ ] **Step 1: Extend the contract tests for editable-vector content**

Parse Draw.io XML and SVG with Python's XML parser; require panel labels, three partition names, `aggregate results only`, `35/45`, `38/45`, `75.56%`, `77.78%`, and `AUROC 0.5629` in both sources.

- [ ] **Step 2: Run the vector tests to verify they fail**

Run: `python -m unittest tests.test_paper_case.PaperCaseContractTests.test_vector_sources -v`

Expected: FAIL because the vector files do not exist.

- [ ] **Step 3: Create the Draw.io source and export SVG/PDF**

Use a restrained journal palette, readable sans-serif labels, solid arrows for material handoff, dashed arrows for review/revision, and no claims that raw-row locality was technically enforced.

- [ ] **Step 4: Render and visually compare all three forms**

Open the `.drawio` source in Draw.io, render SVG and PDF to raster previews, and confirm equivalent labels, line routing, panel alignment, margins, and no clipping at paper-column width.

- [ ] **Step 5: Run vector and narrative tests**

Run: `python -m unittest tests.test_paper_case -v`

Expected: vector and narrative checks pass; screenshot checks may still fail.

- [ ] **Step 6: Commit the scientific figure**

```bash
git add paper/case-02-heart-disease/figures tests/test_paper_case.py
git commit -m "docs: add editable Heart Disease case figure"
```

### Task 4: Capture and label authentic operation records

**Files:**
- Create: `paper/case-02-heart-disease/screenshots/project-handoff.png`
- Create: `paper/case-02-heart-disease/screenshots/metric-review.png`
- Modify: `paper/case-02-heart-disease/appendix.tex`

**Interfaces:**
- Consumes: the historical B/C test profiles and original screenshots in `figures/`.
- Produces: two pointer-free operation-record screenshots with captions that state whether each is original evidence or an English-interface reconstruction.

- [ ] **Step 1: Test whether the historical project still opens under the English C profile**

Launch only the isolated B/C test profiles, preserve the normal SciForge profile, and verify the Heart Disease board and shared note still show the original task/result state.

- [ ] **Step 2: Capture faithful English-interface views when reproducible**

Capture the task handoff and VA review screens without the mouse pointer or click halo. Keep historical user-created project names, comments, and notes unchanged even when they remain Chinese.

- [ ] **Step 3: Apply the evidence fallback when reproduction is incomplete**

If either state is unavailable or materially different, use the corresponding original repository screenshot and change the caption from `English-interface reconstruction` to `original demonstration screenshot`; do not synthesize missing history.

- [ ] **Step 4: Run screenshot-path and caption tests**

Run: `python -m unittest tests.test_paper_case -v`

Expected: all automatic contract tests pass.

- [ ] **Step 5: Commit the operation records**

```bash
git add paper/case-02-heart-disease/screenshots paper/case-02-heart-disease/appendix.tex
git commit -m "docs: add Heart Disease operation evidence"
```

### Task 5: Package, compile, and final-review the case

**Files:**
- Create: `paper/case-02-heart-disease/README.md`
- Modify: `docs/case-study.en.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Tasks 1--4 and the migrated Overleaf case folder convention.
- Produces: a self-contained public package plus links from the existing English report and repository overview.

- [ ] **Step 1: Add inclusion and provenance documentation**

Document where to copy `body.tex`, `appendix.tex`, `figures/`, and `screenshots/`; list the evidence JSON files; explain original versus reconstructed screenshots and the later VA recomputation.

- [ ] **Step 2: Align the public English report with the paper wording**

Make the VA diagnostic finding prominent, remove execution-log phrasing, avoid repeated defensive limitations, and link to the publication package without deleting the existing case history.

- [ ] **Step 3: Validate LaTeX references and compile in a minimal wrapper**

Run the repository test suite, then compile a local wrapper with the installed LaTeX engine. If no engine is installed, validate syntax and asset paths locally and compile after importing into the migrated Overleaf project; record which route was used in the package README.

- [ ] **Step 4: Perform visual QA**

Inspect every compiled page at normal zoom, the SVG preview, the PDF figure, and both screenshots for legibility, clipping, duplicated captions, mouse pointers, and accidental disclosure of credentials or unrelated personal data.

- [ ] **Step 5: Reproduce the numerical evidence**

Run: `python scripts/reproduce.py`

Expected: all three partitions and the VA supplementary distribution report PASS.

- [ ] **Step 6: Run the final contract suite**

Run: `python -m unittest tests.test_paper_case -v`

Expected: PASS for every test.

- [ ] **Step 7: Commit the completed package**

```bash
git add README.md docs/case-study.en.md paper/case-02-heart-disease
git commit -m "docs: publish Heart Disease paper case package"
```
