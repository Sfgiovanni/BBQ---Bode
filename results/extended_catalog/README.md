# BR-BBQ estendido — resultados consolidados

Pacote autocontido com os **seis modelos** avaliados no catálogo estendido
(`questions/categories_bilingual_extended.yaml`, 51 pares), para servir de base à
escrita do paper.

O run do BODE no catálogo **base** (27 pares, 19.440 avaliações) está
deliberadamente **fora** deste pacote. Misturar catálogos numa mesma tabela é a
forma mais fácil de publicar um número errado — se precisar dele, ele continua em
`bode_repo/results/runs/20260710_000126_*`.

---

## Mapa

```
results/extended_catalog/
├── README.md                     este arquivo
├── metrics/                      métricas consolidadas (formato longo, coluna `model`)
│   ├── overall.csv                    4 linhas — uma por modelo
│   ├── by_language.csv                pt / en
│   ├── by_context.csv                 ambíguo / desambiguado
│   ├── by_language_context.csv        cruzamento dos dois
│   ├── by_category.csv                9 categorias
│   ├── by_category_language.csv       categoria × idioma
│   ├── by_group.csv                   por grupo social
│   ├── by_scenario.csv                por cenário
│   ├── by_question_type.csv           negativa / não-negativa
│   ├── by_unknown_position.csv        por posição da alternativa "não sei"
│   ├── by_unknown_position_language.csv
│   ├── by_aggregation_language.csv
│   ├── paired_overall.csv             diferenças PT−EN e concordância
│   ├── paired_by_category.csv
│   ├── pt_en_transition.csv           matriz de transição de conteúdo PT→EN
│   ├── bootstrap_ci.csv               IC 95% de cada métrica, com flag excludes_zero
│   └── positional_stability.csv       ← métrica adicional, ver abaixo
├── predictions/README.md         aponta para results/runs/*/raw_predictions.parquet
│                                 (36.720 × 69 colunas por modelo)
└── provenance/
    ├── models.csv                     modelo, adapter, prompt, revisão, tokens
    ├── dataset_integrity.json         prova de que os 4 viram os mesmos itens
    └── <modelo>__<arquivo>            config, metadata, runtime, git state
```

**O arquivo de referência é `results/runs/<run_id>/raw_predictions.parquet`.** Todo o resto é derivado dele.
Se você discordar de alguma métrica, dá para recalcular sem reexecutar nada.

---

## Desenho experimental

| | |
|---|---|
| catálogo | 9 categorias × 30 cenários × 51 pares de grupos |
| condições | ambíguo/desambiguado × pergunta negativa/não-negativa |
| idiomas | pt-br e en, **escritos**, não traduzidos em tempo de execução |
| rotações | 3 permutações de A/B/C por questão lógica |
| totais | 6.120 pares semânticos · 12.240 questões lógicas · **36.720 avaliações por modelo** |
| scoring | log-probabilidade do **primeiro token** sobre A/B/C, `logsumexp` sobre variantes |
| amostragem | desativada, temperatura 0 |
| bootstrap | 1.000 amostras agrupadas por `semantic_pair_id` |

As três rotações são o que permite separar preferência real de resposta posicional:

| rotação | A | B | C |
|---:|---|---|---|
| 0 | grupo 1 | grupo 2 | não sei |
| 1 | não sei | grupo 1 | grupo 2 |
| 2 | grupo 2 | não sei | grupo 1 |

---

## Modelos

| modelo | identificador | prompt | scoring | pesos |
|---|---|---|---|---|
| `bode-7b` | `recogna-nlp/bode-7b-alpaca-pt-br-no-peft` | **alpaca** | logprob local (fp16) | locais, commit `ff1ecd8e` |
| `mistral-7b` | `mistralai/Mistral-7B-Instruct-v0.3` | chat_template | logprob local (**4-bit NF4**) | locais |
| `qwen2.5-7b` | `Qwen/Qwen2.5-7B-Instruct` | chat_template | logprob local (**4-bit NF4**) | locais |
| `sabiazinho-4` | `sabiazinho-4` (Maritaca) | simple | logprob via API | remotos, sem revisão fixável |
| `sabia-4` | `sabia-4` (Maritaca) | simple | logprob via API | remotos, sem revisão fixável |
| `gpt-4o` | `gpt-4o` (OpenAI) | simple | logprob via Batch API | remotos, sem revisão fixável |

Tokens médios de entrada: 196,9 (Bode, tokenizer Llama + preâmbulo Alpaca),
151,7 (Mistral) e 145,8 (Qwen), ambos com seu chat template, 117,7 (Sabiás), 114,0 (gpt-4o).

Três modelos locais e gratuitos (Bode, Mistral, Qwen — todos 7 B) contra três
servidos por API e pagos (Sabiás, gpt-4o). Mistral e Qwen são os **controles de
tamanho**: mesmo porte do Bode, sem especialização em português, de famílias
diferentes — para que "7 B não-brasileiro competente" não dependa de um único
fornecedor.

---

## Integridade

`provenance/dataset_integrity.json` registra que os seis runs avaliaram itens
**idênticos** — mesmos `example_id`, condições, rotações, gabaritos e **mesmo texto
de contexto, pergunta e alternativas**, conferido por SHA-256. O build aborta se
isso deixar de valer.

Consequência: qualquer diferença nas métricas é atribuível aos modelos — com uma
exceção documentada abaixo (o formato de prompt do Bode).

---

## Métricas

### As três do BBQ original (Parrish et al., 2022)

```
acurácia            proporção de acertos, reportada geral e por condição

s_DIS = 2 × (n_enviesadas / n_não_UNKNOWN) − 1        # contexto desambiguado
s_AMB = (1 − acurácia_ambígua) × s(ambíguos)          # contexto ambíguo
```

"Enviesada" é a alternativa que reflete o estereótipo configurado: em pergunta
negativa, o grupo estereotipado; em não-negativa, o outro grupo. Respostas
"não sei" **não entram no denominador**.

Leitura: `s = 0` é ausência de viés · `s = +1` é viés máximo na direção do
estereótipo · `s < 0` é viés na direção contrária, que costuma indicar
sobrecorreção e não neutralidade.

### O que o BR-BBQ acrescenta

| métrica | o que mede |
|---|---|
| `position_consistency` | fração de questões lógicas com o mesmo conteúdo escolhido nas 3 rotações |
| `flip_rate` | `1 − position_consistency` |
| `rate_A` / `rate_B` / `rate_C` | preferência bruta por letra |
| `unknown_rate` por `unknown_position` | se a abstenção depende de **onde** o "não sei" está |
| `semantic_agreement` | fração de pares PT/EN com a mesma resposta semântica |
| `semantic_change_rate` | `1 − semantic_agreement` |
| `*_diff_pt_minus_en` | diferença pareada de cada métrica entre idiomas |
| `pt_en_transition` | matriz de para onde a resposta migra ao trocar de idioma |
| IC 95% | bootstrap agrupado por `semantic_pair_id` |

### O que foi acrescentado aqui — `positional_stability.csv`

`s_DIS` e `s_AMB` recalculados **apenas nas questões posicionalmente estáveis**
(aquelas em que o modelo escolhe o mesmo conteúdo nas três rotações).

Não faz parte do conjunto de métricas do framework: é calculado a partir do
parquet pelo `scripts/build_paper_package.py`. Colunas: `model`, `scope`
(`all` / `stable_only`), `language` (`all` / `pt` / `en`), `frac_stable`, `n_logical`,
`accuracy`, `accuracy_ambiguous`, `accuracy_disambiguated`, `s_DIS`, `s_AMB`.

**Por que importa:** um modelo que responde por posição gera ruído que puxa o
escore de viés em direção a zero. Reportar só o número agregado subestima o viés
do Bode por um fator de 2,6 — ver resultados abaixo. Um revisor que fizer esse
recorte vai encontrar isso.

---

## Resultados principais

| métrica | bode-7b | mistral-7b | qwen2.5-7b | sabiazinho-4 | sabia-4 | gpt-4o |
|---|---:|---:|---:|---:|---:|---:|
| acurácia geral | 0,401 | 0,866 | 0,973 | 0,977 | 0,996 | **0,997** |
| acurácia · ambíguo | 0,028 | 0,747 | 0,955 | 0,980 | 0,998 | 0,998 |
| acurácia · desambiguado | 0,775 | 0,984 | 0,991 | 0,973 | 0,993 | **0,995** |
| taxa de "não sei" | 4,9% | 37,8% | 48,2% | 50,4% | 50,3% | 50,1% |
| `s_DIS` | +0,056 | +0,005 | +0,005 | −0,004 | +0,001 | +0,003 |
| `s_AMB` | +0,026 | +0,001 | **+0,030** | +0,008 | −0,000 | −0,001 |
| `position_consistency` | 0,368 | 0,749 | 0,941 | 0,960 | 0,992 | **0,995** |
| taxa A / B / C | 0,21/0,46/0,33 | 0,37/0,31/0,32 | 0,35/0,34/0,32 | 0,34/0,33/0,34 | 0,33/0,33/0,33 | 0,33/0,33/0,33 |
| `semantic_agreement` PT↔EN | 0,725 | 0,842 | 0,967 | 0,963 | 0,994 | **0,995** |

**7 B não é a limitação.** Os três modelos de 7 B vão de 0,401 a 0,973 de
acurácia e de 0,368 a 0,941 de consistência posicional. A contagem de parâmetros
não explica nada; a receita de fine-tune explica tudo.

**Instabilidade posicional e viés social são eixos independentes.** É o achado
metodológico central, e só aparece com os três modelos locais lado a lado:

| modelo | estável? | enviesado? | assinatura |
|---|---|---|---|
| `bode-7b` | não (0,368) | **sim** — 4 ICs excluem zero | posicional **e** estereotípico |
| `mistral-7b` | não (0,749) | **não** — nenhum IC exclui zero | posicional, **não** estereotípico |
| `qwen2.5-7b` | sim (0,941) | **sim** — `s_AMB` nos dois idiomas | estereotípico, **não** posicional |

Um modelo pode ser instável sem ser enviesado (Mistral puxa para a letra A —
inclusive escolhendo "não sei" 45,4% das vezes quando ela está em A contra
33,8% em B — mas essa preferência não é estereotípica), enviesado sem ser instável (Qwen), ou os dois (Bode).
Segue-se que um `s_DIS` baixo **não** é evidência de neutralidade até você
verificar de qual dos dois ele vem — que é exatamente o que
`positional_stability.csv` permite fazer.

**Capacidade não elimina viés.** O Qwen tem o maior `s_AMB` dos seis (+0,030),
com intervalos que excluem zero nos dois idiomas — mais que os dois Sabiás. Ele
abstém menos em contexto ambíguo (0,955 contra 0,998 do sabia-4) e, quando
chuta, chuta na direção do estereótipo. O eixo que separa os modelos aqui é
**abstenção calibrada**, não nacionalidade.

### `s_DIS` restrito a questões estáveis

| modelo | % estáveis | `s_DIS` todas | `s_DIS` estáveis |
|---|---:|---:|---:|
| bode-7b | 36,8% | +0,056 | **+0,144** |
| mistral-7b | 74,9% | +0,005 | +0,004 |
| qwen2.5-7b | 94,1% | +0,005 | +0,000 |
| sabiazinho-4 | 96,0% | −0,004 | −0,011 |
| sabia-4 | 99,2% | +0,001 | −0,006 |
| gpt-4o | 99,5% | +0,003 | −0,001 |

O viés do Qwen é **exclusivamente** de contexto ambíguo: restrito às questões
estáveis, o `s_DIS` dele vai a zero. Ele não erra a favor do estereótipo quando o
contexto dá a resposta — erra quando não dá.

### Intervalos que excluem zero (IC 95%)

| modelo | métricas |
|---|---|
| `bode-7b` | **todas as quatro** — `s_DIS` pt [+0,007; +0,071] e en [+0,035; +0,109]; `s_AMB` pt [+0,017; +0,048] e en [+0,001; +0,038] |
| `mistral-7b` | nenhuma — apesar de 25% de instabilidade posicional |
| `qwen2.5-7b` | `s_AMB` **nos dois idiomas** — pt [+0,033; +0,046] e en [+0,017; +0,026] |
| `sabiazinho-4` | `s_AMB` en [+0,008; +0,018] |
| `sabia-4` | nenhuma |
| `gpt-4o` | `s_AMB` pt [−0,003; −0,000] — negativo e de magnitude desprezível |

### Abstenção por posição do "não sei"

| modelo | em A | em B | em C |
|---|---:|---:|---:|
| bode-7b | **0,003** | **0,129** | **0,015** |
| mistral-7b | 0,454 | 0,338 | 0,341 |
| qwen2.5-7b | 0,505 | 0,486 | 0,453 |
| sabiazinho-4 | 0,508 | 0,495 | 0,507 |
| sabia-4 | 0,504 | 0,501 | 0,503 |
| gpt-4o | 0,503 | 0,501 | 0,501 |

---

## Ressalvas — ler antes de escrever

1. **O formato do prompt é um confundidor para o Bode, e só para ele.** Bode usa
   Alpaca; os outros três usam `simple`. A instrução e o corpo são idênticos —
   muda o invólucro da família do modelo. A afirmação defensável é *"o Bode, no
   formato Alpaca em que foi avaliado, responde por posição"*. As comparações
   **entre** sabiazinho-4, sabia-4 e gpt-4o não têm esse problema. Um run
   adicional do Bode com `prompt_style: simple` fecharia a lacuna.

2. **As direções de estereótipo não foram validadas.** O catálogo marca
   `needs_human_validation: true` em todos os pares adicionados, e o run estendido
   do Bode foi publicado como *pending methodological review*. Os resultados são
   computacionalmente válidos e reprodutíveis; o **sinal** de cada escore herda
   esse status. O padrão de classe do Bode é robusto o bastante para não depender
   disso; categorias individuais, não.

3. **O repositório não rodava como publicado.** A regra `*token*` do `.gitignore`
   impediu que `src/brbbq/scoring/tokens.py` fosse commitado. O módulo foi
   reconstruído a partir da especificação do `METHODOLOGY.md` e está marcado como
   reconstrução. **Um rerun do BODE com essa versão é reconstrução, não reprodução**
   do run de julho — pedir o arquivo original ao autor antes de qualquer rerun.

4. **Qwen e Mistral rodaram quantizados em 4-bit (NF4)**, porque 7 B em fp16 passam de 14 GB
   contra 11,3 GB de VRAM disponíveis. A quantização perturba os logits sobre os
   quais o benchmark tira `argmax`: os números do Qwen são comparáveis entre si e
   aos demais dentro da margem esperada, mas uma comparação estrita com o run
   fp16 do Bode carrega essa diferença. `configs/models/qwen25_7b.yaml` registra
   os parâmetros exatos.

5. **Modelos hospedados não têm SHA de revisão.** O Bode fixa o commit dos pesos;
   Sabiás e gpt-4o só podem fixar a data de execução (4 set 2026). Se o provedor
   trocar os pesos, os números deixam de ser reproduzíveis.

6. **Truncamento de `top_logprobs` nas APIs.** O teto é 20. Diagnóstico por linha
   nas colunas `letters_found` / `letters_missing`: as três letras estavam presentes
   em **100%** das linhas do gpt-4o e em 73.439 de 73.440 dos Sabiás. Não afetou
   nenhum resultado, mas a coluna existe para que isso seja verificável.

7. **Teto do benchmark.** Quatro dos seis modelos passam de 0,97 de acurácia. Um
   instrumento onde os concorrentes empatam no topo tem pouca resolução — a
   conclusão "especialização em português não produz vantagem mensurável" vale
   para **este** benchmark, com este nível de dificuldade.

8. **`music_preference` é exploratória** e o próprio catálogo a exclui de
   interpretação demográfica protegida.

9. **Divergência entre documentação e código:** o config estendido usa
   `cluster_key: semantic_pair_id`, enquanto o `METHODOLOGY.md` descreve bootstrap
   sobre `semantic_block_id`. Os ICs aqui seguem o **config**, para serem
   comparáveis ao run publicado do Bode.

---

## Reconstruir o pacote

```bash
PYTHONPATH=src python3 scripts/build_paper_package.py
# --copy-predictions para um pacote autocontido, fora do repositorio
```

Lê os runs publicados e reescreve o pacote; nunca o contrário. Aborta se os
quatro runs deixarem de avaliar itens idênticos.

---

*Documentação em português por conveniência de escrita; o restante do repositório
está em inglês. Peça a tradução se for publicar o pacote junto do código.*
