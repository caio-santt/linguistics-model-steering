# Linguistics and Model Steering

Análise quantitativa de preservação de estilo autoral em textos gerados por LLMs usando três técnicas de steering: baseline prompting, prompt steering com descrições estilísticas, e activation steering via manipulação de representações internas.

## 📊 Visão Geral

Este projeto investiga como diferentes métodos de controle (steering) de modelos de linguagem afetam a preservação de características estilísticas autorais em textos gerados. Analisamos 600 textos através de 65 métricas linguísticas filtradas, cobrindo dimensões léxicas e sintáticas.

**Principais achados:**
- Activation steering preserva melhor o estilo original (0.716) comparado a prompt steering (0.623)
- Baseline sofre decaimento temporal artificial (vocabulário esgota 16× mais rápido que originais)
- Activation steering é significativamente mais consistente entre gerações (CV=0.189 vs 0.342 prompt)
- Nenhum método controla completamente estruturas sintáticas profundas (subordinação, apposição)

## ⚠️ Nota Importante: Repositório Parcial

Este repositório contém **apenas a análise linguística** dos textos gerados. Os seguintes componentes **não estão incluídos** e serão adicionados futuramente:

### Ausentes no Repositório Atual:

1. **📚 Dataset Completo de Treinamento**
   - Textos literários usados para calcular vetores de steering (corpus de treinamento Lispector/Woolf)
   - Textos enciclopédicos usados como contrafactual (corpus completo Wikipedia)
   - Apenas os 60 prefixes de avaliação estão incluídos em `data/original/`

2. **🧮 Pipeline de Cálculo de Steering Vectors**
   - Código para extração de ativações da camada 12
   - Cálculo de vetores contrafactuais (literário - enciclopédico)
   - Metodologia de aplicação dos vetores durante geração
   - Scripts de geração dos 540 textos

3. **📝 Prompts de Geração** ⚠️ **CRÍTICO**
   - Prompt baseline (continuação simples)
   - **Prompt steering com descrições estilométricas detalhadas** (necessário para interpretar métricas)
   - Instruções de temperatura, top-p, e outros hiperparâmetros

**Status atual:** Repositório focado em análise downstream. Pipeline upstream será documentado em breve.

## 📁 Estrutura do Projeto

```
linguistics_and_model_steering/
├── data/                          # Textos de entrada (60 originais + 540 gerados)
│   ├── original/                  # 4 autores × 15 samples cada
│   └── generated/                 # 3 métodos × 3 repetições por sample
│
├── metrics/                       # Métricas extraídas (237 colunas)
│   ├── all_texts.csv             # Dataset principal: 600 textos
│   └── windowed/                 # Análise temporal: 2990 janelas
│
├── metrics_filtered/              # Métricas filtradas (65 colunas)
│   └── all_texts_filtered.csv    # Pós-redução dimensional
│
├── analysis/                      # 6 análises + síntese final
│   ├── 01_metrics_quality/       # Identificação de métricas problemáticas
│   ├── 02_author_profiles/       # Caracterização de estilos autorais
│   ├── 03_method_comparison/     # Comparação entre steering methods
│   ├── 04_temporal_decay/        # Análise de decaimento vocabular
│   ├── 05_consistency/           # Variabilidade intra-método
│   └── 06_synthesis/             # Síntese final e implicações linguísticas
│
└── scripts/                       # Código de extração e análise
    ├── metrics_extraction/       # Pipeline de extração (NLTK + UDPipe)
    └── analysis/                 # 7 scripts de análise dimensional
```

## 🎯 Dataset

**Autores:** 4 (2 literários + 2 enciclopédicos)
- Clarice Lispector (PT, literário)
- Virginia Woolf (EN, literário)
- Wikipedia PT (enciclopédico)
- Wikipedia EN (enciclopédico)

**Estrutura:**
- 60 textos originais (4 autores × 5 títulos × 3 samples)
- 540 textos gerados (60 samples × 3 métodos × 3 repetições)
- **Total:** 600 textos processados

**Métodos de geração:**
1. **Baseline:** Prompt básico sem instruções de estilo
2. **Prompt Steering:** Prompt com descrição estilométrica detalhada
3. **Activation Steering:** Manipulação de vetores de ativação (camada 12, escala 1.0)

## 📈 Métricas Extraídas

**Pipeline completo:** 237 métricas → 65 métricas filtradas

**Redução dimensional:**
- Removidas: 126 métricas com ≥20% NaN (54.8%)
- Removidas: 4 métricas constantes
- Removidas: 31 métricas de contagem (redundantes com proporções)
- Removidas: 8 métricas altamente correlacionadas (|r| ≥ 0.95)

**Métricas finais (65):**
- 8 léxicas básicas (TTR, n-gramas, tamanho médio de sentenças)
- 1 sintática global (mean dependency distance)
- 56 sintáticas (proporções de UPOS/DEPREL + distâncias médias)

## 🔬 Análises Realizadas

### 1. Qualidade das Métricas
Identificação de métricas problemáticas (NaN, variância zero, correlações).

### 2. Perfis Autorais
Caracterização de cada autor através de métricas discriminativas. **Top 3:**
- `root_prop` (CV=0.784): densidade de orações independentes
- `appos_prop` (CV=0.749): uso de aposição
- `PRON_prop` (CV=0.746): densidade pronominal

### 3. Comparação de Métodos
Preservation scores (1 - distância euclidiana normalizada):
- **Activation steering:** 0.716 (melhor)
- Baseline: 0.715
- Prompt steering: 0.623 (pior)

### 4. Decaimento Temporal
Análise de evolução de TTR em 5 janelas temporais:
- Originais: slope = +0.0057 (41.7% negativos, quase sem decay)
- Baseline: slope = -0.0934 (90.6% negativos, **16× mais decay**)

### 5. Consistência Intra-Método
Coeficiente de variação (CV) entre 3 repetições:
- **Activation steering:** 0.189 (melhor, mais determinístico)
- Baseline: 0.198
- Prompt steering: 0.342 (pior, alta instabilidade)
- **Diferença significativa** (Kruskal-Wallis: p<0.0001)

### 6. Síntese Final
Interpretação linguística integrada dos resultados. Ver `analysis/06_synthesis/SINTESE_FINAL.md`.

## 🚀 Como Usar

### Extração de Métricas (se necessário reprocessar)

```bash
cd scripts/metrics_extraction
python extract_all_metrics.py
```

**Tempo:** ~7-11 horas (UDPipe API é o gargalo)  
**Output:** `metrics/all_texts.csv` (600 textos × 237 métricas)

### Redução Dimensional e Análises

```bash
cd scripts/analysis

# Análises individuais (executadas sequencialmente)
python 01_analyze_metrics_quality.py    # Identificar métricas problemáticas
python 02_filter_metrics.py             # Aplicar filtros (237 → 65)
python 03_create_author_profiles.py     # Perfis autorais
python 04_compare_methods.py            # Comparar steering methods
python 05_analyze_temporal_decay.py     # Análise temporal
python 06_analyze_consistency.py        # Consistência intra-método
python 07_generate_final_synthesis.py   # Síntese final
```

Cada script gera:
- `analysis/{N}_{nome}/data/` - CSVs com resultados
- `analysis/{N}_{nome}/plots/` - Visualizações
- `analysis/{N}_{nome}/report.md` - Relatório interpretativo

## 📊 Principais Resultados

### Hierarquia de Controlabilidade

**Facilmente controlável:**
- Métricas léxicas superficiais (tamanho de palavras, TTR)
- Distribuições de classes gramaticais (UPOS)

**Dificilmente controlável:**
- Estruturas sintáticas profundas (subordinação, encaixamento)
- Relações de dependência complexas (apposição, modificação adverbial)

### Implicações Práticas

**Para aplicações que requerem reprodutibilidade:**
- ✅ Usar activation steering (mais consistente)
- ⚠️ Evitar prompt steering (alta variabilidade)

**Para preservação de estilo autoral:**
- ✅ Activation steering é superior
- ⚠️ Baseline tem decaimento temporal artificial
- ❌ Prompt steering diverge muito do original

**Limitação geral:**
- Nenhum método atual controla totalmente estruturas sintáticas profundas
- Supervisão humana permanece necessária para aplicações exigentes

## 🛠️ Dependências

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn nltk tqdm
```

**Recursos NLTK:**
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('rslp')
```

**UDPipe:** API pública do LINDAT (requer conexão internet)

## 🎓 Citação

Se usar este trabalho, considere citar:

```bibtex
@misc{linguistics_steering_2025,
  title={Quantitative Analysis of Authorial Style Preservation in LLM-Generated Texts with Steering Methods},
  author={[Seu Nome]},
  year={2025},
  note={Comparative study of baseline, prompt steering, and activation steering techniques}
}
```

## 📝 Modelo Utilizado

- **Modelo:** `openai/gpt-oss-20b`
- **Steering:** Camada 12, escala 1.0
- **Método:** Contrafactual (aproximar literário, distanciar enciclopédico)

## 🚧 Roadmap

### Para Adicionar ao Repositório:

- [ ] Dataset completo de treinamento (corpus literário + enciclopédico)
- [ ] Pipeline de cálculo de steering vectors
- [ ] Prompts de geração (baseline, prompt steering, activation steering)
- [ ] Scripts de geração dos 540 textos
- [ ] Hiperparâmetros de geração (temperatura, top-p, etc.)
- [ ] Notebook demonstrativo do processo completo

**Contribuições e questões:** Abra uma issue para discutir componentes ausentes ou metodologia.

## 📄 Licença

[Especifique a licença aqui]

---

**Status:** ✅ Análise linguística completa | ⚠️ Pipeline de geração não incluído  
**Última atualização:** Novembro 2025
