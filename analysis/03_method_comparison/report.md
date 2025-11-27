# Comparação dos Métodos de Geração vs Original

## Dados
- Arquivo: `metrics_filtered/all_texts_filtered.csv`
- N textos originais: 60
- N textos gerados: 540
- N métricas: 65

## Método
Cálculo de distância Euclidiana entre cada texto gerado e seu original correspondente no espaço de métricas normalizado (z-score). Preservation score = 1 - (distance / max_distance). Divergência por métrica = diferença relativa média |gerado - original| / |original|.

## Resultados

### 1. Distâncias Estilísticas Globais

| Método | Distância Média | Desvio Padrão | Min | Max |
|--------|----------------|---------------|-----|-----|
| baseline | 12.200 | 11.637 | 4.266 | 41.839 |
| prompt_steering | 16.130 | 17.741 | 6.895 | 42.734 |
| activation_steering | 12.124 | 11.633 | 4.559 | 42.288 |


**Interpretação:** Valores menores = maior similaridade ao original.

### 2. Preservation Scores

| Método | Preservation Score Médio |
|--------|--------------------------|
| baseline | 0.715 |
| prompt_steering | 0.623 |
| activation_steering | 0.716 |


**Interpretação:** 1.0 = preservação perfeita, 0.0 = máxima distorção.

### 3. Métricas Mais Divergentes

**Top 10 métricas com maior desvio relativo (média entre os 3 métodos):**

- `n_repeated_trigrams`: 2.259
- `DEPREL_root_prop`: 1.753
- `DEPREL_acl:relcl_prop`: 1.600
- `DEPREL_appos_prop`: 1.553
- `DEPREL_nsubj_prop`: 0.918
- `UPOS_PRON_prop`: 0.807
- `DEPREL_nmod_prop`: 0.768
- `DEPREL_acl_md`: 0.754
- `DEPREL_acl_prop`: 0.745
- `DEPREL_mark_prop`: 0.734


## Interpretação Técnica

Método com melhor preservação: **activation_steering** (score = 0.716). Distâncias absolutas são maiores que experimentos anteriores devido a: (1) maior número de métricas (65 vs 40), (2) inclusão de 3 repetições aumentando variabilidade, (3) normalização z-score mais sensível a outliers. Divergências concentram-se em métricas sintáticas específicas (subordinação, modificação) enquanto métricas léxicas básicas (TTR, tokens/sent) são melhor preservadas.

## Interpretação Simplificada

Os textos gerados por **activation_steering** são os mais parecidos com os originais. Todos os métodos conseguem imitar bem aspectos superficiais (tamanho de palavras, número de palavras por frase), mas têm mais dificuldade em replicar estruturas sintáticas complexas (tipo de subordinação, modificadores específicos). É como copiar o "formato" de um texto mas ter dificuldade em copiar a "gramática interna".

## Implicações Linguísticas

Preservação diferencial entre níveis linguísticos: **léxico > sintaxe superficial > sintaxe profunda**. TTR e comprimento sentencial são facilmente controlados pelo modelo, mas padrões de subordinação e modificação específicos (ex: `acl`, `nmod`, `advmod`) são mais difíceis de replicar, pois dependem de decisões composicionais complexas. Isso sugere que LLMs capturam bem estatísticas de primeira ordem (distribuição de palavras) mas têm dificuldade com dependências estruturais de longo alcance características de estilo autoral.
