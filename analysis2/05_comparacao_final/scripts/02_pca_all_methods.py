"""
Supervisualização PCA: Movimentação de todos os métodos de steering
Mostra Original → Baseline, Prompt Steering e Activation Steering no mesmo espaço
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path

# Criar diretórios
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'plots'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Carregar dados
df = pd.read_csv("../../metrics_filtered/all_texts_filtered.csv")

# Preparar PCA (EXATAMENTE como nas análises individuais)
metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df.columns if col not in metadata_cols]

# Treinar StandardScaler e PCA APENAS nos ORIGINAIS
df_orig = df[df['condition'] == 'original'].copy()
df_metrics_orig = df_orig[metric_cols].fillna(df_orig[metric_cols].mean())

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(df_metrics_orig)

pca = PCA(n_components=2)
pca.fit(scaler.transform(df_metrics_orig))

# Cores por autor
colors = {
    'lispector': '#E63946',
    'woolf': '#457B9D',
    'wikipedia_pt': '#F1A208',
    'wikipedia_eng': '#2A9D8F'
}

# Estilos para cada método
styles = {
    'baseline': {'linestyle': '-', 'linewidth': 2, 'alpha': 0.7, 'label': 'Baseline'},
    'prompt_steering': {'linestyle': '--', 'linewidth': 2, 'alpha': 0.7, 'label': 'Prompt Steering'},
    'activation_steering': {'linestyle': ':', 'linewidth': 2.5, 'alpha': 0.7, 'label': 'Activation Steering'}
}

# Criar figura
fig, ax = plt.subplots(figsize=(14, 10))

# Processar cada autor
for author in sorted(df['author'].unique()):
    # Original (ponto de partida)
    df_author_orig = df[(df['author'] == author) & (df['condition'] == 'original')]
    X_author_orig = df_author_orig[metric_cols].fillna(df_author_orig[metric_cols].mean())
    orig_pca = pca.transform(scaler.transform(X_author_orig))
    orig_mean = orig_pca.mean(axis=0)
    
    # Plotar ponto original
    ax.scatter(orig_mean[0], orig_mean[1], s=200, color=colors[author], 
               edgecolor='black', linewidth=2, zorder=10, alpha=0.9,
               label=author.replace('_', ' ').title() if author == 'lispector' else "")
    
    # Markers para cada método
    markers = {
        'baseline': 's',           # quadrado
        'prompt_steering': '^',    # triângulo
        'activation_steering': 'D' # diamante
    }
    
    # Para cada método de steering
    for method in ['baseline', 'prompt_steering', 'activation_steering']:
        df_method = df[(df['author'] == author) & (df['condition'] == method)]
        if len(df_method) > 0:
            X_method = df_method[metric_cols].fillna(df_method[metric_cols].mean())
            method_pca = pca.transform(scaler.transform(X_method))
            method_mean = method_pca.mean(axis=0)
            
            # Desenhar linha do original para o método (sem seta)
            dx = method_mean[0] - orig_mean[0]
            dy = method_mean[1] - orig_mean[1]
            
            ax.plot([orig_mean[0], method_mean[0]], [orig_mean[1], method_mean[1]],
                    color=colors[author],
                    linestyle=styles[method]['linestyle'],
                    linewidth=styles[method]['linewidth'],
                    alpha=styles[method]['alpha'],
                    zorder=5)
            
            # Adicionar marker no ponto final
            ax.scatter(method_mean[0], method_mean[1], 
                      s=150, marker=markers[method], 
                      color=colors[author], edgecolor='black', 
                      linewidth=1.5, alpha=0.9, zorder=7)

# Configuração do gráfico
ax.set_xlabel(f'PC1 - Complexidade Linguística ({pca.explained_variance_ratio_[0]*100:.1f}% da variância)', 
             fontsize=13, fontweight='bold')
ax.set_ylabel(f'PC2 - Estilo Verbal/Nominal ({pca.explained_variance_ratio_[1]*100:.1f}% da variância)', 
             fontsize=13, fontweight='bold')
ax.set_title('Movimentação no Espaço PCA: Original → Métodos de Steering', 
            fontsize=16, fontweight='bold', pad=20)
ax.grid(alpha=0.3, linestyle='--')
ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
ax.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)

# Legenda combinada (autores + métodos)
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Autores
author_handles = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['lispector'], 
           markersize=10, markeredgecolor='black', markeredgewidth=1.5, label='Lispector'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['woolf'], 
           markersize=10, markeredgecolor='black', markeredgewidth=1.5, label='Woolf'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['wikipedia_pt'], 
           markersize=10, markeredgecolor='black', markeredgewidth=1.5, label='Wikipedia PT'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['wikipedia_eng'], 
           markersize=10, markeredgecolor='black', markeredgewidth=1.5, label='Wikipedia EN')
]

# Métodos (linhas + markers)
method_handles = [
    Line2D([0], [0], color='gray', linestyle='-', linewidth=2, alpha=0.7, 
           marker='s', markersize=8, markerfacecolor='gray', markeredgecolor='black', 
           markeredgewidth=1.5, label='Baseline'),
    Line2D([0], [0], color='gray', linestyle='--', linewidth=2, alpha=0.7,
           marker='^', markersize=8, markerfacecolor='gray', markeredgecolor='black', 
           markeredgewidth=1.5, label='Prompt Steering'),
    Line2D([0], [0], color='gray', linestyle=':', linewidth=2.5, alpha=0.7,
           marker='D', markersize=8, markerfacecolor='gray', markeredgecolor='black', 
           markeredgewidth=1.5, label='Activation Steering')
]

# Criar duas legendas stackadas no canto superior direito
legend1 = ax.legend(handles=method_handles, loc='upper right', title='Métodos', 
                   framealpha=0.95, facecolor='white', edgecolor='black', fontsize=10,
                   bbox_to_anchor=(1.0, 1.0))
ax.add_artist(legend1)

# Calcular posição para a segunda legenda logo abaixo
ax.legend(handles=author_handles, loc='upper right', title='Autores', 
         framealpha=0.95, facecolor='white', edgecolor='black', fontsize=10,
         bbox_to_anchor=(1.0, 0.68))

plt.tight_layout()

# Salvar
output_path = OUTPUT_DIR / '02_pca_all_methods.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Gráfico PCA consolidado salvo: {output_path}")

# Análise de deslocamentos
print("\n" + "="*80)
print("ANÁLISE DE DESLOCAMENTOS NO ESPAÇO PCA")
print("="*80 + "\n")

for author in sorted(df['author'].unique()):
    print(f"\n{author.upper().replace('_', ' ')}:")
    print("-" * 60)
    
    df_author_orig = df[(df['author'] == author) & (df['condition'] == 'original')]
    X_author_orig = df_author_orig[metric_cols].fillna(df_author_orig[metric_cols].mean())
    orig_pca = pca.transform(scaler.transform(X_author_orig))
    orig_mean = orig_pca.mean(axis=0)
    
    for method in ['baseline', 'prompt_steering', 'activation_steering']:
        df_method = df[(df['author'] == author) & (df['condition'] == method)]
        if len(df_method) > 0:
            X_method = df_method[metric_cols].fillna(df_method[metric_cols].mean())
            method_pca = pca.transform(scaler.transform(X_method))
            method_mean = method_pca.mean(axis=0)
            
            displacement = np.linalg.norm(method_mean - orig_mean)
            direction_pc1 = method_mean[0] - orig_mean[0]
            direction_pc2 = method_mean[1] - orig_mean[1]
            
            print(f"  {method:20s}: deslocamento = {displacement:.3f}")
            print(f"  {'':20s}  PC1: {direction_pc1:+.3f}, PC2: {direction_pc2:+.3f}")

plt.close()
