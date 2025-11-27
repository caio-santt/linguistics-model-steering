# 📊 Análise: Baseline vs Original

## 🎯 Objetivo
Comparar textos gerados com **prompt bruto (baseline)** aos textos **originais** dos autores, identificando como a geração sem steering afeta as características estilísticas.

## 📁 Estrutura de Dados
- **Original**: 60 textos (15 por autor)
- **Baseline**: 180 textos (45 por autor)
  - Estrutura: 3 samples × 3 repetições × 15 textos = 45 por autor
  - Design balanceado para robustez estatística

---

## 🔍 Descobertas Principais

### 1. **Baseline como Regularizador Estilístico**

O modelo LLM atua como um **"regularizador estilístico"**, empurrando estilos extremos em direção ao centro:

#### 📏 **Comprimento de Sentença**
| Autor | Original | Baseline | Mudança | Interpretação |
|-------|----------|----------|---------|---------------|
| **Lispector** | 11.14 palavras | 25.59 palavras | **+129.7%** | Perdeu simplicidade distintiva |
| **Woolf** | 23.13 palavras | 27.71 palavras | +19.8% | Aumentou ligeiramente |
| **Wikipedia PT** | 24.36 palavras | 26.73 palavras | +9.7% | Mudança mínima |
| **Wikipedia EN** | 27.37 palavras | 27.09 palavras | -1.0% | Praticamente estável |

**💡 Insight**: Lispector tinha o estilo **mais distinto** (sentenças curtas). O baseline a **homogeneizou**, aproximando-a dos demais.

---

#### 🗣️ **Densidade Pronominal (PRON)**
| Autor | Original | Baseline | Mudança | Interpretação |
|-------|----------|----------|---------|---------------|
| **Woolf** | 0.121 | 0.095 | **-21.1%** | Perdeu intensidade pronominal |
| **Wikipedia EN** | 0.076 | 0.062 | -18.4% | Reduziu uso de pronomes |
| **Lispector** | 0.067 | 0.099 | **+48.1%** | Aumentou dramaticamente |
| **Wikipedia PT** | 0.057 | 0.067 | +17.5% | Aumento moderado |

**Amplitude entre extremos**:
- Original: 6.22× (Woolf/Wikipedia PT)
- Baseline: 4.61× (Woolf/Lispector)

**💡 Insight**: O baseline **reduziu a diferenciação** entre autores, convergindo para um uso pronominal intermediário.

---

### 2. **Deslocamento no Espaço PCA**

Treinamos um PCA nos textos **originais** e projetamos os textos **baseline** no mesmo espaço:

#### 🎯 **Variância Explicada**
- **PC1** (Complexidade Sintática): 24.07%
- **PC2** (Verbal vs Nominal): 18.76%
- **PC3** (Diversidade Textual): 9.42%
- **Total (3 PCs)**: 52.25%

#### 📐 **Distâncias de Deslocamento**
| Autor | Distância Total | Interpretação |
|-------|-----------------|---------------|
| **Woolf** | **4.39** | Maior deslocamento - estilo muito afetado |
| **Wikipedia EN** | 1.68 | Deslocamento moderado |
| **Lispector** | 1.65 | Deslocamento moderado |
| **Wikipedia PT** | 0.93 | Menor deslocamento - estilo mais preservado |

**💡 Insight**: Autores com estilos **mais complexos** (Woolf) foram os **mais afetados** pelo baseline.

---

### 3. **Decomposição Dimensional do Deslocamento**

#### 🔬 **Componentes do Movimento**

| Autor | ΔPC1 (Complexidade) | ΔPC2 (Verbal/Nominal) | Componente Dominante |
|-------|---------------------|----------------------|---------------------|
| **Woolf** | **-4.23** (96.3% do total) | -1.18 | **PC1**: Simplificação massiva |
| **Wikipedia EN** | -1.10 | **-1.27** (75.5%) | **PC2**: Nominalização |
| **Lispector** | **+1.07** ✅ | -1.25 (76.1%) | **PC2**: Nominalização |
| **Wikipedia PT** | -0.40 | **+0.84** ✅ (90.1%) | **PC2**: Verbalização (única!) |

#### 📊 **Padrões Identificados**

**A. Direção das Mudanças**:
- **Simplificação** (PC1 ↓): 3/4 autores (Woolf, Wikipedia EN, Wikipedia PT)
- **Complexificação** (PC1 ↑): 1/4 autor (**Lispector** - única!)
- **Nominalização** (PC2 ↓): 3/4 autores (Woolf, Wikipedia EN, Lispector)
- **Verbalização** (PC2 ↑): 1/4 autor (**Wikipedia PT** - única!)

**B. Interpretações**:

🔴 **WOOLF**:
- **-4.23 em PC1**: Perdeu drasticamente complexidade sintática
- **96.3% da mudança foi em complexidade**
- Ficou mais simples E mais nominal
- **Maior impacto de todos os autores**

🟢 **LISPECTOR** (comportamento oposto!):
- **+1.07 em PC1**: GANHOU complexidade (única!)
- Partiu de muito simples (11 palavras/sentença) → baseline adicionou complexidade
- Mas perdeu verbalidade (-1.25), como os demais

🔵 **WIKIPEDIA PT**:
- **+0.84 em PC2**: GANHOU verbalidade (única!)
- Menor deslocamento total (0.93)
- Baseline preservou relativamente bem suas características

🟡 **WIKIPEDIA EN**:
- Mudanças equilibradas em ambas dimensões
- Simplificação + Nominalização moderadas

---

### 4. **Perda de Diversidade (PC3)**

**Todos os autores** se moveram negativamente em PC3 (Diversidade):

| Autor | PC3 Original | PC3 Baseline | ΔPC3 | Interpretação |
|-------|--------------|--------------|------|---------------|
| **Woolf** | -1.32 | -3.83 | **-2.51** | Mais repetitivo |
| **Wikipedia EN** | -1.36 | -3.71 | **-2.35** | Mais repetitivo |
| **Lispector** | +2.02 | +0.59 | **-1.43** | Perdeu originalidade |
| **Wikipedia PT** | +0.67 | +0.00 | **-0.66** | Convergiu para neutro |

**💡 Insight**: Baseline **reduz originalidade** e **aumenta padrões repetitivos** em TODOS os autores.

---

### 5. **Reversão de Padrões de N-gramas**

Descobrimos um padrão **oposto** entre autores únicos e repetitivos:

#### 📈 **Trigramas Repetidos**
| Autor | Original | Baseline | Mudança |
|-------|----------|----------|---------|
| **Lispector** | 15 | 41 | **+167%** ⬆️ |
| **Woolf** | 87 | 28 | **-68%** ⬇️ |
| **Wikipedia EN** | 205 | 33 | **-84%** ⬇️ |

#### 📊 **Bigramas Repetidos**
| Autor | Original | Baseline | Mudança |
|-------|----------|----------|---------|
| **Lispector** | 82 | 130 | **+58%** ⬆️ |
| **Woolf** | 210 | 120 | **-43%** ⬇️ |
| **Wikipedia EN** | 360 | 109 | **-70%** ⬇️ |

**💡 Insight Chave**: 
- **Lispector** (única): Aumentou repetições → modelo adicionou padrões
- **Woolf & Wikipedia**: Reduziram repetições → modelo diversificou

**Hipótese**: O modelo possui um **"ponto de equilíbrio"** para repetições:
- Autores **muito únicos** → modelo adiciona repetições (convergência)
- Autores **muito formulaicos** → modelo remove repetições (convergência)
- **Resultado**: Todos convergem para o centro

---

## 🎨 Visualizações Criadas

### 1. `01_key_metrics_comparison.png`
- Comparação de 3 métricas interpretáveis
- Barras com erro padrão
- Destaca mudanças percentuais

### 2. `02_pca_movement.png`
- Scatter plot: textos individuais no espaço PCA
- Setas de deslocamento: centro original → centro baseline
- Quantificação de distâncias

### 3. `03_displacement_decomposition.png`
- **Esquerda**: Barras empilhadas (componentes PC1 + PC2)
- **Direita**: Barras horizontais (direção com sinais)
- Mostra contribuição de cada dimensão

### 4. `04_displacement_profiles.png`
- **Esquerda**: Vetores no espaço (ΔPC1 × ΔPC2)
- **Direita**: Radar chart (magnitude das mudanças)
- Identifica clusters de comportamento

---

## 📊 Dados Exportados

1. **`metric_changes.csv`**: Mudanças percentuais nas métricas-chave
2. **`pca_movement.csv`**: Coordenadas PCA e distâncias
3. **`displacement_decomposition.csv`**: Decomposição dimensional completa

---

## 🧠 Conclusões

### ✅ Hipótese Validada: **Baseline = Regularizador Estilístico**

1. **Convergência para o Centro**: 
   - Estilos extremos (Lispector, Woolf) são puxados para valores intermediários
   - Redução de diferenciação entre autores

2. **Perda de Complexidade (maioria)**:
   - 3/4 autores simplificaram sintaticamente
   - Exceção: Lispector ganhou complexidade (partiu de muito simples)

3. **Tendência à Nominalização**:
   - 3/4 autores reduziram verbalidade
   - Exceção: Wikipedia PT aumentou verbalidade

4. **Redução Universal de Diversidade**:
   - PC3 negativo para TODOS
   - Baseline aumenta repetições ou reduz originalidade

5. **Reversão de N-gramas**:
   - Autores únicos → mais repetitivos
   - Autores formulaicos → menos repetitivos
   - **Evidência de "ponto de equilíbrio" do modelo**

---

## 🚀 Próximos Passos

1. **Comparar com Prompt Steering**: O steering consciente preserva melhor o estilo?
2. **Comparar com Activation Steering**: Intervenção nos activations é mais eficaz?
3. **Métricas Sintáticas Específicas**: Analisar dependências e estruturas arbóreas
4. **Análise Temporal**: Mudanças ocorrem no início ou fim da geração?
5. **Efeito do Sample**: Diferentes seed texts produzem padrões diferentes?

---

## 📝 Metodologia

- **Abordagem**: Incremental, levantando hipóteses e respondendo individualmente
- **Ferramentas**: Python (pandas, sklearn, matplotlib, seaborn)
- **PCA**: Treinado em originais, baseline projetado no mesmo espaço
- **Estatísticas**: Médias, desvios padrão, coeficientes de variação
- **Visualizações**: 4 plots com múltiplas perspectivas dos dados
