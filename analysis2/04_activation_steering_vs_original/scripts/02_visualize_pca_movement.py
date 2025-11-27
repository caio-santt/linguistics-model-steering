#!/usr/bin/env python3
"""
Pergunta: Como os autores se moveram no espaço PCA com activation steering?
Visualização: Original vs Activation Steering projetados no mesmo espaço PCA
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from pathlib import Path

# Carregar dados
df = pd.read_csv("../../metrics_filtered/all_texts_filtered.csv")

metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df.columns if col not in metadata_cols]

# Treinar PCA nos ORIGINAIS
df_orig = df[df['condition'] == 'original'].copy()
df_metrics_orig = df_orig[metric_cols].fillna(df_orig[metric_cols].mean())

scaler = StandardScaler()
scaler.fit(df_metrics_orig)

pca = PCA(n_components=2)
orig_pca = pca.fit_transform(scaler.transform(df_metrics_orig))

# Projetar ACTIVATION STEERING
df_act = df[df['condition'] == 'activation_steering'].copy()
df_metrics_act = df_act[metric_cols].fillna(df_act[metric_cols].mean())
act_pca = pca.transform(scaler.transform(df_metrics_act))

df_orig['PC1'] = orig_pca[:, 0]
df_orig['PC2'] = orig_pca[:, 1]
df_act['PC1'] = act_pca[:, 0]
df_act['PC2'] = act_pca[:, 1]

colors = {'lispector': '#E63946', 'woolf': '#457B9D', 
          'wikipedia_pt': '#F1A208', 'wikipedia_eng': '#2A9D8F'}

# ============================================================================
# VISUALIZAÇÃO
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# Plot 1: Scatter com todos os pontos
ax = axes[0]

for author in sorted(df_orig['author'].unique()):
    # Originais - pontos grandes
    orig_data = df_orig[df_orig['author'] == author]
    ax.scatter(orig_data['PC1'], orig_data['PC2'],
               c=colors[author], s=150, alpha=0.8,
               edgecolors='black', linewidth=2, label=f'{author} (orig)',
               marker='o')
    
    # Activation Steering - pontos pequenos com transparência
    act_data = df_act[df_act['author'] == author]
    ax.scatter(act_data['PC1'], act_data['PC2'],
               c=colors[author], s=30, alpha=0.3,
               edgecolors='none', marker='o')

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%) - Complexidade Sintática', 
              fontsize=12, weight='bold')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%) - Verbal vs Nominal', 
              fontsize=12, weight='bold')
ax.set_title('Distribuição Completa: Original vs Activation Steering\n(Pontos grandes=Original, Pontos pequenos=Activation Steering)', 
             fontsize=13, weight='bold')
ax.legend(fontsize=9, loc='best')
ax.grid(True, alpha=0.3)

# Plot 2: Centros com setas de movimento
ax = axes[1]

for author in sorted(df_orig['author'].unique()):
    # Calcular centros
    orig_data = df_orig[df_orig['author'] == author]
    act_data = df_act[df_act['author'] == author]
    
    orig_center = (orig_data['PC1'].mean(), orig_data['PC2'].mean())
    act_center = (act_data['PC1'].mean(), act_data['PC2'].mean())
    
    delta_pc1 = act_center[0] - orig_center[0]
    delta_pc2 = act_center[1] - orig_center[1]
    
    # Linhas tracejadas para componentes horizontal (ΔPC1) e vertical (ΔPC2)
    ax.plot([orig_center[0], act_center[0]], [orig_center[1], orig_center[1]], 
            linestyle='--', color=colors[author], linewidth=2.5, alpha=0.5, zorder=5)
    
    ax.plot([act_center[0], act_center[0]], [orig_center[1], act_center[1]],
            linestyle='--', color=colors[author], linewidth=2.5, alpha=0.5, zorder=5)
    
    # Plotar centros
    ax.scatter(*orig_center, c=colors[author], s=300, alpha=0.8,
               edgecolors='black', linewidth=3, marker='o', zorder=10)
    ax.scatter(*act_center, c=colors[author], s=300, alpha=0.4,
               edgecolors='black', linewidth=3, marker='s', zorder=10)
    
    # Seta de movimento (diagonal - distância total)
    ax.annotate('', xy=act_center, xytext=orig_center,
                arrowprops=dict(arrowstyle='->', lw=3, color=colors[author], alpha=0.7))
    
    # Label do autor
    ax.text(orig_center[0], orig_center[1] + 0.3, author, 
            ha='center', fontsize=10, weight='bold')
    
    # Distância total (diagonal)
    dist = np.sqrt(delta_pc1**2 + delta_pc2**2)
    mid_x = (orig_center[0] + act_center[0]) / 2
    mid_y = (orig_center[1] + act_center[1]) / 2
    ax.text(mid_x, mid_y - 0.3, f'd={dist:.2f}', 
            ha='center', fontsize=9, style='italic', weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Label ΔPC1 (horizontal)
    h_mid_x = (orig_center[0] + act_center[0]) / 2
    ax.text(h_mid_x, orig_center[1] - 0.25, f'Δ₁={abs(delta_pc1):.2f}', 
            fontsize=8, ha='center', style='italic', color=colors[author], 
            weight='bold', alpha=0.9)
    
    # Label ΔPC2 (vertical)
    v_mid_y = (orig_center[1] + act_center[1]) / 2
    ax.text(act_center[0] + 0.35, v_mid_y, f'Δ₂={abs(delta_pc2):.2f}', 
            fontsize=8, va='center', style='italic', color=colors[author],
            weight='bold', alpha=0.9)

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel(f'PC1 - Complexidade Sintática', fontsize=12, weight='bold')
ax.set_ylabel(f'PC2 - Verbal vs Nominal', fontsize=12, weight='bold')
ax.set_title('Movimento dos Centros: Original → Activation Steering\n(Círculos=Original, Quadrados=Activation Steering)', 
             fontsize=13, weight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()

output_path = Path(__file__).parent.parent / "plots/02_pca_movement.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print("✓ Visualização salva: 02_pca_movement.png")

# Salvar dados de movimento
movement_data = []
for author in df_orig['author'].unique():
    orig_data = df_orig[df_orig['author'] == author]
    act_data = df_act[df_act['author'] == author]
    
    movement_data.append({
        'author': author,
        'orig_PC1': orig_data['PC1'].mean(),
        'orig_PC2': orig_data['PC2'].mean(),
        'act_PC1': act_data['PC1'].mean(),
        'act_PC2': act_data['PC2'].mean(),
        'distance': np.sqrt((act_data['PC1'].mean() - orig_data['PC1'].mean())**2 + 
                           (act_data['PC2'].mean() - orig_data['PC2'].mean())**2),
        'delta_PC1': act_data['PC1'].mean() - orig_data['PC1'].mean(),
        'delta_PC2': act_data['PC2'].mean() - orig_data['PC2'].mean()
    })

movement_df = pd.DataFrame(movement_data)
movement_df = movement_df.sort_values('distance', ascending=False)

dados_path = Path(__file__).parent.parent / "dados/pca_movement.csv"
dados_path.parent.mkdir(parents=True, exist_ok=True)
movement_df.to_csv(dados_path, index=False)

print("\n" + "="*70)
print("MOVIMENTO NO ESPAÇO PCA:")
print("="*70)
print(movement_df.to_string(index=False))
print("\n✓ Dados salvos: pca_movement.csv")
