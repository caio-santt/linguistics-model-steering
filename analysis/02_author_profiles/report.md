# Perfis Estilísticos dos Autores Originais

## Dados
- Arquivo: `metrics_filtered/original_filtered.csv`
- N textos: 60
- N autores: 4
- N métricas: 65

## Método
Cálculo de estatísticas descritivas (média ± desvio padrão) por autor. Seleção das 10 métricas mais discriminativas (maior variação entre autores) para visualização em radar charts.

## Resultados

### Distribuição de Textos por Autor

- **wikipedia_pt** (pt): 15 textos
- **woolf** (eng): 15 textos
- **wikipedia_eng** (eng): 15 textos
- **lispector** (pt): 15 textos

### Características Distintivas por Autor

#### wikipedia_pt (prosa enciclopédica)

**Estilo esperado:** expositiva, formal, informativa

**Métricas elevadas** (>20% acima da média geral):
- `DEPREL_appos_prop`: 2.06× a média
- `DEPREL_nmod_prop`: 1.82× a média
- `UPOS_PROPN_prop`: 1.67× a média
- `DEPREL_acl_prop`: 1.62× a média
- `UPOS_ADP_prop`: 1.46× a média

**Métricas reduzidas** (<20% abaixo da média geral):
- `UPOS_PRON_prop`: 0.32× a média
- `UPOS_SCONJ_prop`: 0.46× a média
- `DEPREL_advmod_prop`: 0.46× a média
- `DEPREL_cop_prop`: 0.50× a média
- `UPOS_AUX_prop`: 0.56× a média

#### woolf (prosa literária)

**Estilo esperado:** modernista, psicológica, fluxo de consciência

**Métricas elevadas** (>20% acima da média geral):
- `UPOS_PRON_prop`: 2.00× a média
- `DEPREL_nsubj_prop`: 1.64× a média
- `mean_dependency_distance`: 1.44× a média
- `DEPREL_advmod_prop`: 1.44× a média
- `DEPREL_advcl_prop`: 1.36× a média

**Métricas reduzidas** (<20% abaixo da média geral):
- `DEPREL_appos_prop`: 0.45× a média
- `DEPREL_nmod_prop`: 0.52× a média
- `DEPREL_root_prop`: 0.55× a média
- `DEPREL_acl_prop`: 0.60× a média
- `UPOS_PROPN_prop`: 0.60× a média

#### wikipedia_eng (prosa enciclopédica)

**Estilo esperado:** expositiva, formal, informativa

**Métricas elevadas** (>20% acima da média geral):
- `DEPREL_amod_prop`: 1.58× a média
- `tokens_per_sentence_mean`: 1.21× a média
- `UPOS_NOUN_prop`: 1.20× a média

**Métricas reduzidas** (<20% abaixo da média geral):
- `DEPREL_root_prop`: 0.53× a média
- `UPOS_PRON_prop`: 0.57× a média
- `DEPREL_advmod_prop`: 0.64× a média
- `DEPREL_cop_prop`: 0.73× a média
- `DEPREL_det_prop`: 0.79× a média

#### lispector (prosa literária)

**Estilo esperado:** introspectiva, fragmentada, stream of consciousness

**Métricas elevadas** (>20% acima da média geral):
- `DEPREL_root_prop`: 2.17× a média
- `DEPREL_cop_prop`: 1.57× a média
- `DEPREL_advmod_prop`: 1.46× a média
- `UPOS_SCONJ_prop`: 1.43× a média
- `DEPREL_obj_prop`: 1.29× a média

**Métricas reduzidas** (<20% abaixo da média geral):
- `tokens_per_sentence_mean`: 0.45× a média
- `DEPREL_amod_prop`: 0.56× a média
- `DEPREL_appos_prop`: 0.57× a média
- `UPOS_PROPN_prop`: 0.57× a média
- `n_repeated_trigrams`: 0.58× a média


## Interpretação Técnica

Autores literários (Lispector, Woolf) apresentam maior densidade pronominal e subordinação complexa (MDD elevado), refletindo narrativa introspectiva. Autores enciclopédicos (Wikipedia PT/EN) mostram maior densidade nominal e adjetival, característico de texto expositivo-descritivo. A variabilidade intra-autor é maior em textos literários (CV alto em métricas sintáticas), indicando versatilidade estilística vs. uniformidade enciclopédica.

## Interpretação Simplificada

Cada autor tem uma "assinatura" estilística única. Lispector e Woolf usam mais pronomes e frases complexas (estilo literário introspectivo). Wikipedia usa mais substantivos e adjetivos (estilo informativo-descritivo). É como comparar poesia (variada, pessoal) com manual técnico (uniforme, objetivo).

## Implicações Linguísticas

Perfis confirmam distinção entre **prosa literária** (alta subordinação, densidade pronominal, variabilidade sintática) e **prosa enciclopédica** (nominalização, modificação adjetival, uniformidade estrutural). Diferenças entre Lispector (PT) e Woolf (EN) refletem não apenas língua, mas também período histórico e escola literária (modernismo brasileiro vs. inglês). Métricas quantitativas capturam conceitos qualitativos bem estabelecidos na estilística literária.
