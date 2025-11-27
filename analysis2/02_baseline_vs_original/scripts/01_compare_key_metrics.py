#!/usr/bin/env python3
"""
Comparação: Original vs Baseline
Métricas: TTR, Tamanho de Frases, Densidade de Pronomes
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Carregar dados
df = pd.read_csv("../../metrics_filtered/all_texts_filtered.csv")
df_comp = df[df['condition'].isin(['original', 'baseline'])].copy()

# Métricas padronizadas
metrics = {
    'basic_ttr': 'Riqueza Vocabular (TTR)',
    'basic_tokens_per_sentence_mean': 'Tamanho de Frases',
    'synt_UPOS_PRON_prop': 'Densidade de Pronomes'
}

colors = {'lispector': '#E63946', 'woolf': '#457B9D', 
          'wikipedia_pt': '#F1A208', 'wikipedia_eng': '#2A9D8F'}

# Visualização
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (metric_key, metric_name) in enumerate(metrics.items()):
    ax = axes[idx]
    stats = df_comp.groupby(['author', 'condition'])[metric_key].agg(['mean', 'std', 'count']).reset_index()
    authors = sorted(df_comp['author'].unique())
    x_orig = np.arange(len(authors))
    x_base = x_orig + 0.35
    width = 0.35
    
    for i, author in enumerate(authors):
        orig_val = stats[(stats['author'] == author) & (stats['condition'] == 'original')]['mean'].values[0]
        base_val = stats[(stats['author'] == author) & (stats['condition'] == 'baseline')]['mean'].values[0]
        orig_std = stats[(stats['author'] == author) & (stats['condition'] == 'original')]['std'].values[0]
        base_std = stats[(stats['author'] == author) & (stats['condition'] == 'baseline')]['std'].values[0]
        orig_n = stats[(stats['author'] == author) & (stats['condition'] == 'original')]['count'].values[0]
        base_n = stats[(stats['author'] == author) & (stats['condition'] == 'baseline')]['count'].values[0]
        
        # Usar erro padrão da média (SEM) ao invés de std
        orig_sem = orig_std / np.sqrt(orig_n)
        base_sem = base_std / np.sqrt(base_n)
        
        ax.bar(x_orig[i], orig_val, width, yerr=orig_sem,
               color=colors[author], alpha=0.7, edgecolor='black', linewidth=1.5, capsize=4)
        ax.bar(x_base[i], base_val, width, yerr=base_sem,
               color=colors[author], alpha=0.3, edgecolor='black', linewidth=1.5, capsize=4, hatch='//')
    
    ax.set_ylabel(metric_name, fontsize=12, weight='bold')
    ax.set_title(metric_name, fontsize=13, weight='bold')
    ax.set_xticks(list(x_orig) + list(x_base))
    ax.set_xticklabels(authors + authors, fontsize=8, rotation=15, ha='right')
    ax.grid(True, alpha=0.3, axis='y')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='gray', alpha=0.7, label='Original'),
    Patch(facecolor='gray', alpha=0.3, hatch='//', label='Baseline')
]
fig.legend(handles=legend_elements, loc='upper center', ncol=2, 
           fontsize=11, bbox_to_anchor=(0.5, 0.98))

plt.suptitle('Métricas-Chave: Original vs Baseline\n(Barras cheias=Original, Barras listradas=Baseline)', 
             fontsize=14, weight='bold', y=1.05)
plt.tight_layout()

output_path = Path(__file__).parent.parent / "plots/01_key_metrics_comparison.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print("✓ Gráfico salvo: 01_key_metrics_comparison.png")

# Calcular mudanças
print("\n" + "="*70)
print("MUDANÇAS: Original → Baseline")
print("="*70)

changes_data = []
for metric_key, metric_name in metrics.items():
    print(f"\n{metric_name}:")
    for author in sorted(df_comp['author'].unique()):
        orig = df_comp[(df_comp['author'] == author) & (df_comp['condition'] == 'original')][metric_key]
        base = df_comp[(df_comp['author'] == author) & (df_comp['condition'] == 'baseline')][metric_key]
        orig_mean, base_mean = orig.mean(), base.mean()
        change_pct = ((base_mean - orig_mean) / orig_mean * 100)
        print(f"  {author:20s} {orig_mean:7.3f} → {base_mean:7.3f} ({change_pct:+6.1f}%)")
        changes_data.append({
            'metric': metric_name, 'author': author,
            'original': orig_mean, 'baseline': base_mean, 'change_pct': change_pct
        })

changes_df = pd.DataFrame(changes_data)
dados_path = Path(__file__).parent.parent / "dados/metric_changes.csv"
dados_path.parent.mkdir(parents=True, exist_ok=True)
changes_df.to_csv(dados_path, index=False)
print(f"\n✓ Mudanças salvas: metric_changes.csv")
