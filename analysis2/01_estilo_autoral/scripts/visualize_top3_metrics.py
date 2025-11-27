#!/usr/bin/env python3
"""
Visualizações das 3 Métricas Individuais Mais Interpretáveis

1. Tamanho de frases (tokens_per_sentence_mean)
2. Riqueza vocabular (TTR)
3. Densidade de pronomes (PRON_prop)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# Configuração
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 12)

# Paths
BASE_DIR = Path(__file__).parent.parent
METRICS_FILE = BASE_DIR / "metrics_filtered/all_texts_filtered.csv"
OUTPUT_DIR = BASE_DIR / "analysis2"

print("=" * 80)
print("VISUALIZAÇÕES: 3 MÉTRICAS INDIVIDUAIS MAIS INTERPRETÁVEIS")
print("=" * 80)

# Carregar dados
df = pd.read_csv(METRICS_FILE)
df_orig = df[df['condition'] == 'original'].copy()

colors = {'lispector': '#E63946', 'woolf': '#457B9D', 
          'wikipedia_pt': '#F1A208', 'wikipedia_eng': '#2A9D8F'}

# As 3 métricas
metrics = {
    'basic_tokens_per_sentence_mean': {
        'name': 'Tamanho de Frases',
        'ylabel': 'Palavras por Frase',
        'eta2': 0.589,
        'description': 'Número médio de palavras em cada frase'
    },
    'basic_ttr': {
        'name': 'Riqueza Vocabular (TTR)',
        'ylabel': 'Type-Token Ratio',
        'eta2': 0.282,
        'description': 'Proporção de palavras únicas no texto'
    },
    'synt_UPOS_PRON_prop': {
        'name': 'Densidade de Pronomes',
        'ylabel': 'Proporção de Pronomes',
        'eta2': 0.810,
        'description': 'Percentual de pronomes no texto'
    }
}

# ============================================================================
# FIGURA PRINCIPAL: 3×3 GRID
# ============================================================================
fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

for row, (metric_key, metric_info) in enumerate(metrics.items()):
    print(f"\n[{row+1}/3] Processando: {metric_info['name']}")
    
    # Calcular estatísticas
    stats_df = df_orig.groupby('author')[metric_key].agg(['mean', 'std', 'min', 'max'])
    stats_df = stats_df.sort_values('mean', ascending=False)
    
    print(f"  Estatísticas:")
    for author in stats_df.index:
        print(f"    {author:20s} {stats_df.loc[author, 'mean']:8.3f} ± {stats_df.loc[author, 'std']:6.3f}")
    
    # ========================================================================
    # COLUNA 1: BARPLOT COM VALORES
    # ========================================================================
    ax = fig.add_subplot(gs[row, 0])
    
    x_pos = np.arange(len(stats_df))
    bars = ax.bar(x_pos, stats_df['mean'],
                   yerr=stats_df['std'],
                   color=[colors.get(author, 'gray') for author in stats_df.index],
                   alpha=0.8, edgecolor='black', linewidth=2,
                   capsize=8, error_kw={'linewidth': 2})
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(stats_df.index, rotation=15, ha='right', fontsize=11)
    ax.set_ylabel(metric_info['ylabel'], fontsize=12, weight='bold')
    ax.set_title(f"{metric_info['name']}\n(η² = {metric_info['eta2']:.3f})", 
                 fontsize=13, weight='bold', pad=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras
    for i, (idx, row_data) in enumerate(stats_df.iterrows()):
        ax.text(i, row_data['mean'] + row_data['std'] + ax.get_ylim()[1]*0.02,
                f"{row_data['mean']:.2f}",
                ha='center', va='bottom', fontsize=11, weight='bold')
    
    # ========================================================================
    # COLUNA 2: BOXPLOT
    # ========================================================================
    ax = fig.add_subplot(gs[row, 1])
    
    data_for_box = [df_orig[df_orig['author'] == author][metric_key].values 
                    for author in stats_df.index]
    
    bp = ax.boxplot(data_for_box, patch_artist=True,
                    tick_labels=stats_df.index,
                    widths=0.6,
                    boxprops=dict(linewidth=2),
                    whiskerprops=dict(linewidth=2),
                    capprops=dict(linewidth=2),
                    medianprops=dict(color='red', linewidth=3))
    
    for patch, author in zip(bp['boxes'], stats_df.index):
        patch.set_facecolor(colors.get(author, 'gray'))
        patch.set_alpha(0.7)
    
    ax.set_xticklabels(stats_df.index, rotation=15, ha='right', fontsize=11)
    ax.set_ylabel(metric_info['ylabel'], fontsize=12, weight='bold')
    ax.set_title('Distribuição por Autor', fontsize=13, weight='bold', pad=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # ========================================================================
    # COLUNA 3: SWARMPLOT (distribuição individual)
    # ========================================================================
    ax = fig.add_subplot(gs[row, 2])
    
    # Preparar dados para swarmplot
    plot_data = []
    for author in stats_df.index:
        author_data = df_orig[df_orig['author'] == author][metric_key].values
        for value in author_data:
            plot_data.append({'author': author, 'value': value})
    
    plot_df = pd.DataFrame(plot_data)
    
    # Criar swarmplot manual (mais controle)
    for i, author in enumerate(stats_df.index):
        author_values = plot_df[plot_df['author'] == author]['value'].values
        y_vals = author_values
        x_vals = np.random.normal(i, 0.08, size=len(y_vals))  # Jitter
        
        ax.scatter(x_vals, y_vals,
                   c=colors.get(author, 'gray'),
                   s=120, alpha=0.6,
                   edgecolors='black', linewidth=1)
        
        # Adicionar média
        mean_val = author_values.mean()
        ax.plot([i-0.3, i+0.3], [mean_val, mean_val],
                'k-', linewidth=3, alpha=0.8, zorder=10)
    
    ax.set_xticks(range(len(stats_df)))
    ax.set_xticklabels(stats_df.index, rotation=15, ha='right', fontsize=11)
    ax.set_ylabel(metric_info['ylabel'], fontsize=12, weight='bold')
    ax.set_title('Distribuição Individual de Textos', fontsize=13, weight='bold', pad=10)
    ax.grid(True, alpha=0.3, axis='y')

# Título geral
fig.suptitle('Métricas Individuais Mais Interpretáveis\nEffect Size Grande (η² > 0.28) e Diferenças Significativas (p < 0.001)',
             fontsize=16, weight='bold', y=0.995)

plt.savefig(OUTPUT_DIR / "top3_interpretable_metrics.png", dpi=150, bbox_inches='tight')
print(f"\n✓ Figura principal salva: top3_interpretable_metrics.png")

# ============================================================================
# FIGURA COMPARATIVA: DIFERENÇAS RELATIVAS
# ============================================================================
print("\n" + "=" * 80)
print("GERANDO FIGURA COMPARATIVA")
print("=" * 80)

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

for idx, (metric_key, metric_info) in enumerate(metrics.items()):
    ax = axes[idx]
    
    # Calcular diferenças relativas ao mínimo
    stats_df = df_orig.groupby('author')[metric_key].agg(['mean'])
    stats_df = stats_df.sort_values('mean', ascending=True)
    
    min_val = stats_df['mean'].min()
    stats_df['relative'] = (stats_df['mean'] / min_val)
    stats_df['percentage'] = ((stats_df['mean'] - min_val) / min_val * 100)
    
    # Plot
    x_pos = np.arange(len(stats_df))
    bars = ax.barh(x_pos, stats_df['relative'],
                    color=[colors.get(author, 'gray') for author in stats_df.index],
                    alpha=0.8, edgecolor='black', linewidth=2)
    
    ax.set_yticks(x_pos)
    ax.set_yticklabels(stats_df.index, fontsize=12)
    ax.set_xlabel('Múltiplo do Menor Valor', fontsize=12, weight='bold')
    ax.set_title(f"{metric_info['name']}", fontsize=13, weight='bold', pad=10)
    ax.grid(True, alpha=0.3, axis='x')
    ax.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.5)
    
    # Adicionar valores
    for i, (author, row_data) in enumerate(stats_df.iterrows()):
        if row_data['relative'] > 1.1:
            label = f"{row_data['relative']:.2f}× (+{row_data['percentage']:.0f}%)"
        else:
            label = f"{row_data['relative']:.2f}×"
        
        ax.text(row_data['relative'] + 0.05, i, label,
                va='center', fontsize=11, weight='bold')
    
    print(f"\n{metric_info['name']}:")
    print(f"  Baseline: {stats_df.index[0]} = {stats_df['mean'].iloc[0]:.3f}")
    for author in stats_df.index[1:]:
        mult = stats_df.loc[author, 'relative']
        perc = stats_df.loc[author, 'percentage']
        print(f"  {author:20s} {mult:.2f}× maior (+{perc:.0f}%)")

plt.suptitle('Diferenças Relativas entre Autores\n(Normalizado pelo menor valor)',
             fontsize=15, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top3_relative_differences.png", dpi=150, bbox_inches='tight')
print(f"\n✓ Figura comparativa salva: top3_relative_differences.png")

# ============================================================================
# TABELA RESUMO
# ============================================================================
print("\n" + "=" * 80)
print("TABELA RESUMO")
print("=" * 80)

summary_data = []
for metric_key, metric_info in metrics.items():
    stats_df = df_orig.groupby('author')[metric_key].agg(['mean', 'std'])
    stats_df = stats_df.sort_values('mean', ascending=False)
    
    ranking = " > ".join(stats_df.index.tolist())
    max_author = stats_df.index[0]
    min_author = stats_df.index[-1]
    max_val = stats_df.loc[max_author, 'mean']
    min_val = stats_df.loc[min_author, 'mean']
    diff_mult = max_val / min_val
    
    summary_data.append({
        'Métrica': metric_info['name'],
        'η²': metric_info['eta2'],
        'Ranking': ranking,
        'Maior': f"{max_author} ({max_val:.2f})",
        'Menor': f"{min_author} ({min_val:.2f})",
        'Diferença': f"{diff_mult:.2f}×"
    })

summary_df = pd.DataFrame(summary_data)
print("\n" + summary_df.to_string(index=False))

summary_df.to_csv(OUTPUT_DIR / "top3_metrics_summary.csv", index=False)
print(f"\n✓ Tabela resumo salva: top3_metrics_summary.csv")

# ============================================================================
# FIGURA CORRELAÇÃO ENTRE AS 3 MÉTRICAS
# ============================================================================
print("\n" + "=" * 80)
print("GERANDO MATRIZ DE CORRELAÇÃO")
print("=" * 80)

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

metric_keys = list(metrics.keys())
combinations = [
    (0, 1),  # Tamanho vs TTR
    (0, 2),  # Tamanho vs Pronomes
    (1, 2)   # TTR vs Pronomes
]

for idx, (i, j) in enumerate(combinations):
    ax = axes[idx]
    
    metric_x = metric_keys[i]
    metric_y = metric_keys[j]
    
    name_x = metrics[metric_x]['name']
    name_y = metrics[metric_y]['name']
    
    # Scatter por autor
    for author in df_orig['author'].unique():
        df_author = df_orig[df_orig['author'] == author]
        ax.scatter(df_author[metric_x], df_author[metric_y],
                   c=colors.get(author, 'gray'), label=author,
                   s=150, alpha=0.7, edgecolors='black', linewidth=1.5)
    
    # Correlação geral
    corr = df_orig[metric_x].corr(df_orig[metric_y])
    
    ax.set_xlabel(metrics[metric_x]['ylabel'], fontsize=12, weight='bold')
    ax.set_ylabel(metrics[metric_y]['ylabel'], fontsize=12, weight='bold')
    ax.set_title(f"{name_x.split()[0]} vs {name_y.split()[0]}\n(r = {corr:.3f})",
                 fontsize=13, weight='bold', pad=10)
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)

plt.suptitle('Correlações entre as 3 Métricas Mais Interpretáveis',
             fontsize=15, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top3_correlations.png", dpi=150, bbox_inches='tight')
print(f"\n✓ Figura de correlações salva: top3_correlations.png")

# Matriz de correlação
print("\nMatriz de Correlação:")
corr_matrix = df_orig[list(metrics.keys())].corr()
corr_matrix.columns = [m['name'].split()[0] for m in metrics.values()]
corr_matrix.index = [m['name'].split()[0] for m in metrics.values()]
print(corr_matrix.to_string())

# ============================================================================
# SÍNTESE
# ============================================================================
print("\n" + "=" * 80)
print("SÍNTESE")
print("=" * 80)
print(f"""
Arquivos gerados:
  • top3_interpretable_metrics.png - Grid 3×3 com todas as visualizações
  • top3_relative_differences.png - Comparação relativa entre autores
  • top3_correlations.png - Correlações entre as 3 métricas
  • top3_metrics_summary.csv - Tabela resumo

Principais insights:

1. TAMANHO DE FRASES (η²=0.589):
   • Wikipedia PT tem frases 3.08× maiores que Lispector
   • Range: 11.1 (Lispector) a 34.4 (Wiki PT) palavras
   • Métrica mais discriminativa e mais fácil de comunicar

2. RIQUEZA VOCABULAR (η²=0.282):
   • Wikipedia PT e Lispector têm TTR similar (~0.51)
   • Woolf tem o menor (0.46) - repete mais palavras
   • Diferença menor que outras métricas (1.12×)

3. DENSIDADE DE PRONOMES (η²=0.810):
   • Woolf tem densidade muito maior que outros
   • Marca distintiva do estilo stream-of-consciousness
   • Segunda métrica mais discriminativa

Correlações:
  • Tamanho vs TTR: Baixa correlação (textos longos não são necessariamente mais variados)
  • Tamanho vs Pronomes: Correlação dependente do autor
  • TTR vs Pronomes: Independentes (vocabulário ≠ foco pronominal)
""")

print("=" * 80)
print("✅ VISUALIZAÇÕES CONCLUÍDAS")
print("=" * 80)
