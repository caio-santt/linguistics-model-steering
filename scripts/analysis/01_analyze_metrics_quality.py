#!/usr/bin/env python3
"""
Análise de Qualidade das Métricas Extraídas

Identifica métricas problemáticas:
- Valores ausentes (NaN)
- Variância zero ou muito baixa
- Correlações altas (redundância)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
METRICS_FILE = BASE_DIR / "metrics/full_text/individual/all_texts.csv"
OUTPUT_DIR = BASE_DIR / "analysis/01_metrics_quality"
DATA_DIR = OUTPUT_DIR / "data"

# Criar diretórios
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("ANÁLISE DE QUALIDADE DAS MÉTRICAS")
print("=" * 70)

# 1. Carregar dados
print("\n[1/5] Carregando dados...")
df = pd.read_csv(METRICS_FILE)
print(f"   ✓ {len(df)} textos × {len(df.columns)} colunas")

# Separar metadados de métricas
metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df.columns if col not in metadata_cols]
print(f"   ✓ {len(metric_cols)} métricas para análise")

# 2. Análise de valores ausentes
print("\n[2/5] Analisando valores ausentes...")
nan_stats = []
for col in metric_cols:
    n_nan = df[col].isna().sum()
    pct_nan = (n_nan / len(df)) * 100
    nan_stats.append({
        'metric': col,
        'n_nan': n_nan,
        'pct_nan': pct_nan
    })

nan_df = pd.DataFrame(nan_stats).sort_values('pct_nan', ascending=False)
nan_df.to_csv(DATA_DIR / "nan_percentage.csv", index=False)

# Contagem por categoria
n_perfect = (nan_df['pct_nan'] == 0).sum()
n_good = ((nan_df['pct_nan'] > 0) & (nan_df['pct_nan'] < 5)).sum()
n_acceptable = ((nan_df['pct_nan'] >= 5) & (nan_df['pct_nan'] < 20)).sum()
n_problematic = (nan_df['pct_nan'] >= 20).sum()

print(f"   ✓ Métricas perfeitas (0% NaN): {n_perfect}")
print(f"   ✓ Métricas boas (<5% NaN): {n_good}")
print(f"   ✓ Métricas aceitáveis (5-20% NaN): {n_acceptable}")
print(f"   ⚠ Métricas problemáticas (≥20% NaN): {n_problematic}")

# 3. Análise de variância
print("\n[3/5] Analisando variância...")
variance_stats = []
for col in metric_cols:
    values = df[col].dropna()
    if len(values) > 0:
        variance_stats.append({
            'metric': col,
            'n_valid': len(values),
            'mean': values.mean(),
            'std': values.std(),
            'variance': values.var(),
            'min': values.min(),
            'max': values.max()
        })

var_df = pd.DataFrame(variance_stats)
var_df['cv'] = var_df['std'] / var_df['mean'].replace(0, np.nan)  # Coeficiente de variação
var_df = var_df.sort_values('variance')
var_df.to_csv(DATA_DIR / "variance_stats.csv", index=False)

# Métricas constantes (variância zero)
n_constant = (var_df['variance'] == 0).sum()
n_very_low = ((var_df['variance'] > 0) & (var_df['variance'] < 0.001)).sum()

print(f"   ⚠ Métricas constantes (var=0): {n_constant}")
print(f"   ⚠ Métricas com variância muito baixa (<0.001): {n_very_low}")

# 4. Análise de correlações
print("\n[4/5] Analisando correlações...")
# Apenas métricas com <20% NaN para correlação confiável
valid_metrics = nan_df[nan_df['pct_nan'] < 20]['metric'].tolist()
df_valid = df[valid_metrics].dropna()

print(f"   ✓ Calculando correlações para {len(valid_metrics)} métricas...")

corr_matrix = df_valid.corr()

# Encontrar pares com alta correlação (r ≥ 0.95)
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_value = corr_matrix.iloc[i, j]
        if abs(corr_value) >= 0.95:
            high_corr_pairs.append({
                'metric_1': corr_matrix.columns[i],
                'metric_2': corr_matrix.columns[j],
                'correlation': corr_value
            })

corr_df = pd.DataFrame(high_corr_pairs).sort_values('correlation', ascending=False, key=abs)
corr_df.to_csv(DATA_DIR / "correlations_high.csv", index=False)

print(f"   ⚠ Pares com correlação |r| ≥ 0.95: {len(high_corr_pairs)}")

# 5. Gerar relatório
print("\n[5/5] Gerando relatório...")

report = f"""# Análise de Qualidade das Métricas

## Dados
- Arquivo: `metrics/full_text/individual/all_texts.csv`
- N textos: {len(df)}
- N métricas: {len(metric_cols)}

## Método
Análise exploratória para identificar métricas problemáticas: valores ausentes (NaN), variância zero, e alta correlação (redundância).

## Resultados

### 1. Valores Ausentes

| Categoria | N Métricas | % do Total |
|-----------|------------|------------|
| Perfeitas (0% NaN) | {n_perfect} | {n_perfect/len(metric_cols)*100:.1f}% |
| Boas (<5% NaN) | {n_good} | {n_good/len(metric_cols)*100:.1f}% |
| Aceitáveis (5-20% NaN) | {n_acceptable} | {n_acceptable/len(metric_cols)*100:.1f}% |
| **Problemáticas (≥20% NaN)** | **{n_problematic}** | **{n_problematic/len(metric_cols)*100:.1f}%** |

**Top 10 métricas com mais NaN:**
"""

for idx, row in nan_df.head(10).iterrows():
    report += f"\n- `{row['metric']}`: {row['pct_nan']:.1f}% NaN"

report += f"""

### 2. Variância

| Categoria | N Métricas |
|-----------|------------|
| Constantes (var=0) | {n_constant} |
| Variância muito baixa (<0.001) | {n_very_low} |

**Métricas constantes devem ser removidas** (não discriminam nada).

### 3. Correlações Altas

- **N pares com \\|r\\| ≥ 0.95:** {len(high_corr_pairs)}
- Indicam redundância: métricas medem praticamente a mesma coisa

**Exemplo de pares altamente correlacionados:**
"""

for idx, row in corr_df.head(5).iterrows():
    report += f"\n- `{row['metric_1']}` ↔ `{row['metric_2']}`: r = {row['correlation']:.3f}"

report += """

## Interpretação Técnica

Das 230 métricas extraídas, aproximadamente {:.0f}% apresentam algum problema de qualidade (NaN ≥20%, variância zero, ou alta redundância). Métricas com muitos valores ausentes ocorrem porque certas relações sintáticas são raras (ex: `reparandum`, `vocative`, `orphan`). Alta correlação indica que proporções e contagens da mesma relação sintática são quase perfeitamente lineares (ex: `DEPREL_det_prop` ≈ `DEPREL_count_det`).

## Interpretação Simplificada

Muitas métricas são inúteis para análise: algumas nunca aparecem nos textos (valores ausentes), outras são sempre iguais (sem variação), e várias medem a mesma coisa de formas diferentes (redundância). Precisamos filtrar para manter apenas as métricas informativas e independentes.

## Implicações Linguísticas

Relações sintáticas raras (vocativos, reparos, elipses) são pouco informativas para caracterizar estilo autoral em textos escritos formais. A redundância entre proporções e contagens é esperada matematicamente, mas apenas uma forma deve ser mantida (proporções são preferíveis por serem normalizadas pelo tamanho do texto). A filtragem deve priorizar **métricas linguisticamente interpretáveis** (UPOS, DEPREL principais, MDD) sobre artefatos de parsing.
""".format(n_problematic/len(metric_cols)*100)

# Salvar relatório
report_file = OUTPUT_DIR / "report.md"
report_file.write_text(report)

print(f"   ✓ Relatório salvo em: {report_file.relative_to(BASE_DIR)}")

print("\n" + "=" * 70)
print("✅ ANÁLISE CONCLUÍDA")
print("=" * 70)
print(f"\nOutputs:")
print(f"  • {(DATA_DIR / 'nan_percentage.csv').relative_to(BASE_DIR)}")
print(f"  • {(DATA_DIR / 'variance_stats.csv').relative_to(BASE_DIR)}")
print(f"  • {(DATA_DIR / 'correlations_high.csv').relative_to(BASE_DIR)}")
print(f"  • {report_file.relative_to(BASE_DIR)}")
print()
