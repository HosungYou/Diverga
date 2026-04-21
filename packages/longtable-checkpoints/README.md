# @longtable/checkpoints

Checkpoint policy and runtime guidance engine for LongTable.

Current responsibilities:

- structural and adaptive checkpoint resolution
- natural-language checkpoint trigger classification
- runtime guidance generation by interaction mode
- closure-disposition rules for provider adapters
- question-first governance for high-ambiguity research work

Key API:

- `classifyCheckpointTrigger(prompt, options)` converts natural-language context
  into a provider-neutral `CheckpointSignal`.
- `resolveCheckpointPolicy(profile, signal)` decides whether the checkpoint is
  blocking, recommended, log-only, or inactive.
- `resolveRuntimeGuidance(profile, signal, policy)` generates ordering guidance
  for provider adapters.
