# Linguistics and Model Steering

Análise de preservação de estilo autoral em LLMs usando steering de ativações.

## 📁 Estrutura do Projeto

```
linguistics_and_model_steering/
├── data/
│   ├── original/                                    # Textos originais (prefixes)
│   │   ├── lispector/                               # 15 samples (5 títulos × 3 samples)
│   │   ├── woolf/                                   # 15 samples
│   │   ├── wikipedia_pt/                            # 15 samples
│   │   └── wikipedia_eng/                           # 15 samples
│   │
│   └── generated/                                   # Textos gerados pela LLM
│       ├── 00_BASELINE-raw_prompt/                  # Prompt básico sem instruções
│       ├── 01_PROMPT_STEERING-style-description/    # Prompt com descrição estilística
│       └── 02_ACTIVATION_STEERING-raw-prompt/       # Steering de ativações + prompt básico
│
├── metrics/                   # Métricas extraídas (a gerar)
├── analysis/                  # Scripts de análise (a criar)
└── results/                   # Resultados e visualizações (a criar)
```

## 📊 Dataset

**Autores:** 4 (2 literários + 2 enciclopédicos)
- `lispector` - Clarice Lispector (PT, literário)
- `woolf` - Virginia Woolf (EN, literário)
- `wikipedia_pt` - Artigos da Wikipedia em português (enciclopédico)
- `wikipedia_eng` - Artigos da Wikipedia em inglês (enciclopédico)

**Textos por autor:**
- 5 títulos para avaliação
- 3 samples por título (diferentes trechos)
- **Total: 60 samples originais** (4 autores × 5 títulos × 3 samples)

**Condições experimentais:**

1. **00_BASELINE-raw_prompt**: Prompt básico sem instruções de estilo
   - Apenas "Continue este texto..."

2. **01_PROMPT_STEERING-style-description**: Guia explícito via prompt
   - Prompt com descrição estilométrica detalhada do autor
   - Ex: "Continue com frases curtas, ritmo ágil, foco em ações..."

3. **02_ACTIVATION_STEERING-raw-prompt**: Guia implícito via manipulação interna
   - Prompt básico + steering de ativações (camada 12)
   - Vetores literários aplicados a todos:
     * Wikipedia PT → steering de Lispector
     * Lispector → steering de Lispector  
     * Wikipedia EN → steering de Woolf
     * Woolf → steering de Woolf

**Repetições:** 3 por sample/condição

**Total de textos gerados:** 540 (60 samples × 3 condições × 3 reps)

## 🎯 Hipóteses de Pesquisa

**RQ1:** LLMs conseguem manter estilo autoral? Qual a diferença entre estilos literários e enciclopédicos?
- Método: Baseline vs Originais

**RQ2:** Existem métodos para melhorar preservação de estilo literário?
- Métodos testados:
  1. Style Description (guia explícito via prompt)
  2. Activation Steering (guia implícito via manipulação de ativações)

## 📝 Naming Convention

**Textos originais:**
```
{author}/{title}__s{sample:02d}.txt
Exemplo: lispector/brasilia__s00.txt
```

**Textos gerados:**
```
{condition}/{author}/{title}__s{sample:02d}__r{rep:02d}.txt
Exemplo: 00_BASELINE-raw_prompt/lispector/brasilia__s00__r00.txt
```

## 🔧 Próximos Passos

1. [ ] Extrair métricas estilométricas (UDPipe + básicas)
2. [ ] Análise comparativa (baseline vs style_desc vs steering)
3. [ ] Análise por gênero (literário vs enciclopédico)
4. [ ] Visualizações e relatório final

## 🚀 LLM Utilizado

- **Modelo:** `openai/gpt-oss-20b`
- **Steering:** Camada 12, escala 1.0
- **Método:** Contrafactual (aproximar literário, distanciar enciclopédico)
