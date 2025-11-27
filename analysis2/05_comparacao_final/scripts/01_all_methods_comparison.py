"""
Comparação consolidada: Original vs Todos os Métodos de Steering
Visualização unificada das 3 métricas-chave
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Criar diretórios
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'plots'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Carregar dados
df = pd.read_csv("../../metrics_filtered/all_texts_filtered.csv")

# Filtrar condições relevantes
conditions = ['original', 'baseline', 'prompt_steering', 'activation_steering']
df_comp = df[df['condition'].isin(conditions)].copy()

# Métricas padronizadas
metrics = {
    'basic_ttr': 'Riqueza Vocabular (TTR)',
    'basic_tokens_per_sentence_mean': 'Tamanho de Frases',
    'synt_UPOS_PRON_prop': 'Densidade de Pronomes'
}

# Cores por autor
colors = {
    'lispector': '#E63946',
    'woolf': '#457B9D',
    'wikipedia_pt': '#F1A208',
    'wikipedia_eng': '#2A9D8F'
}

# Padrões de hachura para cada método
hatches = {
    'original': '',
    'baseline': '///',
    'prompt_steering': '\\\\\\',
    'activation_steering': 'xxx'
}

# Labels mais curtos para legenda
labels = {
    'original': 'Original',
    'baseline': 'Baseline',
    'prompt_steering': 'Prompt Steering',
    'activation_steering': 'Activation Steering'
}

# Criar figura com 3 subplots (um por métrica)
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

for idx, (metric_key, metric_name) in enumerate(metrics.items()):
    ax = axes[idx]
    stats = df_comp.groupby(['author', 'condition'])[metric_key].agg(['mean', 'std', 'count']).reset_index()
    
    authors = sorted(df_comp['author'].unique())
    n_authors = len(authors)
    n_conditions = len(conditions)
    
    # Configuração das barras
    bar_width = 0.18
    x = np.arange(n_authors)
    
    # Para cada condição, desenhar barras de todos os autores
    for cond_idx, condition in enumerate(conditions):
        positions = x + (cond_idx - n_conditions/2 + 0.5) * bar_width
        
        for i, author in enumerate(authors):
            val = stats[(stats['author'] == author) & (stats['condition'] == condition)]['mean'].values
            std_val = stats[(stats['author'] == author) & (stats['condition'] == condition)]['std'].values
            n_val = stats[(stats['author'] == author) & (stats['condition'] == condition)]['count'].values
            
            if len(val) > 0:
                val = val[0]
                std_val = std_val[0]
                n_val = n_val[0]
                sem = std_val / np.sqrt(n_val)
                
                # Determinar alpha e edge
                if condition == 'original':
                    alpha = 0.8
                    edgecolor = 'black'
                    linewidth = 1.5
                else:
                    alpha = 0.5
                    edgecolor = 'black'
                    linewidth = 1.2
                
                ax.bar(positions[i], val, bar_width, yerr=sem,
                       color=colors[author], alpha=alpha, 
                       edgecolor=edgecolor, linewidth=linewidth,
                       hatch=hatches[condition], capsize=3)
    
    # Configuração do subplot
    ax.set_title(metric_name, fontsize=15, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([a.replace('_', ' ').title() for a in authors], 
                       rotation=20, ha='right', fontsize=11)
    ax.set_ylabel('Valor', fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.suptitle('Comparação Consolidada: Original vs Métodos de Steering', 
             fontsize=17, fontweight='bold', y=1.00)

# Criar handles para a legenda (pegar do último loop)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='gray', edgecolor='black', linewidth=1.5, alpha=0.8, label='Original'),
    Patch(facecolor='gray', edgecolor='black', linewidth=1.2, alpha=0.5, hatch='///', label='Baseline'),
    Patch(facecolor='gray', edgecolor='black', linewidth=1.2, alpha=0.5, hatch='\\\\\\', label='Prompt Steering'),
    Patch(facecolor='gray', edgecolor='black', linewidth=1.2, alpha=0.5, hatch='xxx', label='Activation Steering')
]
fig.legend(handles=legend_elements, loc='upper right', framealpha=0.95, fontsize=10, 
           facecolor='white', edgecolor='black', bbox_to_anchor=(0.995, 0.88))

plt.tight_layout()

# Salvar
output_path = OUTPUT_DIR / '01_all_methods_comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Gráfico salvo: {output_path}")

# Mostrar estatísticas resumidas
print("\n" + "="*80)
print("RESUMO COMPARATIVO - MUDANÇAS PERCENTUAIS EM RELAÇÃO AO ORIGINAL")
print("="*80 + "\n")

for metric_key, metric_name in metrics.items():
    print(f"{metric_name}:")
    print(f"{'':20s} {'Baseline':>12s} {'Prompt':>12s} {'Activation':>12s}")
    print("-" * 60)
    
    # Recalcular stats para esta métrica específica
    metric_stats = df_comp.groupby(['author', 'condition'])[metric_key].agg(['mean', 'std', 'count']).reset_index()
    
    for author in sorted(df_comp['author'].unique()):
        orig_val = metric_stats[(metric_stats['author'] == author) & (metric_stats['condition'] == 'original')]['mean'].values[0]
        
        changes = []
        for cond in ['baseline', 'prompt_steering', 'activation_steering']:
            cond_val = metric_stats[(metric_stats['author'] == author) & (metric_stats['condition'] == cond)]['mean'].values
            if len(cond_val) > 0:
                change = ((cond_val[0] - orig_val) / orig_val) * 100
                changes.append(f"{change:+.1f}%")
            else:
                changes.append("N/A")
        
        print(f"  {author:18s} {changes[0]:>12s} {changes[1]:>12s} {changes[2]:>12s}")
    print()

plt.close()
