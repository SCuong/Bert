# NEXT TASK

task_id: overnight-002
reviewed_commit_sha: 0a47a1ea9f131da41d014457e5dc815ff89e4726
status: READY

## Goal

Run the real data audit + token-length EDA only, use those measurements to make the MAX_LENGTH decision, and update documentation with measured data facts. Do not train any model yet.

## Reviewer decision on overnight-001

The pre-experiment runtime/methodology fixes are accepted with one important refinement for this phase:

- Data integrity audit may describe the full supplied dataset.
- Any hyperparameter choice that could influence training, especially MAX_LENGTH, must be based on training/validation data only, not on the held-out Test Set.
- Do not use Test Set text distribution to choose 128 vs 256.

## Required work

1. Run the real data audit on the teacher-provided dataset using:
   `python -m src.data`

2. Before using token-length statistics to choose MAX_LENGTH, ensure the implementation computes selection statistics from:
   - Train + Validation only, or
   - Train only.
   
   Prefer Train + Validation for descriptive preprocessing analysis if no labels/predictions from Test are used, but document the scope explicitly.

   The held-out Test Set must not influence the MAX_LENGTH decision.

3. Produce and persist real audit statistics, including at minimum:
   - raw row count;
   - missing text count;
   - missing label count;
   - empty-after-clean count;
   - conflicting-label row count and unique conflicting texts;
   - exact duplicate rows removed;
   - final unique valid sample count;
   - final class distribution;
   - exact Train / Validation / Test counts after stratified split;
   - explicit zero-overlap verification result.

4. Produce and persist BERT token-length statistics using `google-bert/bert-base-uncased` tokenizer for the allowed selection scope:
   - mean;
   - median;
   - p90;
   - p95;
   - p99;
   - max;
   - percentage longer than 128 tokens;
   - percentage longer than 256 tokens.

5. Save the results in machine-readable artifacts. Reuse `artifacts/metrics/token_length_stats.json` and, if useful, add:
   - `artifacts/metrics/data_audit.json`

6. Save EDA figures, at minimum:
   - class distribution;
   - token-length distribution with 128 and 256 cutoffs.

7. Decide MAX_LENGTH = 128 or 256 from the measured statistics and the practical 8 GB VRAM constraint.

   The decision must be explained in a short evidence-based note:
   - truncation tradeoff;
   - expected memory/compute cost;
   - why the chosen value is appropriate for this course project.

8. Update `src/config.py` only after the real measurements support the decision.

9. Update documentation with only measured facts:
   - `README.md`
   - `data/README.md`
   - `FINAL_REPORT.md`
   - `docs/02_project_spec.md`
   - `docs/PRE_EXPERIMENT_REVIEW.md`
   - presentation source/outline/notes where EDA facts or MAX_LENGTH are mentioned.

10. Keep the project in PRE-BASELINE state. Do NOT run:
    - TF-IDF baseline training;
    - BERT fine-tuning;
    - final Test Set model evaluation;
    - final PowerPoint generation.

11. Do not convert descriptive EDA into conclusions about model quality.

## Verification criteria

Before completion, verify:
- `python -m src.data` completes successfully on the real dataset;
- artifacts contain real measured values rather than placeholders;
- token-length selection statistics clearly state their scope (Train or Train+Val);
- Test Set was not used to choose MAX_LENGTH;
- `src/config.py` MAX_LENGTH matches the documented EDA decision;
- no baseline/BERT model artifacts or evaluation metrics were created;
- documentation numbers match the JSON artifacts exactly.

## Completion protocol

When done:
1. Review the generated JSON and figures.
2. Run only non-training consistency checks.
3. Commit the EDA/config/docs changes with:
   `data: run audited EDA and select sequence length`
4. Push to `main`.
5. Create/update `docs/REVIEW_REQUEST.md` containing:
   - request_commit_sha: the new pushed implementation commit SHA
   - status: READY_FOR_REVIEW
   - exact data-audit results
   - token-length statistics
   - chosen MAX_LENGTH and rationale
   - files/artifacts changed
   - verification commands actually run
   - known issues/blockers
   - proposed next phase
6. Commit/push the review request if needed.
7. Stop and wait for the next NEXT_TASK.
