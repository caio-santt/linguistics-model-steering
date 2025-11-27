"""
Visualização das 3 métricas-chave dos textos originais.
Padrão consistente com as comparações baseline/prompt/activation.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'plots'

# Carregar dados originais
df = pd.read_csv("../../metrics_filtered/all_texts_filtered.csv")
df_orig = df[df['condition'] == 'original'].copy()

# Métricas-chave (mesmas das outras análises)
metrics = {
    'basic_ttr': 'Riqueza Vocabular (TTR)',
    'basic_tokens_per_sentence_mean': 'Tamanho de Frases',
    'synt_UPOS_PRON_prop': 'Densidade de Pronomes'
}

# Cores por autor (padrão estabelecido)
colors = {
    'lispector': '#E63946',      # vermelho
    'woolf': '#457B9D',          # azul
    'wikipedia_pt': '#F1A208',   # laranja
    'wikipedia_eng': '#2A9D8F'   # verde-azulado
}

# Criar figura com 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (metric_key, metric_name) in enumerate(metrics.items()):
    ax = axes[idx]
    stats = df_orig.groupby('author')[metric_key].agg(['mean', 'std', 'count']).reset_index()
    authors = sorted(df_orig['author'].unique())
    x = np.arange(len(authors))
    width = 0.6  # Barra mais larga já que é única
    
    for i, author in enumerate(authors):
        val = stats[stats['author'] == author]['mean'].values[0]
        std = stats[stats['author'] == author]['std'].values[0]
        n = stats[stats['author'] == author]['count'].values[0]
        
        # Usar erro padrão da média (SEM)
        sem = std / np.sqrt(n)
        
        ax.bar(x[i], val, width, yerr=sem,
               color=colors[author], alpha=0.7, edgecolor='black', 
               linewidth=1.5, capsize=4)
    
    # Configuração do subplot
    ax.set_title(metric_name, fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([a.replace('_', ' ').title() for a in authors], 
                       rotation=20, ha='right', fontsize=11)
    ax.set_ylabel('Valor', fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.suptitle('Perfil Estilístico dos Autores - Textos Originais', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

# Salvar
output_path = OUTPUT_DIR / '01_key_metrics_original.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Gráfico salvo: {output_path.name}")

# Mostrar valores
print("\n" + "="*70)
print("VALORES MÉDIOS - TEXTOS ORIGINAIS")
print("="*70 + "\n")

for metric_key, metric_name in metrics.items():
    print(f"{metric_name}:")
    stats = df_orig.groupby('author')[metric_key].agg(['mean', 'std', 'count'])
    for author in sorted(df_orig['author'].unique()):
        mean_val = stats.loc[author, 'mean']
        std_val = stats.loc[author, 'std']
        n_val = stats.loc[author, 'count']
        sem_val = std_val / np.sqrt(n_val)
        print(f"  {author:20s} {mean_val:7.3f} ± {sem_val:.3f}")
    print()

plt.close()
