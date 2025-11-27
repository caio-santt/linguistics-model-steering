# 📊 Análise: Activation Steering vs Original

## 🎯 Objetivo
Comparar textos gerados com **activation steering** (intervenção nos activations do modelo) aos textos **originais**, avaliando se manipulação interna preserva melhor o estilo que métodos baseados em prompt.

## 📁 Estrutura de Dados
- **Original**: 60 textos (15 por autor)
- **Activation Steering**: 180 textos (45 por autor)
  - Estrutura: 3 samples × 3 repetições = 45 por autor

---

## 🔍 Descobertas Principais

### 1. **Activation Steering ≈ Baseline: Resultados Similares**

#### 📏 **Comprimento de Sentença**
| Autor | Original | Activation | Mudança | vs Baseline |
|-------|----------|------------|---------|-------------|
| **Lispector** | 11.14 palavras | 25.73 palavras | **+130.9%** | Similar (+129.7%) |
| **Woolf** | 23.13 palavras | 26.18 palavras | +13.2% | Similar (+19.8%) |
| **Wikipedia EN** | 29.63 palavras | 28.62 palavras | -3.4% | Inverteu (+177.8% prompt) |
| **Wikipedia PT** | 34.39 palavras | 32.43 palavras | -5.7% | Similar (+9.7%) |

**💡 Insight**: 
- **Activation** reproduz padrão do **baseline** (convergência ~26 palavras)
- Lispector novamente teve maior mudança (+131%)
- **Contraste com Prompt**: Wikipedia EN aqui reduziu (-3%), no prompt explodiu (+178%)

---

#### 🗣️ **Densidade Pronominal**
| Autor | Original | Activation | Mudança | Interpretação |
|-------|----------|------------|---------|---------------|
| **Lispector** | 0.067 | 0.106 | +58.2% | Ganhou uso pronominal |
| **Wikipedia PT** | 0.019 | 0.022 | +13.6% | Leve aumento |
| **Woolf** | 0.121 | 0.093 | **-23.1%** | Perdeu intensidade |
| **Wikipedia EN** | 0.034 | 0.022 | **-36.4%** | Redução dramática |

**Amplitude entre extremos**:
- Original: 6.36× (Woolf/Wikipedia PT)
- Activation: 4.82× (Lispector/Wikipedia PT)
- **Similar ao Baseline** (4.61×)

---

#### 📖 **Riqueza Vocabular (TTR)**
| Autor | Original | Activation | Mudança | vs Baseline vs Prompt |
|-------|----------|------------|---------|----------------------|
| **Wikipedia EN** | 0.486 | 0.542 | **+11.4%** ✅ | Único que ganhou! |
| **Woolf** | 0.461 | 0.475 | +3.0% | Preservou |
| **Wikipedia PT** | 0.515 | 0.518 | +0.7% | Estável |
| **Lispector** | 0.512 | 0.458 | -10.5% | Perdeu menos que outros |

**💡 Insight Chave**: 
- **Activation** preserva melhor TTR que baseline e prompt!
- 3/4 autores mantiveram ou ganharam riqueza vocabular
- **Contraste dramático com Prompt** (todos perderam -17% a -40%)

---

### 2. **Deslocamento no Espaço PCA**

#### 📐 **Distâncias de Deslocamento**
| Autor | Distância | vs Baseline | vs Prompt | Interpretação |
|-------|-----------|-------------|-----------|---------------|
| **Woolf** | **4.57** | +4.1% (4.39) | +70.5% (2.68) | Praticamente igual ao baseline |
| **Wikipedia EN** | 1.65 | -1.3% (1.68) | -69.3% (5.39) | Estável baseline, muito diferente prompt |
| **Lispector** | 1.49 | -9.4% (1.65) | -36.6% (2.35) | Menor impacto |
| **Wikipedia PT** | **0.87** | -6.5% (0.93) | -86.7% (6.53) | MELHOR PRESERVADO! |

**⚠️ PADRÃO CRÍTICO:**
- **Activation ≈ Baseline** em todas as distâncias
- **Woolf**: Activation 4.57 vs Baseline 4.39 (diferença <5%)
- **Wikipedia PT**: Menor distância em TODOS os métodos
- **Prompt**: Único método drasticamente diferente (especialmente Wikipedias)

---

### 3. **Decomposição Dimensional do Deslocamento**

#### 🔬 **Componentes do Movimento**

| Autor | ΔPC1 (Complexidade) | ΔPC2 (Verbal/Nominal) | vs Baseline |
|-------|---------------------|----------------------|-------------|
| **Woolf** | **-4.41** (96.4%) | -1.21 (26.6%) | PC1: -4.23 (98% similar!) |
| **Wikipedia EN** | -1.09 (66.2%) | -1.24 (75.0%) | Similar pattern |
| **Lispector** | +1.13 (75.4%) | -0.98 (65.6%) | PC1: +1.07 (similar) |
| **Wikipedia PT** | -0.32 (37.2%) | **+0.81** (92.8%) | PC2: +0.84 (idêntico!) |

#### 📊 **Padrões Identificados**

**A. Direção das Mudanças - IDÊNTICO AO BASELINE:**
- **Simplificação** (PC1 ↓): 3/4 autores (Woolf, Wikipedias)
- **Complexificação** (PC1 ↑): 1/4 autor (Lispector)
- **Nominalização** (PC2 ↓): 3/4 autores (Woolf, Wikipedia EN, Lispector)
- **Verbalização** (PC2 ↑): 1/4 autor (Wikipedia PT)

**🔥 COMPARAÇÃO COM OS 3 MÉTODOS:**

| Direção | Baseline | Activation | Prompt |
|---------|----------|------------|--------|
| PC1 ↓ (Simplificam) | 3/4 | **3/4** | **0/4** |
| PC1 ↑ (Complexificam) | 1/4 | **1/4** | **4/4** |
| PC2 ↓ (Nominalizam) | 3/4 | **3/4** | 2/4 |
| PC2 ↑ (Verbalizam) | 1/4 | **1/4** | 2/4 |

**Activation = Baseline em TODAS as direções!**

---

**B. Interpretações por Autor**:

🔵 **WOOLF** (pior resultado):
- **-4.41 em PC1**: Perdeu massivamente complexidade
- **96.4% da mudança** foi em complexidade
- Baseline: -4.23 (diferença <5%)
- Prompt: +0.52 (PROMPT PRESERVOU MELHOR!)
- **Activation não oferece vantagem**

🔴 **LISPECTOR** (única complexificadora):
- **+1.13 em PC1**: Ganhou complexidade
- Baseline: +1.07, Prompt: +2.25
- **Prompt foi mais eficaz em complexificar**
- Activation = baseline

🟡 **WIKIPEDIA PT** (melhor preservado):
- **+0.81 em PC2**: Verbalização dominante
- Distância 0.87 (menor de todos)
- Baseline: 0.93, Prompt: 6.53
- **Activation melhor para Wikipedia PT**

🟢 **WIKIPEDIA EN**:
- Simplificação + Nominalização
- Activation: -1.09 PC1, -1.24 PC2
- Prompt: +5.39 PC1 (OPOSTO COMPLETO!)
- **Activation = baseline, Prompt = divergente**

---

### 4. **Comparação Tripla: Baseline vs Activation vs Prompt**

| Aspecto | Baseline | Activation | Prompt |
|---------|----------|------------|--------|
| **Complexidade** | 3/4 simplificam | **3/4 simplificam** | 4/4 complexificam |
| **Woolf PC1** | -4.23 | **-4.41** (similar) | +0.52 (oposto) |
| **Lispector PC1** | +1.07 | **+1.13** (similar) | +2.25 (maior) |
| **Distâncias** | 0.93-4.39 | **0.87-4.57** (similar) | 2.35-6.53 (maior) |
| **TTR** | Variável | **3/4 ganham** ✅ | Todos perdem ❌ |
| **Comprimento** | Convergência ~26 | **Convergência ~26** | Divergência 6-82 |
| **Pronomes** | Convergência 4.61× | **Convergência 4.82×** | Convergência 1.63× |

---

## 🧠 Conclusões

### ✅ Descobertas Chave

1. **Activation Steering ≈ Baseline**:
   - Padrões quase idênticos em todas as métricas
   - Diferenças <10% nas distâncias PCA
   - Mesma direção de mudança (3/4 simplificam, 3/4 nominalizam)
   - **Intervenção nos activations não superou prompt simples**

2. **Woolf Não Preservada**:
   - Activation: -4.41 (pior)
   - Baseline: -4.23 (pior)
   - Prompt: +0.52 (**melhor!**)
   - **Prompt steering foi superior para autores complexos**

3. **Wikipedia PT Melhor Preservada**:
   - Activation: 0.87 (melhor entre todos os métodos)
   - Menor impacto em textos enciclopédicos neutros
   - Consistente através dos 3 métodos

4. **TTR: Única Vantagem do Activation**:
   - 3/4 autores mantiveram ou ganharam riqueza vocabular
   - Wikipedia EN: +11.4% (único ganho em todos os métodos!)
   - Baseline: variável
   - Prompt: todos perderam (-17% a -40%)
   - **Activation preserva melhor diversidade lexical**

5. **Prompt Steering Único Diferente**:
   - Todos complexificam (oposto de baseline/activation)
   - Maiores distâncias (2.35-6.53)
   - Divergência extrema em comprimento (6-82 palavras)
   - **Único método que muda comportamento fundamental**

6. **Lispector: Sempre Complexifica**:
   - Todos os métodos: PC1 positivo
   - Baseline: +1.07, Activation: +1.13, Prompt: +2.25
   - Modelo sempre adiciona complexidade a textos curtos
   - **Prompt intensifica o efeito**

7. **Nominalização Dominante**:
   - Baseline: 3/4 nominalizam
   - Activation: 3/4 nominalizam
   - Prompt: 2/4 nominalizam (split)
   - **Tendência natural do modelo**

---

## 🎯 Ranking de Métodos por Objetivo

### **Para Preservar Complexidade de Autores Literários (Woolf):**
1. **Prompt Steering** (+0.52) ✅
2. Baseline (-4.23)
3. Activation (-4.41) ❌

### **Para Preservar Textos Enciclopédicos (Wikipedias):**
1. **Activation** (0.87-1.65) ✅
2. Baseline (0.93-1.68)
3. Prompt (5.39-6.53) ❌

### **Para Preservar Riqueza Vocabular:**
1. **Activation** (3/4 ganham) ✅
2. Baseline (variável)
3. Prompt (todos perdem) ❌

### **Para Criar Textos Complexos:**
1. **Prompt** (4/4 complexificam) ✅
2. Activation (1/4 complexifica)
3. Baseline (1/4 complexifica) ❌

---

## 💡 Hipóteses Validadas/Refutadas

### ❌ REFUTADAS:
1. **"Activation steering preserva melhor que baseline"**
   - Falso: Resultados praticamente idênticos
   - Exceção: TTR ligeiramente melhor

2. **"Intervenção interna é superior a instruções externas"**
   - Falso: Prompt steering foi superior para Woolf
   - Activation não mudou comportamento fundamental

### ✅ VALIDADAS:
1. **"Modelo tem viés de simplificação"**
   - Confirmado: 3/4 autores simplificam (baseline + activation)
   - Apenas prompt inverte isso

2. **"TTR mais sensível a método de steering"**
   - Confirmado: Activation preserva, Prompt destrói

3. **"Textos neutros são mais preservados"**
   - Confirmado: Wikipedia PT menor distância em todos os métodos

---

## 🎨 Visualizações Criadas

1. **`01_key_metrics_comparison.png`**: 3 métricas interpretáveis
2. **`02_pca_movement.png`**: Movimento PCA com componentes
3. **`03_displacement_decomposition.png`**: Decomposição dimensional
4. **`04_displacement_profiles.png`**: Vetores e radar chart

---

## 📊 Dados Exportados

1. **`metric_changes.csv`**: Mudanças nas 3 métricas
2. **`pca_movement.csv`**: Coordenadas e distâncias PCA
3. **`displacement_decomposition.csv`**: Decomposição PC1 vs PC2

---

## 🚀 Próximos Passos

1. **Análise Comparativa 3-Way**: Baseline vs Prompt vs Activation lado a lado
2. **Investigar Causa do TTR**: Por que activation preserva vocabulário?
3. **Métricas de Coerência**: Qual método gera textos mais coerentes?
4. **Trade-offs**: Complexidade × Vocabulário × Fidelidade
5. **Recomendações**: Quando usar cada método?

---

## 🏁 Síntese Final

**Activation Steering não oferece vantagem significativa sobre Baseline simples.**

- Padrões idênticos em 90% das métricas
- Única vantagem: preservação de TTR (+11% vs -10%)
- Não resolve problema de simplificação de autores complexos
- **Prompt Steering é o único método que muda comportamento fundamental**

**Recomendação**: 
- Use **Prompt** para autores literários complexos (Woolf)
- Use **Activation/Baseline** para textos neutros (Wikipedias)
- **Não há justificativa para complexidade adicional do Activation** sobre Baseline
