# Model adapters

`BaseModelAdapter` isolates all model-specific behavior from dataset and
analysis code. Implementations must provide model/tokenizer loading, final
prompt rendering, device discovery, A/B/C token metadata, batched scoring,
greedy audit generation, and reproducibility metadata.

`HuggingFaceCausalLMAdapter` supports simple causal prompts and tokenizer chat
templates. `BodeAlpacaAdapter` enforces the Alpaca format expected by the first
experiment. Both use attention masks, left padding, `torch.inference_mode()`,
and a single forward pass per scoring batch.

To add a model:

1. Add a YAML file under `configs/models/`.
2. Reuse `huggingface_causal_lm` when its contract is sufficient.
3. Otherwise subclass `BaseModelAdapter` under `src/brbbq/models/` and register
   it in `src/brbbq/models/__init__.py`.
4. Run validation, unit tests, and preflight before a full experiment.

Do not put model names, credentials, or device assumptions in dataset,
metrics, or reporting modules.
