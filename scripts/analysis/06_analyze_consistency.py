#!/usr/bin/env python3
"""
Análise de Consistência Intra-Método

Avalia variabilidade entre as 3 repetições de cada sample/condição.
Métodos mais consistentes (baixo CV) são mais determinísticos/controlados.

Métricas:
- Coeficiente de variação (CV) por sample
- CV médio por método
- Comparação entre métodos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
METRICS_FILE = BASE_DIR / "metrics_filtered/all_texts_filtered.csv"
OUTPUT_DIR = BASE_DIR / "analysis/05_consistency"
DATA_DIR = OUTPUT_DIR / "data"
PLOTS_DIR = OUTPUT_DIR / "plots"

# Criar diretórios
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("ANÁLISE DE CONSISTÊNCIA INTRA-MÉTODO")
print("=" * 70)

# 1. Carregar dados
print("\n[1/4] Carregando dados...")
df = pd.read_csv(METRICS_FILE)

# Apenas textos gerados (têm 3 repetições)
df_generated = df[df['condition'] != 'original'].copy()
print(f"   ✓ {len(df_generated)} textos gerados")
print(f"   ✓ Métodos: {df_generated['condition'].unique().tolist()}")

# Separar metadados
metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df.columns if col not in metadata_cols]
print(f"   ✓ {len(metric_cols)} métricas")

# 2. Calcular CV por sample (3 repetições)
print("\n[2/4] Calculando coeficientes de variação...")

cv_results = []

# Agrupar por (author, title, sample_idx, condition)
for (author, title, sample_idx, condition), group in df_generated.groupby(['author', 'title', 'sample_idx', 'condition']):
    if len(group) == 3:  # Exatamente 3 repetições
        sample_cvs = {
            'author': author,
            'title': title,
            'sample_idx': sample_idx,
            'condition': condition,
            'lang': group.iloc[0]['lang']
        }
        
        # CV por métrica
        for metric in metric_cols:
            values = group[metric].dropna()
            if len(values) >= 2 and values.mean() != 0:
                cv = values.std() / values.mean()
                sample_cvs[f'{metric}_cv'] = abs(cv)  # Valor absoluto
            else:
                sample_cvs[f'{metric}_cv'] = np.nan
        
        cv_results.append(sample_cvs)

cv_df = pd.DataFrame(cv_results)
cv_df.to_csv(DATA_DIR / "cv_by_sample.csv", index=False)
print(f"   ✓ CV calculado para {len(cv_df)} samples")

# 3. Estatísticas por método
print("\n[3/4] Calculando estatísticas por método...")

cv_cols = [col for col in cv_df.columns if col.endswith('_cv')]

method_stats = []
for condition in ['baseline', 'prompt_steering', 'activation_steering']:
    df_method = cv_df[cv_df['condition'] == condition]
    
    # CV médio por métrica
    cv_means = df_method[cv_cols].mean()
    
    # CV global (média de todas as métricas)
    global_cv = cv_means.mean()
    
    method_stats.append({
        'method': condition,
        'n_samples': len(df_method),
        'mean_cv_global': global_cv,
        'std_cv_global': cv_means.std(),
        'min_cv': cv_means.min(),
        'max_cv': cv_means.max()
    })
    
    print(f"   • {condition}:")
    print(f"     - CV médio global: {global_cv:.4f}")
    print(f"     - Métricas mais consistentes: {cv_means.nsmallest(3).index.tolist()}")

method_stats_df = pd.DataFrame(method_stats)
method_stats_df.to_csv(DATA_DIR / "consistency_by_method.csv", index=False)

# Teste estatístico: Comparar CV entre métodos
print("\n   ✓ Comparando consistência entre métodos...")
groups = []
for condition in ['baseline', 'prompt_steering', 'activation_steering']:
    # Pegar CV médio por sample (média de todas as métricas)
    df_method = cv_df[cv_df['condition'] == condition]
    sample_cvs = df_method[cv_cols].mean(axis=1).dropna()
    groups.append(sample_cvs)

h_stat, p_value = stats.kruskal(*groups)
print(f"   ✓ Kruskal-Wallis test: H={h_stat:.3f}, p={p_value:.4f}")

# 4. Visualizações
print("\n[4/4] Gerando visualizações...")

# Plot 1: CV global por método
fig, ax = plt.subplots(figsize=(10, 6))

methods = ['baseline', 'prompt_steering', 'activation_steering']
data_plot = []
for method in methods:
    df_method = cv_df[cv_df['condition'] == method]
    # CV médio por sample (média de todas as métricas)
    sample_cvs = df_method[cv_cols].mean(axis=1).dropna()
    data_plot.append(sample_cvs)

bp = ax.boxplot(data_plot, labels=[m.replace('_', '\n') for m in methods], patch_artist=True)
for patch, color in zip(bp['boxes'], ['lightblue', 'lightgreen', 'lightyellow']):
    patch.set_facecolor(color)

ax.set_ylabel('Coeficiente de Variação (CV)', fontsize=12)
ax.set_title('Consistência Intra-Método (menor = mais consistente)', fontsize=14, weight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "consistency_comparison.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: consistency_comparison.png")

# Plot 2: Heatmap - CV por métrica e método (top 20 métricas mais variáveis)
# Calcular CV médio por métrica e método
cv_by_metric_method = []
for condition in methods:
    df_method = cv_df[cv_df['condition'] == condition]
    for col in cv_cols:
        metric_name = col.replace('_cv', '')
        cv_mean = df_method[col].mean()
        cv_by_metric_method.append({
            'metric': metric_name,
            'method': condition,
            'mean_cv': cv_mean
        })

cv_heatmap_df = pd.DataFrame(cv_by_metric_method)

# Top 20 métricas com maior CV (média entre métodos)
top_metrics = cv_heatmap_df.groupby('metric')['mean_cv'].mean().nlargest(20).index
cv_heatmap_filtered = cv_heatmap_df[cv_heatmap_df['metric'].isin(top_metrics)]

# Pivot para heatmap
heatmap_data = cv_heatmap_filtered.pivot(index='metric', columns='method', values='mean_cv')

# Limpar nomes
heatmap_data.index = [m.replace('synt_', '').replace('basic_', '').replace('_prop', '').replace('_md', '')
                       for m in heatmap_data.index]
heatmap_data.columns = [c.replace('_', ' ').title() for c in heatmap_data.columns]

fig, ax = plt.subplots(figsize=(10, 12))
sns.heatmap(heatmap_data, annot=True, fmt='.3f', cmap='YlOrRd', cbar_kws={'label': 'CV Médio'}, ax=ax)
ax.set_title('Variabilidade por Métrica e Método\n(valores altos = baixa consistência)', 
             fontsize=14, weight='bold', pad=20)
ax.set_xlabel('Método de Geração', fontsize=12)
ax.set_ylabel('Métrica', fontsize=12)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "cv_heatmap_top20.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: cv_heatmap_top20.png")

# 5. Relatório
print("\n[5/5] Gerando relatório...")

# Identificar método mais consistente
best_method = method_stats_df.loc[method_stats_df['mean_cv_global'].idxmin(), 'method']
best_cv = method_stats_df['mean_cv_global'].min()

report = f"""# Análise de Consistência Intra-Método

## Dados
- Arquivo: `metrics_filtered/all_texts_filtered.csv`
- N samples: {len(cv_df)} (cada sample com 3 repetições)
- N métodos: 3 (baseline, prompt_steering, activation_steering)
- N métricas: {len(metric_cols)}

## Método
Para cada sample, calcular coeficiente de variação (CV = std/mean) entre as 3 repetições. CV baixo indica consistência (gerações similares), CV alto indica variabilidade (gerações divergentes). Teste de Kruskal-Wallis para comparar CV entre métodos.

## Resultados

### 1. Consistência Global por Método

| Método | N Samples | CV Médio | Desvio Padrão | Min CV | Max CV |
|--------|-----------|----------|---------------|--------|--------|
"""

for _, row in method_stats_df.iterrows():
    report += f"| {row['method']} | {row['n_samples']} | {row['mean_cv_global']:.4f} | {row['std_cv_global']:.4f} | {row['min_cv']:.4f} | {row['max_cv']:.4f} |\n"

report += f"""

**Método mais consistente:** {best_method} (CV = {best_cv:.4f})

**Teste de Kruskal-Wallis:** H = {h_stat:.3f}, p = {p_value:.4f}

"""

if p_value < 0.05:
    report += "**Interpretação:** Diferença significativa na consistência entre métodos (p < 0.05).\n"
else:
    report += "**Interpretação:** Sem diferença significativa na consistência entre métodos (p ≥ 0.05).\n"

report += """

### 2. Métricas Mais Variáveis

**Métricas com maior CV (média entre métodos):**

"""

# Top 10 métricas mais variáveis
top_variable = cv_heatmap_df.groupby('metric')['mean_cv'].mean().nlargest(10)
for metric, cv_val in top_variable.items():
    metric_clean = metric.replace('synt_', '').replace('basic_', '')
    report += f"- `{metric_clean}`: CV = {cv_val:.4f}\n"

report += """

## Interpretação Técnica

"""

if best_method == 'baseline':
    interpretation = "Baseline é mais determinístico: mesmo input gera outputs similares. Steering methods introduzem variabilidade, possivelmente por dependerem de vetores de ativação que capturam ruído do modelo."
elif best_method == 'prompt_steering':
    interpretation = "Prompt steering é mais consistente: instruções explícitas reduzem espaço de busca do modelo. Baseline e activation têm mais variabilidade por explorarem latent space mais livremente."
else:  # activation_steering
    interpretation = "Activation steering é mais consistente: manipulação direta de representações internas produz outputs mais previsíveis. Prompt steering e baseline dependem mais de sampling estocástico."

report += f"{interpretation} CV alto em métricas sintáticas específicas (subordinação, modificação) indica que essas estruturas são menos controláveis mesmo com steering.\n"

report += """

## Interpretação Simplificada

Consistência mede se o método gera textos parecidos quando executado várias vezes com o mesmo input. Baixo CV = método confiável e previsível. Alto CV = método instável, cada geração é muito diferente. Métodos consistentes são preferíveis para aplicações que requerem reprodutibilidade (ex: geração de resumos, tradução automática).

## Implicações Linguísticas

Consistência baixa em métricas léxicas (TTR, n-gramas) é esperada e desejável (variação superficial mantendo conteúdo). Consistência baixa em métricas sintáticas profundas (subordinação, modificação) é problemática: sugere que steering não controla totalmente estrutura gramatical, apenas aspectos superficiais. Ideal: **alta consistência em sintaxe + variação controlada em léxico**. Métodos que atingem esse equilíbrio demonstram controle fino sobre geração.
"""

report_file = OUTPUT_DIR / "report.md"
report_file.write_text(report)
print(f"   ✓ Relatório salvo em: {report_file.relative_to(BASE_DIR)}")

print("\n" + "=" * 70)
print("✅ ANÁLISE DE CONSISTÊNCIA CONCLUÍDA")
print("=" * 70)
print(f"\nMétodo mais consistente: {best_method} (CV = {best_cv:.4f})")
print(f"Teste Kruskal-Wallis: H={h_stat:.3f}, p={p_value:.4f}")
print(f"\nOutputs:")
print(f"  • {(DATA_DIR / 'cv_by_sample.csv').relative_to(BASE_DIR)}")
print(f"  • {(DATA_DIR / 'consistency_by_method.csv').relative_to(BASE_DIR)}")
print(f"  • {PLOTS_DIR.relative_to(BASE_DIR)}/*.png (2 gráficos)")
print(f"  • {report_file.relative_to(BASE_DIR)}")
print()
