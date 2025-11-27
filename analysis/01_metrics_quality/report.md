# Análise de Qualidade das Métricas

## Dados
- Arquivo: `metrics/full_text/individual/all_texts.csv`
- N textos: 600
- N métricas: 230

## Método
Análise exploratória para identificar métricas problemáticas: valores ausentes (NaN), variância zero, e alta correlação (redundância).

## Resultados

### 1. Valores Ausentes

| Categoria | N Métricas | % do Total |
|-----------|------------|------------|
| Perfeitas (0% NaN) | 11 | 4.8% |
| Boas (<5% NaN) | 69 | 30.0% |
| Aceitáveis (5-20% NaN) | 24 | 10.4% |
| **Problemáticas (≥20% NaN)** | **126** | **54.8%** |

**Top 10 métricas com mais NaN:**

- `synt_DEPREL_count_goeswith`: 99.8% NaN
- `synt_DEPREL_goeswith_prop`: 99.8% NaN
- `synt_DEPREL_goeswith_md`: 99.8% NaN
- `synt_DEPREL_list_prop`: 99.7% NaN
- `synt_DEPREL_count_dislocated`: 99.7% NaN
- `synt_DEPREL_count_list`: 99.7% NaN
- `synt_DEPREL_dislocated_md`: 99.7% NaN
- `synt_DEPREL_dislocated_prop`: 99.7% NaN
- `synt_DEPREL_list_md`: 99.7% NaN
- `synt_DEPREL_orphan_md`: 99.3% NaN

### 2. Variância

| Categoria | N Métricas |
|-----------|------------|
| Constantes (var=0) | 4 |
| Variância muito baixa (<0.001) | 59 |

**Métricas constantes devem ser removidas** (não discriminam nada).

### 3. Correlações Altas

- **N pares com \|r\| ≥ 0.95:** 48
- Indicam redundância: métricas medem praticamente a mesma coisa

**Exemplo de pares altamente correlacionados:**

- `synt_DEPREL_total_words` ↔ `synt_UPOS_total_words`: r = 1.000
- `synt_DEPREL_punct_md` ↔ `synt_UPOS_PUNCT_md`: r = 0.999
- `synt_DEPREL_punct_prop` ↔ `synt_UPOS_PUNCT_prop`: r = 0.998
- `synt_DEPREL_count_punct` ↔ `synt_UPOS_count_PUNCT`: r = 0.998
- `synt_DEPREL_count_det` ↔ `synt_UPOS_count_DET`: r = 0.996

## Interpretação Técnica

Das 230 métricas extraídas, aproximadamente 55% apresentam algum problema de qualidade (NaN ≥20%, variância zero, ou alta redundância). Métricas com muitos valores ausentes ocorrem porque certas relações sintáticas são raras (ex: `reparandum`, `vocative`, `orphan`). Alta correlação indica que proporções e contagens da mesma relação sintática são quase perfeitamente lineares (ex: `DEPREL_det_prop` ≈ `DEPREL_count_det`).

## Interpretação Simplificada

Muitas métricas são inúteis para análise: algumas nunca aparecem nos textos (valores ausentes), outras são sempre iguais (sem variação), e várias medem a mesma coisa de formas diferentes (redundância). Precisamos filtrar para manter apenas as métricas informativas e independentes.

## Implicações Linguísticas

Relações sintáticas raras (vocativos, reparos, elipses) são pouco informativas para caracterizar estilo autoral em textos escritos formais. A redundância entre proporções e contagens é esperada matematicamente, mas apenas uma forma deve ser mantida (proporções são preferíveis por serem normalizadas pelo tamanho do texto). A filtragem deve priorizar **métricas linguisticamente interpretáveis** (UPOS, DEPREL principais, MDD) sobre artefatos de parsing.
