#!/usr/bin/env python3
"""
Análise Exploratória: Perfis Estilísticos Autorais

Objetivo: Caracterizar o estilo linguístico de cada autor através dos textos originais.
Abordagem livre e exploratória, focando em interpretação linguística acessível.

Pergunta: Como cada autor se distingue linguisticamente? Quais padrões léxicos e 
sintáticos definem sua "assinatura estilística"?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Configuração visual
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Paths
BASE_DIR = Path(__file__).parent.parent
# analysis2/01_estilo_autoral/scripts -> linguistics_and_model_steering/metrics_filtered
METRICS_FILE = BASE_DIR.parent.parent / "metrics_filtered" / "all_texts_filtered.csv"
OUTPUT_DIR = BASE_DIR / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("ANÁLISE EXPLORATÓRIA: PERFIS ESTILÍSTICOS AUTORAIS")
print("=" * 80)
print("\nPergunta: Como cada autor se distingue linguisticamente?")
print("Dados: Textos originais (60 amostras, 4 autores)")
print("Métricas: 65 filtradas (léxicas + sintáticas)")
print()

# Carregar apenas textos originais
print("[1/6] Carregando dados originais...")
df = pd.read_csv(METRICS_FILE)
df_orig = df[df['condition'] == 'original'].copy()

metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df_orig.columns if col not in metadata_cols]

print(f"   ✓ {len(df_orig)} textos originais")
print(f"   ✓ {len(metric_cols)} métricas")
print(f"   ✓ Autores: {df_orig['author'].unique().tolist()}")

# Separar métricas por tipo
lexical_metrics = [m for m in metric_cols if m.startswith('basic_')]
syntactic_metrics = [m for m in metric_cols if not m.startswith('basic_')]

print(f"\n   • {len(lexical_metrics)} métricas léxicas")
print(f"   • {len(syntactic_metrics)} métricas sintáticas")

# ============================================================================
# PARTE 1: ESTATÍSTICAS DESCRITIVAS POR AUTOR
# ============================================================================
print("\n" + "=" * 80)
print("[2/6] ESTATÍSTICAS DESCRITIVAS POR AUTOR")
print("=" * 80)

author_stats = []
for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    
    # Estatísticas gerais
    stats = {
        'author': author,
        'n_texts': len(df_author),
        'lang': df_author['lang'].iloc[0]
    }
    
    # Médias das métricas léxicas (mais interpretáveis)
    for metric in lexical_metrics:
        stats[f'{metric}_mean'] = df_author[metric].mean()
        stats[f'{metric}_std'] = df_author[metric].std()
    
    author_stats.append(stats)

stats_df = pd.DataFrame(author_stats)
print("\nMétricas Léxicas Médias por Autor:")
print(stats_df.to_string(index=False))

# ============================================================================
# PARTE 2: VARIABILIDADE INTER-AUTOR (COEFICIENTE DE VARIAÇÃO)
# ============================================================================
print("\n" + "=" * 80)
print("[3/6] MÉTRICAS MAIS DISCRIMINATIVAS (Alta variabilidade entre autores)")
print("=" * 80)
print("\n[Conceito] Coeficiente de Variação (CV) = std/mean")
print("CV alto = métrica varia muito entre autores = boa para distinguir estilos")
print()

# Calcular CV inter-autor para cada métrica
cv_scores = []
for metric in metric_cols:
    # Média por autor
    author_means = df_orig.groupby('author')[metric].mean()
    
    # CV entre autores
    cv = author_means.std() / author_means.mean() if author_means.mean() != 0 else 0
    
    cv_scores.append({
        'metric': metric,
        'cv': abs(cv),
        'type': 'Léxica' if metric.startswith('basic_') else 'Sintática'
    })

cv_df = pd.DataFrame(cv_scores).sort_values('cv', ascending=False)

print("Top 15 métricas mais discriminativas:")
print(cv_df.head(15).to_string(index=False))

# Salvar
cv_df.to_csv(OUTPUT_DIR / "discriminative_metrics.csv", index=False)

# ============================================================================
# PARTE 3: PCA - REDUÇÃO DIMENSIONAL
# ============================================================================
print("\n" + "=" * 80)
print("[4/6] PCA - VISUALIZAÇÃO DO ESPAÇO ESTILÍSTICO")
print("=" * 80)
print("\n[Conceito] PCA (Principal Component Analysis):")
print("Reduz 65 dimensões (métricas) para 2 dimensões visualizáveis.")
print("PC1 e PC2 capturam as direções de maior variação nos dados.")
print("Autores próximos no gráfico = estilos similares.")
print()

# Normalizar métricas (tratar NaN: preencher com média da coluna)
df_metrics = df_orig[metric_cols].copy()
df_metrics = df_metrics.fillna(df_metrics.mean())

scaler = StandardScaler()
metrics_scaled = scaler.fit_transform(df_metrics)

# PCA
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(metrics_scaled)

df_orig['PC1'] = pca_coords[:, 0]
df_orig['PC2'] = pca_coords[:, 1]

var_explained = pca.explained_variance_ratio_
print(f"Variância explicada:")
print(f"   • PC1: {var_explained[0]*100:.2f}%")
print(f"   • PC2: {var_explained[1]*100:.2f}%")
print(f"   • Total: {var_explained.sum()*100:.2f}%")

# Plot PCA
fig, ax = plt.subplots(figsize=(10, 8))

colors = {'lispector': '#E63946', 'woolf': '#457B9D', 
          'wikipedia_pt': '#F1A208', 'wikipedia_eng': '#2A9D8F'}

for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    ax.scatter(df_author['PC1'], df_author['PC2'], 
               c=colors.get(author, 'gray'), label=author, 
               s=100, alpha=0.7, edgecolors='black', linewidth=0.5)

ax.set_xlabel(f'PC1 - Complexidade Linguística ({var_explained[0]*100:.1f}% da variância)', fontsize=12, weight='bold')
ax.set_ylabel(f'PC2 - Estilo Verbal/Nominal ({var_explained[1]*100:.1f}% da variância)', fontsize=12, weight='bold')
ax.set_title('Espaço Estilístico dos Autores (PCA)', fontsize=14, weight='bold', pad=20)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pca_author_styles.png", dpi=150, bbox_inches='tight')
print(f"\n✓ Gráfico PCA salvo: analysis2/pca_author_styles.png")

# ============================================================================
# PARTE 4: LOADINGS DO PCA (Quais métricas contribuem para PC1/PC2?)
# ============================================================================
print("\n" + "=" * 80)
print("[5/6] INTERPRETAÇÃO DOS COMPONENTES PRINCIPAIS")
print("=" * 80)
print("\n[Conceito] Loadings:")
print("Mostram quais métricas originais mais contribuem para cada PC.")
print("Loading alto (positivo ou negativo) = métrica importante para aquela dimensão.")
print()

# Extrair loadings
loadings = pd.DataFrame(
    pca.components_.T,
    columns=['PC1', 'PC2'],
    index=metric_cols
)

# Top 10 métricas para PC1
print("Top 10 métricas que mais contribuem para PC1:")
loadings_pc1 = loadings['PC1'].abs().sort_values(ascending=False)
for i, (metric, loading) in enumerate(loadings_pc1.head(10).items(), 1):
    direction = "+" if loadings.loc[metric, 'PC1'] > 0 else "-"
    print(f"   {i}. {metric}: {direction}{abs(loadings.loc[metric, 'PC1']):.4f}")

print("\nTop 10 métricas que mais contribuem para PC2:")
loadings_pc2 = loadings['PC2'].abs().sort_values(ascending=False)
for i, (metric, loading) in enumerate(loadings_pc2.head(10).items(), 1):
    direction = "+" if loadings.loc[metric, 'PC2'] > 0 else "-"
    print(f"   {i}. {metric}: {direction}{abs(loadings.loc[metric, 'PC2']):.4f}")

loadings.to_csv(OUTPUT_DIR / "pca_loadings.csv")

# ============================================================================
# PARTE 5: PERFIS AUTORAIS DETALHADOS (Top métricas discriminativas)
# ============================================================================
print("\n" + "=" * 80)
print("[6/6] PERFIS LINGUÍSTICOS DETALHADOS")
print("=" * 80)
print("\nUsando as 10 métricas mais discriminativas para caracterizar cada autor:")
print()

top_metrics = cv_df.head(10)['metric'].tolist()

profiles = []
for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    
    profile = {'author': author}
    for metric in top_metrics:
        profile[metric] = df_author[metric].mean()
    
    profiles.append(profile)

profiles_df = pd.DataFrame(profiles)

# Normalizar para comparação (z-score)
profiles_normalized = profiles_df.copy()
for metric in top_metrics:
    mean = profiles_df[metric].mean()
    std = profiles_df[metric].std()
    if std > 0:
        profiles_normalized[metric] = (profiles_df[metric] - mean) / std

print("\nPerfis Normalizados (z-scores):")
print("[z > 0 = acima da média, z < 0 = abaixo da média]")
print(profiles_normalized.to_string(index=False))

profiles_normalized.to_csv(OUTPUT_DIR / "author_profiles_normalized.csv", index=False)

# Heatmap dos perfis
fig, ax = plt.subplots(figsize=(14, 6))
profiles_matrix = profiles_normalized.set_index('author').T

sns.heatmap(profiles_matrix, annot=True, fmt='.2f', cmap='RdBu_r', 
            center=0, cbar_kws={'label': 'Z-score'}, ax=ax, linewidths=0.5)

ax.set_xlabel('Autor', fontsize=12, weight='bold')
ax.set_ylabel('Métrica', fontsize=12, weight='bold')
ax.set_title('Perfis Estilísticos (Top 10 Métricas Discriminativas)', 
             fontsize=14, weight='bold', pad=20)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "author_profiles_heatmap.png", dpi=150, bbox_inches='tight')
print(f"\n✓ Heatmap de perfis salvo: analysis2/author_profiles_heatmap.png")

# ============================================================================
# SÍNTESE
# ============================================================================
print("\n" + "=" * 80)
print("SÍNTESE")
print("=" * 80)
print(f"""
Arquivos gerados em analysis2/:
  • discriminative_metrics.csv - Métricas rankeadas por poder discriminativo
  • pca_author_styles.png - Visualização do espaço estilístico (2D)
  • pca_loadings.csv - Contribuições das métricas para PC1 e PC2
  • author_profiles_normalized.csv - Perfis quantitativos dos autores
  • author_profiles_heatmap.png - Perfis visualizados como heatmap

Próximos passos sugeridos:
  1. Interpretar linguisticamente os clusters do PCA
  2. Analisar métricas léxicas vs sintáticas separadamente
  3. Comparar literário (Lispector/Woolf) vs enciclopédico (Wikipedia)
  4. Investigar métricas com loadings altos nos PCs
""")

print("=" * 80)
print("✅ ANÁLISE CONCLUÍDA")
print("=" * 80)
