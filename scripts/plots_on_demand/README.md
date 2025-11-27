# Scripts de Plots Sob Demanda

Scripts independentes para gerar visualizações específicas para apresentação/slides.

## 📊 Scripts Disponíveis

### 1. `dimensao_divergencia_table.py`
**Descrição:** Gera tabela de divergência agrupada por dimensão linguística.

**Output:**
- CSV: `divergence_by_dimension.csv`
- Tabela formatada no terminal (baseline)

**Dimensões analisadas:**
- Léxica (básica): TTR, n-gramas, tamanho
- Sintática UPOS: Classes gramaticais
- Sintática DEPREL: Relações de dependência
- Sintática (outras): MDD e outras métricas

**Como usar:**
```bash
cd scripts/plots_on_demand
python dimensao_divergencia_table.py
```

**Output exemplo:**
```
Dimensão                            | Divergência  | Classificação  
-------------------------------------------------------------------
Léxica (básica)                     | 0.8234       | Baixa ✅
Sintática UPOS (classes gram.)      | 1.2456       | Média ⚠️
Sintática DEPREL (dependências)     | 1.8923       | Alta ❌
```

---

### 2. `temporal_evolution_plot.py`
**Descrição:** Gera gráfico de linha mostrando evolução temporal de TTR (Type-Token Ratio).

**Output:**
- PNG: `temporal_evolution_ttr.png` (alta resolução, 150 DPI)
- Estatísticas descritivas no terminal

**Compara:**
- Original vs Baseline (padrão para RQ1)
- Ou todas as condições (modificar variável `conditions_to_plot`)

**Como usar:**
```bash
cd scripts/plots_on_demand
python temporal_evolution_plot.py
```

**Features do gráfico:**
- 5 janelas temporais (0-20%, 20-40%, ..., 80-100%)
- Linhas com marcadores
- Área sombreada (desvio padrão)
- Anotação de decay % do baseline
- Cores distintas por método

---

## 🎨 Personalização

Para ajustar cores, tamanhos, ou estilos:
- Edite as variáveis no início de cada script
- `condition_colors`: Cores das linhas
- `plt.rcParams['figure.dpi']`: Resolução da imagem
- `figsize`: Tamanho da figura

---

## 📁 Dependências

Ambos os scripts dependem de:
- `metrics_filtered/all_texts_filtered.csv`
- `metrics/windowed/lexical_windowed.csv`
- `analysis/03_method_comparison/data/metrics_divergence.csv`

---

## 💡 Adicionar Novos Scripts

Coloque scripts soltos nesta pasta seguindo o padrão:
1. Nome descritivo: `{tipo}_{descricao}.py`
2. Docstring no topo explicando o objetivo
3. Output em `scripts/plots_on_demand/`
4. Print de confirmação ao final

---

**Última atualização:** Novembro 2025
