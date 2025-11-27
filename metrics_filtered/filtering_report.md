# Filtragem de Métricas

## Dados
- Arquivo original: `metrics/full_text/individual/all_texts.csv`
- Métricas iniciais: 230
- Métricas finais: 65
- **Redução: 165 métricas (71.7%)**

## Método
Aplicação sequencial de filtros para remover métricas problemáticas.

## Resultados

### Pipeline de Filtragem

| Filtro | Critério | N Removidas | N Restantes |
|--------|----------|-------------|-------------|
| Inicial | - | - | 230 |
| 1 | NaN ≥ 20% | 126 | 104 |
| 2 | Variância = 0 | 4 | 100 |
| 3 | Contagens absolutas | 31 | 69 |
| 4 | Correlação \|r\| ≥ 0.95 | 8 | 65 |

### Métricas Finais por Categoria

**Léxicas básicas:**

- N = 8
  - `basic_ttr`
  - `basic_tokens_per_sentence_mean`
  - `basic_chars_per_token_mean`
  - `basic_n_unique_unigrams`
  - `basic_n_unique_bigrams`
  - `basic_n_repeated_bigrams`
  - `basic_n_unique_trigrams`
  - `basic_n_repeated_trigrams`

**Sintáticas globais:**
- N = 1
  - `synt_mean_dependency_distance`

**DEPREL (relações de dependência):**
- N = 37
- Principais: `det`, `nmod`, `obj`, `amod`, `nsubj`, `mark`, `acl`, `advmod`, `obl`, `advcl`

**UPOS (part-of-speech):**
- N = 19
- Principais: `NOUN`, `VERB`, `ADJ`, `ADV`, `ADP`, `DET`, `PRON`, `CCONJ`, `SCONJ`

## Interpretação Técnica

Redução de 230 para 65 métricas (28.3% retidos). Priorizadas métricas normalizadas (proporções), linguisticamente interpretáveis (UPOS/DEPREL principais), e com dados completos (<20% NaN). Redundâncias resolvidas mantendo medidas mais diretas (proporções > distâncias, DEPREL > UPOS quando correlacionados).

## Interpretação Simplificada

Eliminamos mais da metade das métricas porque eram redundantes, vazias, ou mediam construções raríssimas. Mantivemos apenas as medidas essenciais e interpretáveis que realmente caracterizam estilo: diversidade vocabular, comprimento de sentenças, tipos de palavras (substantivos, verbos, etc.), e relações sintáticas principais (sujeito, objeto, modificadores).

## Implicações Linguísticas

O conjunto final equilibra **cobertura** (captura múltiplas dimensões estilísticas) e **interpretabilidade** (todas as métricas têm significado linguístico claro). Léxicas capturam superficie textual (vocabulário, tamanho). UPOS capturam classes gramaticais (densidade nominal/verbal). DEPREL capturam estrutura sintática (subordinação, modificação). MDD captura complexidade global. Juntas, formam perfil estilométrico abrangente.
