# Resumo Rápido: Componentes Principais e Métricas-Chave

## 📊 Componentes Principais (PCA)

### ✅ **PC1 (24.07%): Complexidade Sintática**
**O que separa:** Estruturas simples ↔ Estruturas complexas

**Métricas principais:**
- Distâncias de dependência (`_md`)
- Distância média geral, distância dos verbos, substantivos

**Interpretação prática:**
- **Alto (→):** Frases longas, subordinação, encaixamento (Woolf)
- **Baixo (←):** Frases curtas, coordenação, estrutura simples (Lispector)

---

### ✅ **PC2 (18.76%): Verbal vs. Nominal**
**O que separa:** Foco em ações ↔ Foco em entidades/descrições

**Métricas principais:**
- `VERB_prop` (+) - Densidade de verbos
- `tokens_per_sentence` (-) - Tamanho de frases
- `nmod_prop` (-) - Modificadores nominais
- `appos_prop` (-) - Aposições

**Interpretação prática:**
- **Alto (↑):** Muitos verbos, frases curtas, dinâmico (Lispector)
- **Baixo (↓):** Muitos substantivos, frases longas, descritivo (Wikipedia)

---

### ✅ **PC3 (9.42%): Repetição vs. Diversidade**
**O que separa:** Textos formulaicos ↔ Textos variados

**Métricas principais:**
- `n_unique_bigrams` (+) - Combinações únicas
- `n_repeated_bigrams` (-) - Combinações repetidas
- `ttr` (+) - Riqueza vocabular

**Interpretação prática:**
- **Alto (+2.0):** Cada frase construída de forma única, sem fórmulas (Lispector)
- **Médio (+0.7):** Variabilidade moderada (Wikipedia PT)
- **Baixo (-1.3):** Repetição de padrões estruturais (Woolf, Wikipedia EN)

**Ranking dos autores:**
1. **Lispector (+2.02)** - Máxima diversidade (450 bigramas únicos / 82 repetidos = 5.47×)
2. **Wikipedia PT (+0.67)** - Diversidade moderada-alta
3. **Woolf (-1.32)** - Repetição moderada (fluxo de consciência = fórmulas recorrentes)
4. **Wikipedia EN (-1.36)** - Máxima repetição (fórmulas enciclopédicas fixas)

**PC3 vs TTR:**
- TTR mede repetição de **palavras individuais**
- PC3 mede repetição de **combinações** (bigramas/trigramas)
- Wikipedia EN: TTR médio mas PC3 baixo = usa palavras variadas mas sempre nas mesmas fórmulas

**Status:** ✅ Interpretável E discriminativo! Revela dimensão independente de PC1-PC2

---

### ❌ **PC4 (8.33%) e PC5 (6.18%): Pouco Interpretáveis**

**PC4:** Mistura tamanho textual + densidade de determinantes (interpretação difusa)

**PC5:** Subordinação complexa (similar a PC1, mas mais específico)

**Conclusão:** PC1-PC2 são suficientes. PC3 útil para análises específicas. PC4-PC5 não adicionam interpretabilidade clara.

---

## 🎯 Métricas Individuais Altamente Discriminativas

### Top 3 Métricas Mais Fáceis de Interpretar

| # | Métrica | η² | O que mede | Ranking |
|---|---------|-----|------------|---------|
| 1 | **Tamanho de Frases** | 0.589 | Palavras por frase | Wiki PT (34) > Wiki EN (30) > Woolf (23) > **Lispector (11)** |
| 2 | **Riqueza Vocabular (TTR)** | 0.282 | Proporção palavras únicas | Wiki PT (0.52) > Lispector (0.51) > Wiki EN (0.49) > **Woolf (0.46)** |
| 3 | **Densidade de Pronomes** | 0.810 | Proporção de pronomes | **Woolf** muito alta, demais baixo |

### Outras Métricas com Grande Effect Size (η² > 0.7)

- **Densidade de preposições** (0.867) - "de", "em", "para"
- **Proporção de orações principais** (0.841) - Quantas frases independentes
- **Modificadores adverbiais** (0.800) - Como verbos são modificados
- **Tamanho de palavras** (0.777) - Complexidade lexical
- **Modificadores nominais** (0.777) - Como substantivos são especificados

---

## 📍 Posicionamento dos Autores no Espaço Estilístico

```
PC2 (Verbal/Dinâmico)
        ↑
        |
   LISPECTOR         PC1 alto
        |            PC2 médio/alto
        |            (Complexa + Verbal)
←───────┼───────────────→ PC1 (Complexidade)
        |               WOOLF
   WIKI PT              
   WIKI EN         
        |
        ↓
PC2 (Nominal/Descritivo)
```

### Quadrantes:

**Superior Esquerdo (Lispector):**
- Estrutura simples (PC1 baixo)
- Estilo verbal (PC2 alto)
- Frases muito curtas (11 palavras)

**Superior Direito (Woolf):**
- Estrutura complexa (PC1 alto)
- Estilo verbal/pronominal (PC2 médio/alto)
- Muitos pronomes, subordinação

**Inferior Central (Wikipedias):**
- Estrutura mediana (PC1 médio)
- Estilo nominal (PC2 baixo)
- Frases muito longas (30-34 palavras)
- Muitas aposições e modificadores nominais

---

## 💡 Insights-Chave para Apresentação

1. **Estilo é estrutural, não lexical:** 9 de 10 métricas mais discriminativas são sintáticas

2. **2 dimensões capturam 43% da variação:** PC1 (complexidade) + PC2 (verbal vs. nominal)

3. **Tamanho de frase sozinho separa bem os autores:** De 11 palavras (Lispector) a 34 palavras (Wikipedia PT)

4. **Cada autor ocupa região distinta no espaço PCA:** Não há sobreposição significativa

5. **Métricas individuais são mais comunicáveis que PCs:** Para apresentações, usar "frases curtas vs. longas" é mais claro que "PC1 baixo vs. alto"

---

## 🔄 Recomendações de Uso

### Para Visualizações:
- **Use PC1 vs PC2** - Mais informativos e interpretáveis
- PC3 apenas se houver análise específica sobre repetição estilística
- Evite PC4-PC5 - Interpretação difusa

### Para Explicações Verbais:
- **Prefira métricas individuais:** "Lispector usa frases de 11 palavras em média, enquanto Wikipedia usa 34"
- PCs são úteis para visualização, mas difíceis de explicar em palavras

### Para Análise Técnica:
- Use todas as dimensões (PC1-PC5) para capturar 67% da variância
- Mas mantenha foco em PC1-PC2 para interpretação

---

## 📁 Arquivos Gerados

- `pca_author_styles.png` - Visualização PC1 vs PC2
- `pca_additional_components.png` - Visualização PC3 e PC4
- `pca_loadings_5components.csv` - Loadings de todos os PCs
- `metrics_statistical_significance.csv` - ANOVA para todas as métricas
- `significant_interpretable_metrics.csv` - Métricas interpretáveis significativas
- `author_profiles_heatmap.png` - Perfis das 10 métricas mais discriminativas

---

**Variância Total Explicada:**
- PC1-PC2: 42.82%
- PC1-PC3: 52.25%
- PC1-PC5: 66.77%
