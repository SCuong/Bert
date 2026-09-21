# NEXT TASK

task_id: overnight-007
reviewed_commit_sha: 9b442fafd1ff81828317365b855ba7621ed13a19
status: READY

## Goal

Perform evidence-based qualitative analysis of the 20 already-frozen BERT Test misclassifications in artifacts/metrics/error_cases.json. Do not rerun Test evaluation, retrain, retune, or modify model artifacts. This phase is analysis-only and prepares the evidence for the final report/presentation packaging phase.

## Reviewer decision on final Test evaluation

The held-out Test evaluation is accepted and frozen.

Final Test results:
- Test samples: 3,949
- Baseline Accuracy: 0.8194479615092428
- Baseline Macro F1: 0.8192008301395627
- BERT Accuracy: 0.8483160293745252
- BERT Macro F1: 0.8482655894059412
- Accuracy delta BERT - Baseline: +0.0289
- Macro F1 delta BERT - Baseline: +0.0291
- Baseline confusion matrix: [[1691, 293], [420, 1545]]
- BERT confusion matrix: [[1711, 273], [326, 1639]]
- Total BERT Test errors: 599
- Selected qualitative sample: 10 high-confidence FP + 10 high-confidence FN

These numbers are FINAL. Do not recompute predictions or alter the experiment.

## Required work

1. Read artifacts/metrics/error_cases.json and manually inspect all 20 selected cases.

2. For each case, record:
   - case index;
   - true label;
   - predicted label;
   - confidence;
   - a short identifying excerpt, not a rewritten example;
   - observed linguistic/data pattern;
   - concise evidence-based explanation of why the case may be difficult;
   - analysis confidence: high / medium / low.

3. Do not force cases into preconceived categories. Use categories only when supported by the actual text. Possible categories may include:
   - mixed sentiment / competing clauses;
   - negation or concessive structure;
   - possible label ambiguity or label noise;
   - template/source marker effects such as "No Positive" or "No Negative";
   - long review / possible truncation;
   - noisy grammar, spelling, or malformed text;
   - domain/platform complaint versus hotel sentiment;
   - other observed patterns.
   Do not claim sarcasm unless the text genuinely supports it.

4. Distinguish clearly between:
   - a plausible model reasoning failure;
   - an ambiguous mixed-sentiment case;
   - a possible dataset-label/data-construction issue.
   Never state that a label is definitely wrong unless the dataset provides evidence for that conclusion.

5. For each of the 20 cases, compute BERT token length using the frozen tokenizer and MAX_LENGTH=128, and mark whether the text would be truncated. This is descriptive analysis only. Do not run model inference again.

6. Produce:
   - docs/04_error_analysis.md
   - artifacts/metrics/error_analysis_summary.json

7. docs/04_error_analysis.md must contain:
   - scope and methodology;
   - explicit note that these are the 20 highest-confidence selected errors, not a random or statistically representative sample of all 599 errors;
   - per-case analysis table;
   - aggregate category counts derived from the actual 20 assignments;
   - FP vs FN pattern observations;
   - truncation observations based on measured token lengths;
   - data-quality/label-ambiguity observations;
   - limitations of the qualitative analysis;
   - a short evidence-based answer to RQ3.

8. error_analysis_summary.json must be machine-readable and derived from the same 20 cases. Include:
   - total_selected_cases = 20;
   - selected_fp = 10;
   - selected_fn = 10;
   - category_counts;
   - truncation_count;
   - per_case records with labels/prediction/confidence/token_length/truncated/categories/analysis_confidence.

9. Cross-check that no final Test metric JSON, model weight, hyperparameter, split logic, or prediction output is modified.

10. Do NOT in this phase:
   - run src.evaluate;
   - run src.train_baseline;
   - run src.train_bert;
   - generate the final PowerPoint;
   - rewrite FINAL_REPORT;
   - change README research conclusions;
   - modify model artifacts;
   - claim the 20 selected cases represent all 599 errors.

## Verification criteria

Before completion verify:
- all 20 entries in error_cases.json are represented exactly once in the analysis;
- FP count = 10 and FN count = 10;
- token lengths are measured with the frozen BERT tokenizer;
- every truncation claim is supported by token_length > 128;
- category counts exactly match per-case assignments;
- uncertain cases are explicitly marked as uncertain rather than overstated;
- no training or Test prediction command was executed;
- final Test metrics and model artifacts remain unchanged.

## Required commit message

Commit the tracked analysis artifacts with exactly:

analysis: classify final BERT test errors

Push to main.

## Completion protocol

After pushing the implementation/analysis commit:
1. Obtain the exact commit SHA with git rev-parse HEAD.
2. Update docs/REVIEW_REQUEST.md with:
   - request_commit_sha: <exact analysis commit SHA>
   - status: READY_FOR_REVIEW
   - summary of the qualitative method
   - category counts
   - truncation count
   - key FP observations
   - key FN observations
   - possible label/data-quality observations with uncertainty language
   - confirmation that all 20 cases were covered
   - confirmation that no model/Test predictions were rerun
   - files changed
   - verification commands actually run
   - known issues/blockers
   - proposed next phase: final report + final PPT + demo smoke test + study/defense materials
3. Commit/push the review request if needed.
4. Stop and wait for the next NEXT_TASK.
