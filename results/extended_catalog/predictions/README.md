# Predições linha a linha

Não são copiadas para cá: os runs já são versionados neste repositório e
duplicá-los custaria ~10 MB sem ganho. Cada arquivo tem 36.720 linhas x 69
colunas.

| modelo | caminho |
|---|---|
| `bode-7b` | `results/runs/20260726_112145_bilingual_bode_extended_bode-7b-alpaca-pt-br-no-peft/raw_predictions.parquet` |
| `sabiazinho-4` | `results/runs/20260904_120011_bilingual_sabia_extended_sabiazinho-4/raw_predictions.parquet` |
| `sabia-4` | `results/runs/20260904_122525_bilingual_sabia_extended_sabia-4/raw_predictions.parquet` |
| `gpt-4o` | `results/runs/20260904_203401_bilingual_openai_extended_gpt-4o/raw_predictions.parquet` |

Para um pacote autocontido (compartilhável fora do repo):

```bash
python3 scripts/build_paper_package.py --copy-predictions
```
