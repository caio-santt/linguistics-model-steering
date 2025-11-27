#!/usr/bin/env python3
"""
Análise detalhada do PC3: Repetição vs. Diversidade Lexical

Objetivo: Entender como cada autor se comporta no eixo de variabilidade estilística.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuração
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "analysis2"

print("=" * 80)
print("ANÁLISE DETALHADA: PC3 - REPETIÇÃO VS. DIVERSIDADE")
print("=" * 80)

# Carregar dados originais com PC3
df = pd.read_csv(BASE_DIR / "metrics_filtered/all_texts_filtered.csv")
df_orig = df[df['condition'] == 'original'].copy()

# Recarregar loadings e dados de PCA
loadings = pd.read_csv(OUTPUT_DIR / "pca_loadings_5components.csv", index_col=0)

# Recalcular PCA para obter PC3
metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df_orig.columns if col not in metadata_cols]

df_metrics = df_orig[metric_cols].copy()
df_metrics = df_metrics.fillna(df_metrics.mean())

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

scaler = StandardScaler()
metrics_scaled = scaler.fit_transform(df_metrics)

pca = PCA(n_components=5)
pca_coords = pca.fit_transform(metrics_scaled)

df_orig['PC3'] = pca_coords[:, 2]

# ============================================================================
# ANÁLISE 1: DISTRIBUIÇÃO DE PC3 POR AUTOR
# ============================================================================
print("\n[1/4] DISTRIBUIÇÃO DE PC3 POR AUTOR")
print("=" * 80)

pc3_stats = df_orig.groupby('author')['PC3'].agg(['mean', 'std', 'min', 'max'])
pc3_stats = pc3_stats.sort_values('mean', ascending=False)

print("\nEstatísticas de PC3 por autor:")
print(pc3_stats)

print("\nInterpretação:")
print("  • Valores ALTOS (positivos) = Alta diversidade, poucas repetições")
print("  • Valores BAIXOS (negativos) = Baixa diversidade, muitas repetições")
print()

for author in pc3_stats.index:
    mean_val = pc3_stats.loc[author, 'mean']
    if mean_val > 0.5:
        profile = "ALTA DIVERSIDADE - textos variados, poucas fórmulas repetidas"
    elif mean_val > 0:
        profile = "Diversidade moderada-alta"
    elif mean_val > -0.5:
        profile = "Diversidade moderada-baixa"
    else:
        profile = "BAIXA DIVERSIDADE - textos formulaicos, muitas repetições"
    
    print(f"  {author:20s} (PC3={mean_val:+.3f}): {profile}")

# ============================================================================
# ANÁLISE 2: MÉTRICAS INDIVIDUAIS QUE COMPÕEM PC3
# ============================================================================
print("\n" + "=" * 80)
print("[2/4] MÉTRICAS QUE MAIS CONTRIBUEM PARA PC3")
print("=" * 80)

pc3_loadings = loadings['PC3'].abs().sort_values(ascending=False).head(10)

print("\nTop 10 métricas (loadings absolutos):")
for i, (metric, loading) in enumerate(pc3_loadings.items(), 1):
    direction = "+" if loadings.loc[metric, 'PC3'] > 0 else "-"
    print(f"  {i:2d}. {metric:40s} {direction}{abs(loadings.loc[metric, 'PC3']):.4f}")

print("\n[Interpretação dos sinais]")
print("  (+) Contribui para ALTA diversidade")
print("  (-) Contribui para BAIXA diversidade (alta repetição)")

# Analisar valores reais das métricas-chave
print("\n" + "-" * 80)
print("VALORES REAIS DAS MÉTRICAS-CHAVE POR AUTOR")
print("-" * 80)

key_metrics = [
    'basic_n_unique_bigrams',
    'basic_n_repeated_bigrams', 
    'basic_n_repeated_trigrams',
    'basic_n_unique_trigrams',
    'basic_ttr'
]

for metric in key_metrics:
    if metric not in df_orig.columns:
        continue
    
    print(f"\n{metric}:")
    metric_stats = df_orig.groupby('author')[metric].agg(['mean', 'std'])
    metric_stats = metric_stats.sort_values('mean', ascending=False)
    
    for author in metric_stats.index:
        mean_val = metric_stats.loc[author, 'mean']
        std_val = metric_stats.loc[author, 'std']
        print(f"  {author:20s} {mean_val:8.2f} ± {std_val:6.2f}")

# ============================================================================
# ANÁLISE 3: VISUALIZAÇÕES
# ============================================================================
print("\n" + "=" * 80)
print("[3/4] GERANDO VISUALIZAÇÕES")
print("=" * 80)

colors = {'lispector': '#E63946', 'woolf': '#457B9D', 
          'wikipedia_pt': '#F1A208', 'wikipedia_eng': '#2A9D8F'}

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Subplot 1: Boxplot de PC3 por autor
ax = axes[0, 0]
author_order = pc3_stats.index.tolist()
data_for_box = [df_orig[df_orig['author'] == author]['PC3'].values 
                for author in author_order]

bp = ax.boxplot(data_for_box, labels=author_order, patch_artist=True)
for patch, author in zip(bp['boxes'], author_order):
    patch.set_facecolor(colors.get(author, 'gray'))
    patch.set_alpha(0.7)

ax.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Zero (neutro)')
ax.set_ylabel('PC3 (Repetição ← → Diversidade)', fontsize=12, weight='bold')
ax.set_title('Distribuição de PC3 por Autor', fontsize=13, weight='bold')
ax.grid(True, alpha=0.3)
ax.legend()

# Subplot 2: PC1 vs PC3 (Complexidade vs Diversidade)
ax = axes[0, 1]
df_orig['PC1'] = pca_coords[:, 0]

for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    ax.scatter(df_author['PC1'], df_author['PC3'], 
               c=colors.get(author, 'gray'), label=author,
               s=100, alpha=0.7, edgecolors='black', linewidth=0.5)

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('PC1 (Complexidade Sintática)', fontsize=11, weight='bold')
ax.set_ylabel('PC3 (Diversidade Lexical)', fontsize=11, weight='bold')
ax.set_title('PC1 vs PC3', fontsize=13, weight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Subplot 3: PC2 vs PC3 (Verbal/Nominal vs Diversidade)
ax = axes[1, 0]
df_orig['PC2'] = pca_coords[:, 1]

for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    ax.scatter(df_author['PC2'], df_author['PC3'], 
               c=colors.get(author, 'gray'), label=author,
               s=100, alpha=0.7, edgecolors='black', linewidth=0.5)

ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('PC2 (Verbal ← → Nominal)', fontsize=11, weight='bold')
ax.set_ylabel('PC3 (Diversidade Lexical)', fontsize=11, weight='bold')
ax.set_title('PC2 vs PC3', fontsize=13, weight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Subplot 4: TTR por autor (métrica-chave do PC3)
ax = axes[1, 1]

if 'basic_ttr' in df_orig.columns:
    ttr_stats = df_orig.groupby('author')['basic_ttr'].agg(['mean', 'std'])
    ttr_stats = ttr_stats.sort_values('mean', ascending=False)
    
    x_pos = np.arange(len(ttr_stats))
    bars = ax.bar(x_pos, ttr_stats['mean'], 
                   yerr=ttr_stats['std'],
                   color=[colors.get(author, 'gray') for author in ttr_stats.index],
                   alpha=0.7, edgecolor='black', linewidth=1.5,
                   capsize=5)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(ttr_stats.index, rotation=0)
    ax.set_ylabel('Type-Token Ratio (TTR)', fontsize=11, weight='bold')
    ax.set_title('Riqueza Vocabular por Autor', fontsize=13, weight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores
    for i, (idx, row) in enumerate(ttr_stats.iterrows()):
        ax.text(i, row['mean'] + 0.01, f"{row['mean']:.3f}", 
                ha='center', va='bottom', fontsize=10, weight='bold')

plt.suptitle('Análise Detalhada: PC3 - Repetição vs. Diversidade Lexical', 
             fontsize=15, weight='bold', y=0.995)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pc3_detailed_analysis.png", dpi=150, bbox_inches='tight')
print("✓ Gráfico salvo: pc3_detailed_analysis.png")

# ============================================================================
# ANÁLISE 4: INTERPRETAÇÃO LINGUÍSTICA
# ============================================================================
print("\n" + "=" * 80)
print("[4/4] INTERPRETAÇÃO LINGUÍSTICA POR AUTOR")
print("=" * 80)

print("\n" + "─" * 80)
for author in pc3_stats.index:
    pc3_mean = pc3_stats.loc[author, 'mean']
    
    # Obter métricas relevantes
    author_data = df_orig[df_orig['author'] == author]
    ttr = author_data['basic_ttr'].mean() if 'basic_ttr' in author_data.columns else None
    unique_bi = author_data['basic_n_unique_bigrams'].mean() if 'basic_n_unique_bigrams' in author_data.columns else None
    repeated_bi = author_data['basic_n_repeated_bigrams'].mean() if 'basic_n_repeated_bigrams' in author_data.columns else None
    
    print(f"\n{author.upper()}")
    print(f"PC3: {pc3_mean:+.3f}")
    
    if ttr:
        print(f"TTR: {ttr:.3f}")
    if unique_bi and repeated_bi:
        ratio = unique_bi / repeated_bi if repeated_bi > 0 else float('inf')
        print(f"Bigramas únicos/repetidos: {unique_bi:.0f}/{repeated_bi:.0f} = {ratio:.2f}x")
    
    print("\nInterpretação:")
    
    if author == 'lispector':
        if pc3_mean > 0:
            print("  Lispector tem ALTA DIVERSIDADE nas combinações de palavras.")
            print("  Apesar de usar frases curtas, cada frase é construída de forma única.")
            print("  Não repete fórmulas - cada pensamento é expresso de maneira singular.")
        else:
            print("  Lispector REPETE PADRÕES nas combinações de palavras.")
            print("  O estilo fragmentado pode levar a estruturas recorrentes.")
    
    elif author == 'woolf':
        if pc3_mean > 0:
            print("  Woolf tem ALTA DIVERSIDADE nas combinações, apesar da repetição de palavras.")
            print("  TTR baixo (repete palavras), mas combina de formas sempre diferentes.")
            print("  Cada frase complexa é construída de maneira única.")
        else:
            print("  Woolf REPETE PADRÕES nas combinações de palavras.")
            print("  O estilo de fluxo de consciência pode gerar estruturas recorrentes.")
    
    elif 'wikipedia' in author:
        if pc3_mean > 0:
            print("  Wikipedia tem ALTA DIVERSIDADE nas combinações.")
            print("  Textos enciclopédicos cobrem tópicos variados com vocabulário específico.")
            print("  Cada artigo usa terminologia própria do seu domínio.")
        else:
            print("  Wikipedia REPETE PADRÕES nas combinações de palavras.")
            print("  Textos enciclopédicos seguem fórmulas estruturais recorrentes.")
            print("  Mesmas construções explicativas aparecem repetidamente.")
    
    print("─" * 80)

# ============================================================================
# SÍNTESE
# ============================================================================
print("\n" + "=" * 80)
print("SÍNTESE: O QUE PC3 REVELA")
print("=" * 80)

print("""
PC3 captura uma dimensão diferente de PC1 (complexidade) e PC2 (verbal/nominal):

PC3 mede VARIABILIDADE ESTILÍSTICA:
  • Autores com PC3 alto constroem cada frase/ideia de forma única
  • Autores com PC3 baixo reutilizam fórmulas e padrões estruturais

Isso é INDEPENDENTE de:
  • Complexidade sintática (PC1) - você pode ser complexo E repetitivo
  • Estilo verbal/nominal (PC2) - você pode ser verbal E repetitivo

Diferença de TTR vs PC3:
  • TTR mede repetição de PALAVRAS individuais
  • PC3 mede repetição de COMBINAÇÕES de palavras (bigramas/trigramas)
  
Exemplo: Woolf tem TTR baixo (repete palavras como "she", "her") mas pode ter
PC3 alto se essas palavras forem sempre combinadas de formas diferentes.

Arquivo gerado:
  • pc3_detailed_analysis.png - Visualizações completas do PC3
""")

print("=" * 80)
print("✅ ANÁLISE PC3 CONCLUÍDA")
print("=" * 80)
