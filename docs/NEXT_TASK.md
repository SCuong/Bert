# NEXT TASK

task_id: overnight-001
reviewed_commit_sha: aef160b22be9648367bfce6753eec71870c4f5a8
status: READY

## Goal

Resolve the final pre-experiment runtime and methodology issues before any model training.

## Required work

1. Standardize Python entrypoints from repository root. Because source files use `from src...`, document and verify:
   - `python -m src.data`
   - `python -m src.train_baseline`
   - `python -m src.train_bert`
   - `python -m src.evaluate`
   - `python -m src.predict`
   Update README, FINAL_REPORT, PRE_EXPERIMENT_REVIEW, and related docs. Ensure presentation/app imports also work from root.

2. Fix `src/data.py` entrypoint so `python -m src.data` performs only:
   - load/validate data,
   - missing/empty/duplicate/conflicting-label audit,
   - split leakage validation,
   - BERT-tokenizer token-length EDA,
   - figure/stat generation.
   It must not train any model.

3. Fix missing-label handling. Do not count missing labels and then fail later at `.astype(int)`. Either drop them with an accurate audit report or fail deliberately with a clear validation error. Avoid double-counting dropped rows.

4. Update Hugging Face Trainer usage for the installed/current API: prefer `processing_class=tokenizer` instead of deprecated/removed `tokenizer=tokenizer`. Smoke-check the installed Transformers API without training.

5. In `train_bert.py`, do not construct a test dataset during training. Training may use only train + validation. The test set remains reserved for final evaluation.

6. Treat `MAX_LENGTH = 128` as a candidate until EDA is executed. Do not claim it is EDA-selected yet. The later EDA report must include median, p90, p95, p99, and truncation rates at 128 and 256 before the final choice.

7. Clean documentation claims across README, FINAL_REPORT, data/README, docs/02_project_spec.md, PRE_EXPERIMENT_REVIEW, presentation outline/notes/source:
   - use "teacher-provided hotel-review sentiment dataset" unless provenance is independently verified;
   - Booking.com-style markers may be described as format observations, not provenance proof;
   - remove arbitrary pre-experiment KPIs such as Accuracy >= 88%, Macro F1 >= 0.88, and +5–8% improvement;
   - main research questions should focus on baseline vs fine-tuned BERT, contextual representation, and error patterns;
   - keep old-code analysis internal/reference-only rather than making it a main research objective;
   - if historical notebooks only report Accuracy, mark other historical metrics as "Not reported";
   - do not put epochs in a "Training time" column;
   - remove/pending-mark unverified empty-row counts, split counts, truncation percentages, inference-time estimates, or other generated-looking numbers;
   - replace "100% reproducible" with "controlled for reproducibility with fixed seeds and documented environment";
   - describe implementation as "independent implementation from scratch; reference code was not reused" rather than claiming strict clean-room implementation.

8. Report/PPT status must remain pre-experiment. If a final PPTX has not been generated from real metrics, say the generator is implemented and the final deck is pending experiment results.

9. Align training-history claims with implementation. If presentation says both training loss and validation loss are tracked, persist/plot actual trainer log history for both; otherwise change the claim.

10. Do not run:
    - TF-IDF baseline training,
    - BERT fine-tuning,
    - final test-set evaluation,
    - final PPT generation.

Allowed verification:
- syntax/compile,
- module imports,
- `--help`,
- Trainer signature/API smoke-check,
- presentation draft guard,
- data-loader validation on a tiny/sample path only if it does not create experiment results.

## Verification criteria

Before completion, verify:
- root-level module commands import correctly;
- no runtime import error from `src`;
- data audit handles missing labels/text consistently;
- `src.data` entrypoint actually invokes EDA logic;
- Trainer construction is compatible with the installed Transformers version;
- training script does not instantiate/use test data;
- docs no longer contain the unsupported KPI/provenance/reproducibility claims above;
- no real experiment has been executed.

## Completion protocol

When done:
1. Run the allowed smoke checks.
2. Commit with:
   `fix: resolve pre-experiment runtime and methodology issues`
3. Push to `main`.
4. Create/update `docs/REVIEW_REQUEST.md` containing:
   - request_commit_sha: the new pushed commit SHA
   - status: READY_FOR_REVIEW
   - summary of changes
   - smoke checks actually run and outputs
   - files changed
   - known issues/blockers
   - proposed next phase
5. Stop. Do not start experiments until a new NEXT_TASK arrives.
