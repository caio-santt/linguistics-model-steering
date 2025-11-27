# Análise 01: Perfis Estilísticos Autorais

Esta pasta contém a primeira análise exploratória da pasta `analysis2/`: caracterização dos estilos linguísticos dos 4 autores através dos textos originais.

## 📂 Estrutura

```
01_estilo_autoral/
├── scripts/          # Scripts Python de análise
├── plots/            # Visualizações geradas
├── dados/            # Dados processados (CSVs)
├── docs/             # Documentação e interpretações
└── README.md         # Este arquivo
```

## 📊 Análises Realizadas

### 1. **Perfis Autorais com PCA** (`01_author_profiles_exploratory.py`)
- Análise exploratória usando 65 métricas filtradas
- PCA com 2 componentes (42.82% da variância)
- Identificação das 10 métricas mais discriminativas
- **Outputs:**
  - `pca_author_styles.png` - Scatter plot PC1 vs PC2
  - `author_profiles_heatmap.png` - Heatmap dos perfis
  - `discriminative_metrics.csv` - Ranking de métricas
  - `pca_loadings.csv` - Loadings de PC1 e PC2

### 2. **Componentes Adicionais** (`explore_additional_dimensions.py`)
- Exploração de PC3, PC4, PC5
- Análise estatística (ANOVA) de todas as métricas
- Identificação de métricas individuais interpretáveis
- **Outputs:**
  - `pca_additional_components.png` - Visualizações de PC3 e PC4
  - `pca_loadings_5components.csv` - Loadings de 5 componentes
  - `metrics_statistical_significance.csv` - ANOVA para todas as métricas

### 3. **Análise Detalhada do PC3** (`analyze_pc3.py`)
- Interpretação de PC3 (Repetição vs. Diversidade)
- Análise de como cada autor se comporta nesta dimensão
- **Outputs:**
  - `pc3_detailed_analysis.png` - 4 gráficos sobre PC3

### 4. **Métricas Individuais Interpretáveis** (`visualize_top3_metrics.py`)
- Visualizações das 3 métricas mais interpretáveis:
  1. Tamanho de frases (η²=0.589)
  2. Riqueza vocabular - TTR (η²=0.282)
  3. Densidade de pronomes (η²=0.810)
- **Outputs:**
  - `top3_interpretable_metrics.png` - Grid 3×3 completo
  - `top3_relative_differences.png` - Comparações relativas
  - `top3_correlations.png` - Correlações entre métricas
  - `top3_metrics_summary.csv` - Tabela resumo

## 🎯 Principais Descobertas

### **Componentes Principais**

#### PC1 (24.07%): Complexidade Sintática
- **Alto:** Estruturas complexas, subordinação, encaixamento (Woolf)
- **Baixo:** Estruturas simples, coordenação (Lispector)

#### PC2 (18.76%): Verbal vs. Nominal
- **Alto:** Foco em verbos e ações (Lispector)
- **Baixo:** Foco em substantivos e descrições (Wikipedia)

#### PC3 (9.42%): Repetição vs. Diversidade
- **Alto:** Cada frase única, sem fórmulas (Lispector +2.02)
- **Baixo:** Repetição de padrões estruturais (Woolf -1.32, Wikipedia EN -1.36)

### **Métricas Individuais Mais Discriminativas**

1. **Densidade de preposições** (η²=0.867)
2. **Proporção de orações principais** (η²=0.841)
3. **Densidade de pronomes** (η²=0.810)
4. **Modificadores adverbiais** (η²=0.800)
5. **Modificadores nominais** (η²=0.777)

### **Perfis dos Autores**

| Autor | PC1 | PC2 | PC3 | Característica Principal |
|-------|-----|-----|-----|--------------------------|
| **Lispector** | Baixo | Alto | +2.02 | Frases curtas (11 palavras), simples, únicas |
| **Woolf** | Alto | Alto | -1.32 | Frases longas (23 palavras), complexas, pronomes |
| **Wikipedia PT** | Médio | Baixo | +0.67 | Frases muito longas (34 palavras), nominais |
| **Wikipedia EN** | Médio | Baixo | -1.36 | Frases longas (30 palavras), fórmulas fixas |

### **Diferenças Quantitativas Extremas**

- **Tamanho de frases:** Wikipedia PT (34.4) vs Lispector (11.1) = **3.09×**
- **Densidade de pronomes:** Woolf (0.121) vs Wikipedia PT (0.019) = **6.22×**
- **Diversidade (PC3):** Lispector (+2.02) vs Wikipedia EN (-1.36) = **3.38 pontos**

## 📖 Documentação Completa

### `docs/INTERPRETACAO_PERFIS_AUTORAIS.md`
Documento principal com:
- Interpretação linguística detalhada dos PCs
- Explicação das métricas-chave
- Perfis quantitativos e qualitativos de cada autor
- Análise completa de PC3
- Síntese discursiva (narrativa + técnica)

### `docs/RESUMO_COMPONENTES.md`
Referência rápida:
- Tabela resumo dos PCs
- Ranking dos autores em cada dimensão
- Recomendações de uso

## 🔄 Próximos Passos

Esta análise caracterizou os **estilos originais** dos autores. As próximas análises na pasta `analysis2/` devem:

1. **Comparar textos gerados vs. originais**
   - Projetar textos gerados no espaço PCA dos originais
   - Medir distâncias e preservação de características

2. **Avaliar métodos de steering**
   - Qual método melhor preserva PC1, PC2, PC3?
   - Quais métricas individuais são preservadas/degradadas?

3. **Análise temporal**
   - Evolução das métricas ao longo da geração
   - Decay de características estilísticas

---

**Data:** Novembro 2025  
**Corpus:** 60 textos originais (15 por autor)  
**Métricas:** 65 filtradas (8 léxicas + 57 sintáticas)
