# NEXT TASK

task_id: overnight-005
reviewed_commit_sha: 2a8a407627a56541b86053a98ec2973fe8127cbe
status: READY

## Goal

Harden the BERT-model completion guard, then run the first and only planned validation-only BERT fine-tuning run with the already-fixed configuration. Persist real validation artifacts and training telemetry. Keep the held-out Test Set sealed; do not run final comparative evaluation in this phase.

## Reviewer decision on overnight-004

The validation-only baseline is accepted as the fixed development reference.

Accepted measured Baseline Validation result:
- split: Validation only
- sample count: 1,975
- Accuracy: 0.810126582278481
- Macro Precision: 0.8115951441377918
- Macro Recall: 0.8099680454828865
- Macro F1: 0.8098450029770088
- Weighted F1: 0.8098783478942885
- confusion matrix: [[838, 154], [221, 762]]

The split-sealing and data-derived EDA rationale changes are also accepted.

One safety issue must be fixed before the BERT run is treated as complete: `train_bert.py` currently creates `BERT_BEST_MODEL_DIR` before training, while `evaluate.py` considers the BERT model available if that directory merely exists. A failed/interrupted training run could therefore leave an empty/incomplete directory that incorrectly opens the final Test-evaluation gate. The final evaluator must require a genuinely complete trained-model artifact, not just a directory.

## Required work

### A. Harden BERT artifact completion before training

1. In `src/train_bert.py`, do not pre-create `BERT_BEST_MODEL_DIR` merely to prepare for training. Let the successful model-save step create/populate it.
2. Add a robust model-completeness check shared with `src/evaluate.py`. At minimum, a BERT artifact must contain:
   - `config.json`;
   - model weights (`model.safetensors` or `pytorch_model.bin`);
   - tokenizer files sufficient for `AutoTokenizer.from_pretrained(BERT_BEST_MODEL_DIR)`.
3. Prefer an explicit local completion marker/manifest written only after all of the following succeed:
   - training finishes;
   - the best checkpoint is loaded;
   - the best model and tokenizer are saved;
   - validation metrics/history are persisted.
   `evaluate.py` must not unlock the Test Set unless the trained BERT artifact passes the completeness check (and completion marker if implemented).
4. Keep the baseline model guard unchanged except for any shared helper refactor needed.
5. Do not load, split, print, or inspect Test labels/predictions while implementing or smoke-checking this guard.

### B. Add explicit BERT Validation artifact paths

Add development/validation paths in `src/config.py`, separate from final-Test paths:
- `artifacts/metrics/bert_validation_metrics.json`
- `artifacts/figures/bert_val_confusion_matrix.png`

Do not reuse `bert_test_metrics.json`, `BERT_METRICS_PATH`, or any final-Test filename for validation results.

### C. Preflight the fixed training configuration

Before the real run, verify without touching the Test Set:
- `torch.cuda.is_available()` and the actual device selected;
- GPU name and total VRAM if CUDA is available;
- installed PyTorch and Transformers versions;
- `TrainingArguments` accepts the arguments used by the project;
- `Trainer` construction remains compatible with `processing_class` in the installed version;
- Train/Validation split remains 13,821 / 1,975 with seed 42 while Test reporting stays sealed.

The official configuration remains fixed from the already-reviewed design:
- model: `google-bert/bert-base-uncased`
- MAX_LENGTH: 128
- epochs: 3
- learning rate: 2e-5
- weight decay: 0.01
- warmup ratio: 0.1
- train batch size: 16
- seed: 42
- checkpoint selection metric: Validation Macro F1

Do not tune these values in response to the Baseline Validation score or intermediate BERT Validation scores.

If the official run fails because of CUDA OOM or an environment/runtime incompatibility, do not silently change the experiment configuration and do not fabricate a replacement result. Record the exact failure in `docs/REVIEW_REQUEST.md`, mark the request as blocked, and stop so the next review can make a grounded resource/configuration decision.

### D. Run the real BERT fine-tuning phase

After A-C pass, run exactly:

`python -m src.train_bert`

Requirements:
1. Train on Train only.
2. Use Validation only for per-epoch evaluation and best-checkpoint selection.
3. Never instantiate/use Test examples for predictions or metrics during this command.
4. Keep `load_best_model_at_end=True` and save the actually selected best model/tokenizer to the local ignored BERT model directory.
5. Persist the real `trainer.state.log_history` / training history already implemented.
6. Record actual training duration.
7. If CUDA is used, also record actual GPU name and peak allocated/reserved CUDA memory if reasonably available from PyTorch. These are measurements, not estimates.

### E. Evaluate the selected BERT checkpoint on Validation only

After training has completed and the best checkpoint is loaded, evaluate/predict once on the Validation dataset and persist `bert_validation_metrics.json` with at minimum:
- `model_name`;
- `evaluation_split: validation`;
- Validation sample count;
- Accuracy;
- Macro Precision;
- Macro Recall;
- Macro F1;
- Weighted F1;
- per-class Precision / Recall / F1;
- Validation inference time;
- confusion matrix;
- best Validation metric / selected best checkpoint information;
- training configuration actually used;
- training time;
- device/GPU information actually observed.

Save `bert_val_confusion_matrix.png` from the same predictions.

The confusion-matrix total must equal 1,975.

### F. Validate training-history provenance

`artifacts/metrics/bert_training_history.json` must reflect real Trainer logs, not hand-entered values. Verify:
- train-loss points exist;
- validation-loss points exist for the evaluation epochs;
- Validation Accuracy and Macro F1 correspond to Trainer evaluation logs;
- best-model/checkpoint information is internally consistent with the configured `metric_for_best_model`;
- `artifacts/figures/training_history.png` is generated from those real logs.

If a claimed curve/metric is not present in Trainer logs, change the report/slide claim instead of synthesizing it.

### G. Preserve Test-set sealing and artifact integrity

Before completion, explicitly confirm that this phase did NOT create or modify final-Test outputs:
- `artifacts/metrics/baseline_test_metrics.json`
- `artifacts/metrics/bert_test_metrics.json`
- `artifacts/metrics/comparative_metrics.json`
- `artifacts/metrics/error_cases.json`
- `artifacts/figures/baseline_test_confusion_matrix.png`
- `artifacts/figures/bert_test_confusion_matrix.png`

Do NOT run `python -m src.evaluate`.

Do NOT generate the final PowerPoint.

### H. Update documentation as Validation-only development evidence

Update only the relevant project/report/presentation source files to reflect the real BERT Validation run. Keep the distinction explicit:
- Baseline Validation = development result;
- BERT Validation = development result;
- final comparative Test result = still pending.

It is acceptable to report a same-Validation-split delta between BERT and Baseline as a development observation, but do not convert it into the final research conclusion and do not alter BERT hyperparameters based on it.

Do not claim Test performance, final superiority, or final error patterns yet.

## Verification criteria

Before completion, verify all of the following:

- the final evaluator cannot unlock merely because an empty `bert_best_model/` directory exists;
- the BERT artifact completeness guard checks real saved model/tokenizer content;
- root-level BERT imports and TrainingArguments/Trainer API preflight pass;
- Train/Validation remain 13,821 / 1,975 with Test reporting sealed;
- `python -m src.train_bert` completes successfully with the fixed reviewed configuration;
- best checkpoint selection is based only on Validation Macro F1;
- `bert_validation_metrics.json` contains real measured Validation values and its confusion matrix sums to 1,975;
- `bert_training_history.json` contains real train/eval logs;
- `training_history.png` and `bert_val_confusion_matrix.png` are derived from those real run artifacts;
- the saved BERT model/tokenizer exists locally and remains Git-ignored;
- no final Test metric, error-analysis, or final-Test confusion-matrix artifact is generated or changed;
- docs and presentation source label all new BERT numbers as Validation/development results.

## Completion protocol

When done successfully:
1. Review the generated BERT Validation JSON, training-history JSON, and figures for internal consistency.
2. Commit tracked source/docs/real Validation artifacts with exactly:
   `experiment: fine-tune BERT with validation-only evaluation`
3. Push to `main`.
4. Obtain the exact implementation SHA with `git rev-parse HEAD` after that implementation commit is created and pushed.
5. Create/update `docs/REVIEW_REQUEST.md` containing:
   - `request_commit_sha: <exact implementation SHA>`
   - `status: READY_FOR_REVIEW`
   - summary of the BERT artifact-guard hardening
   - exact runtime/device preflight results
   - exact BERT Validation metrics copied from the generated JSON
   - training time and Validation inference time
   - best checkpoint / best Validation Macro F1
   - training-history consistency check
   - confusion-matrix consistency check
   - measured GPU peak memory if CUDA was used and the value was captured
   - confirmation that the local BERT model/tokenizer exists and is Git-ignored
   - confirmation that final Test artifacts remain absent/unchanged
   - verification commands actually run
   - files/artifacts changed
   - known issues/blockers
   - proposed next phase
6. Commit/push the review request if needed.
7. Stop and wait for the next NEXT_TASK.

If the real BERT run is blocked by OOM or an environment/runtime error, do not invent results or change experimental hyperparameters silently. Record the exact blocker and evidence in `docs/REVIEW_REQUEST.md`, push that request, and stop.