# NEXT TASK

task_id: overnight-004
reviewed_commit_sha: 48e69dac96c68f7ece6e58b717d46b82331280df
status: READY

## Goal

Close the remaining Test-set sealing/provenance gaps, then run the real validation-only TF-IDF baseline. Do not fine-tune BERT and do not run final Test evaluation in this phase.

## Reviewer decision on overnight-003

The artifact-path cleanup, comparative evaluator preparation, hardware-claim cleanup, and validation-only baseline structure are accepted.

Two residual issues must be corrected before/while running the baseline:

1. `src.data.analyze_and_plot_data()` now writes the EDA JSON itself, but `decision_rationale` still hard-codes measured numbers (`96.07%`, `121.0`, `3.93%`, `3.84%`) instead of deriving the text from the just-computed `stats_dict`. This can silently become stale if the data/tokenizer/config changes. Generate the rationale from computed values or move the human rationale out of the JSON.
2. `split_data()` prints the Test-set sample count and Test label distribution on every call. Therefore `python -m src.train_baseline` and `python -m src.train_bert` still expose Test-derived label statistics during model development even though callers ignore the returned Test dataframe. The development invariant is: split construction may use labels for stratification, but training commands must not print, persist, inspect, or use Test-derived counts/distributions/predictions/metrics for model or hyperparameter decisions.

## Required work

### A. Make EDA rationale data-derived

1. In `src/data.py`, remove hard-coded measured values from `decision_rationale`.
2. Either:
   - build the rationale string from the actual values already computed in `stats_dict`, or
   - keep `token_length_stats.json` measurement-only and place the human explanation in documentation.
3. Re-run `python -m src.data` after the change.
4. Verify the regenerated `artifacts/metrics/token_length_stats.json` still contains the accepted real measurements and is reproducible on a second run.

### B. Fully seal Test-derived reporting during model development

1. Refactor the split/reporting API so development callers can obtain deterministic Train/Validation partitions without printing or otherwise surfacing Test label distribution/counts.
2. Preserve the exact same seed-42 stratified partitioning logic used by the final evaluator.
3. The standalone EDA/data-audit command may continue to report split counts and zero-overlap facts because those are part of the accepted data-integrity audit.
4. `src/train_baseline.py` must not print Test count/distribution or inspect Test labels/metrics.
5. `src/train_bert.py` must follow the same sealed-development behavior for its future run.
6. `src/evaluate.py` remains the only model-evaluation command allowed to expose final Test labels/predictions/metrics after both trained model artifacts exist.

### C. Run the real validation-only baseline

After A and B pass static checks:

1. Run exactly:
   `python -m src.train_baseline`
2. Train TF-IDF + Logistic Regression on Train only with the already-defined fixed baseline configuration.
3. Evaluate only on Validation.
4. Persist the real outputs:
   - `artifacts/metrics/baseline_validation_metrics.json`
   - `artifacts/figures/baseline_val_confusion_matrix.png`
   - local ignored model: `artifacts/model/baseline_tfidf_lr.joblib`
5. Record real training time and validation inference time as measured by the run.
6. Do not tune `C`, `max_features`, n-grams, or other baseline hyperparameters in response to Validation results in this phase. This run establishes the fixed baseline reference.

### D. Validate the artifacts and documentation

1. Confirm the validation metrics JSON contains at minimum:
   - `evaluation_split: validation`
   - Accuracy
   - Macro Precision
   - Macro Recall
   - Macro F1
   - Weighted F1
   - per-class metrics
   - training time
   - validation inference time
   - validation sample count
   - confusion matrix
2. Check that the confusion-matrix totals equal the validation sample count.
3. Check that `artifacts/model/baseline_tfidf_lr.joblib` exists locally but is ignored by Git and is not committed.
4. Confirm that no final-Test metric artifact exists as a result of this phase:
   - no new `baseline_test_metrics.json`
   - no new `bert_test_metrics.json`
   - no new `comparative_metrics.json`
   - no `error_cases.json` from final evaluation
5. Update only the relevant docs/presentation source with the real Baseline **Validation** results, clearly labeled as development/validation results and never presented as final Test performance.
6. Do not claim that BERT outperforms or underperforms the baseline yet.

### E. Keep the next phases sealed

Do NOT run in this phase:
- `python -m src.train_bert`
- `python -m src.evaluate` after model artifacts exist
- any Test-set prediction/evaluation
- final PowerPoint generation

Do not create placeholder BERT/Test metrics to satisfy report or slide code.

## Verification criteria

Before completion, verify all of the following:

- `python -m src.data` succeeds and a second run gives identical EDA JSON content.
- `decision_rationale` is derived from computed measurements or removed from the JSON; it is not a hard-coded copy of today's numbers.
- Running/importing the development split path used by `train_baseline.py` and `train_bert.py` does not print Test count or Test label distribution.
- Baseline training completes successfully on Train only.
- Baseline development evaluation uses Validation only.
- `baseline_validation_metrics.json` contains real measured values and its confusion-matrix sum equals the validation sample count.
- `baseline_tfidf_lr.joblib` exists locally and remains Git-ignored.
- No final Test metric/error artifact is generated by this phase.
- Documentation and presentation source label these numbers as Validation results, not final Test results.

## Completion protocol

When done:
1. Review the generated baseline metrics/figure and the EDA diff.
2. Commit source/docs/real validation artifacts with exactly:
   `experiment: train validation-only baseline`
3. Push to `main`.
4. Obtain the exact implementation SHA with `git rev-parse HEAD` after the implementation commit is created and pushed.
5. Create/update `docs/REVIEW_REQUEST.md` with:
   - `request_commit_sha: <exact implementation SHA>`
   - `status: READY_FOR_REVIEW`
   - summary of the split-sealing and EDA-rationale fixes
   - exact Baseline Validation metrics copied from the generated JSON
   - measured training/inference times
   - confusion-matrix consistency check
   - confirmation that the local baseline model exists and is ignored by Git
   - confirmation that no final Test evaluation/artifacts were produced
   - verification commands actually run
   - files/artifacts changed
   - known issues/blockers
   - proposed next phase
6. Commit/push the review request if needed.
7. Stop and wait for the next NEXT_TASK.
