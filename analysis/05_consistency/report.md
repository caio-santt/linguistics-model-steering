# Análise de Consistência Intra-Método

## Dados
- Arquivo: `metrics_filtered/all_texts_filtered.csv`
- N samples: 180 (cada sample com 3 repetições)
- N métodos: 3 (baseline, prompt_steering, activation_steering)
- N métricas: 65

## Método
Para cada sample, calcular coeficiente de variação (CV = std/mean) entre as 3 repetições. CV baixo indica consistência (gerações similares), CV alto indica variabilidade (gerações divergentes). Teste de Kruskal-Wallis para comparar CV entre métodos.

## Resultados

### 1. Consistência Global por Método

| Método | N Samples | CV Médio | Desvio Padrão | Min CV | Max CV |
|--------|-----------|----------|---------------|--------|--------|
| baseline | 60 | 0.1977 | 0.1264 | 0.0306 | 0.6711 |
| prompt_steering | 60 | 0.3420 | 0.1396 | 0.0685 | 0.6496 |
| activation_steering | 60 | 0.1893 | 0.1151 | 0.0283 | 0.5843 |


**Método mais consistente:** activation_steering (CV = 0.1893)

**Teste de Kruskal-Wallis:** H = 99.137, p = 0.0000

**Interpretação:** Diferença significativa na consistência entre métodos (p < 0.05).


### 2. Métricas Mais Variáveis

**Métricas com maior CV (média entre métodos):**

- `n_repeated_trigrams`: CV = 0.6350
- `DEPREL_appos_prop`: CV = 0.4865
- `UPOS_SCONJ_prop`: CV = 0.4554
- `DEPREL_cop_prop`: CV = 0.4403
- `DEPREL_acl_prop`: CV = 0.4341
- `DEPREL_xcomp_prop`: CV = 0.4276
- `DEPREL_advcl_prop`: CV = 0.4018
- `DEPREL_mark_prop`: CV = 0.3923
- `DEPREL_acl_md`: CV = 0.3847
- `UPOS_PROPN_prop`: CV = 0.3777


## Interpretação Técnica

Activation steering é mais consistente: manipulação direta de representações internas produz outputs mais previsíveis. Prompt steering e baseline dependem mais de sampling estocástico. CV alto em métricas sintáticas específicas (subordinação, modificação) indica que essas estruturas são menos controláveis mesmo com steering.


## Interpretação Simplificada

Consistência mede se o método gera textos parecidos quando executado várias vezes com o mesmo input. Baixo CV = método confiável e previsível. Alto CV = método instável, cada geração é muito diferente. Métodos consistentes são preferíveis para aplicações que requerem reprodutibilidade (ex: geração de resumos, tradução automática).

## Implicações Linguísticas

Consistência baixa em métricas léxicas (TTR, n-gramas) é esperada e desejável (variação superficial mantendo conteúdo). Consistência baixa em métricas sintáticas profundas (subordinação, modificação) é problemática: sugere que steering não controla totalmente estrutura gramatical, apenas aspectos superficiais. Ideal: **alta consistência em sintaxe + variação controlada em léxico**. Métodos que atingem esse equilíbrio demonstram controle fino sobre geração.
