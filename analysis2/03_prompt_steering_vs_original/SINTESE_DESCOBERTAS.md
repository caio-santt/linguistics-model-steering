# 📊 Análise: Prompt Steering vs Original

## 🎯 Objetivo
Comparar textos gerados com **prompt steering** (instruções explícitas sobre estilo) aos textos **originais** dos autores, identificando se o steering consciente preserva ou transforma características estilísticas.

## 📁 Estrutura de Dados
- **Original**: 60 textos (15 por autor)
- **Prompt Steering**: 180 textos (45 por autor)
  - Estrutura: 3 samples × 3 repetições × 15 textos = 45 por autor
  - Design idêntico ao baseline

---

## 🔍 Descobertas Principais

### 1. **Prompt Steering ≠ Baseline: Efeitos Opostos**

#### 📏 **Comprimento de Sentença**
| Autor | Original | Prompt Steering | Mudança | Interpretação |
|-------|----------|-----------------|---------|---------------|
| **Wikipedia EN** | 29.63 palavras | 82.31 palavras | **+177.8%** | Explosão de complexidade |
| **Woolf** | 23.13 palavras | 58.03 palavras | **+150.9%** | Mais que dobrou |
| **Lispector** | 11.14 palavras | 6.65 palavras | **-40.3%** | Mais simples ainda |
| **Wikipedia PT** | 34.39 palavras | 8.05 palavras | **-76.6%** | Dramaticamente reduzida |

**💡 Insight**: 
- **Baseline** homogeneizou (~26 palavras para todos)
- **Prompt Steering** criou **divergência extrema**: 6.65 a 82.31 palavras!
- Lispector e Wikipedia PT ficaram **mais curtas**
- Woolf e Wikipedia EN ficaram **muito mais longas**

**⚠️ CONTRASTE COM BASELINE:**
- Baseline: Lispector +129% (convergência)
- Prompt: Lispector -40% (divergência)

---

#### 🗣️ **Densidade Pronominal (PRON)**
| Autor | Original | Prompt Steering | Mudança | Interpretação |
|-------|----------|-----------------|---------|---------------|
| **Wikipedia PT** | 0.019 | 0.084 | **+330.9%** | Ganhou intensidade pronominal |
| **Wikipedia EN** | 0.034 | 0.129 | **+278.0%** | Muito mais pronomes |
| **Woolf** | 0.121 | 0.137 | +13.3% | Leve aumento |
| **Lispector** | 0.067 | NaN | - | Dados ausentes |

**Amplitude entre extremos**:
- Original: 6.36× (Woolf/Wikipedia PT)
- Prompt Steering: 1.63× (Woolf/Wikipedia PT)

**💡 Insight**: 
- **Baseline** reduziu diferenciação (6.22× → 4.61×)
- **Prompt Steering** reduziu AINDA MAIS (6.36× → 1.63×)
- Wikipedias aumentaram drasticamente uso pronominal
- Convergência mais forte que no baseline!

---

#### 📖 **Riqueza Vocabular (TTR)**
| Autor | Original | Prompt Steering | Mudança | Interpretação |
|-------|----------|-----------------|---------|---------------|
| **Lispector** | 0.512 | 0.308 | **-39.8%** | Vocabulário mais repetitivo |
| **Wikipedia EN** | 0.486 | 0.322 | **-33.7%** | Menos diverso |
| **Woolf** | 0.461 | 0.318 | **-31.1%** | Vocabulário empobrecido |
| **Wikipedia PT** | 0.515 | 0.425 | -17.4% | Menor perda |

**💡 Insight**: TODOS perderam riqueza vocabular com prompt steering, sugerindo que as instruções criaram vocabulário mais formulaico.

---

### 2. **Deslocamento no Espaço PCA**

#### 📐 **Distâncias de Deslocamento**
| Autor | Distância Total | vs Baseline | Interpretação |
|-------|-----------------|-------------|---------------|
| **Wikipedia PT** | **6.53** | +598% | Maior deslocamento de todos! |
| **Wikipedia EN** | **5.39** | +221% | Extremamente afetado |
| **Woolf** | 2.68 | -39% | MENOS afetado que no baseline |
| **Lispector** | 2.35 | +43% | Mais afetado que no baseline |

**⚠️ CONTRASTE DRAMÁTICO COM BASELINE:**
- **Wikipedias**: Baseline teve menor impacto (0.93-1.68), Prompt teve MAIOR impacto (5.39-6.53)
- **Woolf**: Baseline teve maior impacto (4.39), Prompt teve menor impacto (2.68)
- **Inversão de padrão!**

---

### 3. **Decomposição Dimensional do Deslocamento**

#### 🔬 **Componentes do Movimento**

| Autor | ΔPC1 (Complexidade) | ΔPC2 (Verbal/Nominal) | Componente Dominante |
|-------|---------------------|----------------------|---------------------|
| **Wikipedia PT** | +0.20 (3.1%) | **+6.52** (100.0%) | **PC2**: Verbalização massiva |
| **Wikipedia EN** | **+5.39** (100.0%) | +0.03 (0.6%) | **PC1**: Complexificação pura |
| **Woolf** | +0.52 (19.2%) | **-2.63** (98.1%) | **PC2**: Nominalização |
| **Lispector** | **+2.25** (95.5%) | -0.69 (29.5%) | **PC1**: Complexificação |

#### 📊 **Padrões Identificados**

**A. Direção das Mudanças**:
- **Simplificação** (PC1 ↓): **0/4 autores** ⚠️
- **Complexificação** (PC1 ↑): **4/4 autores** ✅
- **Nominalização** (PC2 ↓): 2/4 autores (Woolf, Lispector)
- **Verbalização** (PC2 ↑): 2/4 autores (Wikipedias)

**🔥 CONTRASTE COM BASELINE:**
- Baseline: 3/4 simplificaram, 1/4 complexificou
- Prompt: 0/4 simplificaram, 4/4 complexificaram
- **PADRÃO OPOSTO COMPLETO!**

**B. Interpretações Detalhadas**:

🟡 **WIKIPEDIA PT** (maior mudança):
- **+6.52 em PC2**: Transformação radical de nominal → verbal
- Praticamente 100% da mudança foi em verbalidade
- Distância 6.53 é a **maior de todas as análises**
- Mudou de -4.50 para +2.03 em PC2 (swing de 6.53!)

🟢 **WIKIPEDIA EN**:
- **+5.39 em PC1**: Ganhou muita complexidade sintática
- Praticamente 100% da mudança foi em complexidade
- De 0.09 para +5.48 em PC1
- Segunda maior distância total

🔵 **WOOLF**:
- **-2.63 em PC2**: Ficou mais nominal
- 98.1% da mudança em PC2
- No baseline perdeu -4.23 em PC1, aqui só -0.52
- **Prompt steering preservou melhor a complexidade de Woolf!**

🔴 **LISPECTOR**:
- **+2.25 em PC1**: Complexificou mais que no baseline (+1.07)
- 95.5% da mudança em complexidade
- Prompt steering intensificou o efeito de complexificação

---

### 4. **Clusters de Comportamento**

**Quadrante 1 (↗ Mais Complexo + Mais Verbal):**
- Wikipedia PT (+0.20, +6.52) - dominância verbal
- Wikipedia EN (+5.39, +0.03) - dominância complexidade

**Quadrante 4 (↘ Mais Complexo + Mais Nominal):**
- Woolf (+0.52, -2.63) - dominância nominal
- Lispector (+2.25, -0.69) - dominância complexidade

**💡 Padrão**: Prompt steering cria **dois grupos divergentes**:
- **Wikipedias**: Ambas ganham verbalidade, ficam parecidas
- **Autoras literárias**: Ambas perdem verbalidade, ficam mais nominais

---

## 🆚 Comparação: Baseline vs Prompt Steering

| Aspecto | Baseline | Prompt Steering |
|---------|----------|-----------------|
| **Complexidade** | 3/4 simplificam | **4/4 complexificam** |
| **Padrão PC1** | Convergência para centro | **Todos positivos** |
| **Impacto Woolf** | Maior (4.39) | Menor (2.68) |
| **Impacto Wikipedias** | Menor (0.93-1.68) | **Maior (5.39-6.53)** |
| **Comprimento sentença** | Homogeneização (~26) | **Divergência (6-82)** |
| **Densidade pronominal** | Convergência 4.61× | Convergência 1.63× (mais forte) |
| **TTR** | Variável | **Todos perdem** |
| **PC2 (Verbal/Nominal)** | 3/4 nominalizam | **Dividido 2/2** |

---

## 🧠 Conclusões

### ✅ Descobertas Chave

1. **Prompt Steering ≠ Regularizador**:
   - Baseline empurrava para o centro
   - Prompt steering cria **DIVERGÊNCIA** em algumas dimensões
   - Mas **CONVERGÊNCIA** em outras (pronomes)

2. **Complexificação Universal**:
   - TODOS os autores ganham complexidade sintática (PC1 positivo)
   - Oposto completo do baseline (3/4 perderam)
   - Instruções explícitas parecem "forçar" sintaxe mais elaborada

3. **Wikipedias Mais Afetadas**:
   - No baseline: menor impacto
   - No prompt steering: maior impacto
   - Especialmente Wikipedia PT: +6.53 unidades!
   - Sugestão: textos enciclopédicos mais "maleáveis" a instruções?

4. **Woolf Melhor Preservada**:
   - Baseline destruiu complexidade (-4.23)
   - Prompt steering preservou melhor (+0.52)
   - Menor distância total (2.68 vs 4.39)
   - Instruções ajudaram a manter características literárias?

5. **Lispector Intensificada**:
   - Baseline: +1.07 em PC1
   - Prompt: +2.25 em PC1
   - Prompt steering **amplificou** efeito de complexificação
   - Textos curtos + instruções = sintaxe mais elaborada?

6. **Verbalização Split**:
   - Wikipedias: +6.52 e +0.03 (mais verbais)
   - Autoras: -2.63 e -0.69 (mais nominais)
   - Prompt steering criou **dois clusters distintos**

7. **Empobrecimento Vocabular**:
   - Todos perdem TTR (-17% a -40%)
   - Instruções criam vocabulário mais formulaico?
   - Trade-off: complexidade sintática × diversidade lexical?

---

## 🎨 Visualizações Criadas

1. **`01_key_metrics_comparison.png`**: Comparação de métricas interpretáveis
2. **`02_pca_movement.png`**: Movimento no espaço PCA com componentes
3. **`03_displacement_decomposition.png`**: Decomposição dimensional
4. **`04_displacement_profiles.png`**: Vetores de mudança e radar chart

---

## 📊 Dados Exportados

1. **`metric_changes.csv`**: Mudanças nas 3 métricas-chave
2. **`pca_movement.csv`**: Coordenadas e distâncias no PCA
3. **`displacement_decomposition.csv`**: Decomposição PC1 vs PC2

---

## 🚀 Próximos Passos

1. **Comparar Activation Steering**: Intervenção nos activations será diferente?
2. **Análise Comparativa 3-Way**: Baseline vs Prompt vs Activation
3. **Investigar Causa da Verbalização**: Por que Wikipedias verbalizaram?
4. **Análise de Vocabulário**: Quais palavras mudaram?
5. **Métricas Sintáticas Específicas**: Profundidade de árvores, tipos de cláusulas?

---

## 💡 Hipóteses Emergentes

1. **Instruções Explícitas Forçam Complexidade**: Todos ganham PC1 positivo
2. **Textos Enciclopédicos São Mais Maleáveis**: Wikipedias sofrem maior impacto
3. **Trade-off Sintaxe-Léxico**: Complexidade sintática às custas de vocabulário
4. **Clustering por Gênero**: Wikipedias vs Autoras literárias reagem diferente
5. **Prompt Steering Melhor para Autores Complexos**: Woolf preservada, Wikipedias distorcidas
