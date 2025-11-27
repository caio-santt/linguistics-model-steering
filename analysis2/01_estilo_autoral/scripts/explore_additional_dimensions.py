#!/usr/bin/env python3
"""
Exploração de Dimensões Adicionais e Métricas Individuais

Objetivo: Identificar PCs adicionais interpretáveis (PC3, PC4, PC5) e métricas 
individuais que tenham interpretação direta e diferenças significativas entre autores.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats

# Configuração visual
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

# Paths
BASE_DIR = Path(__file__).parent.parent
METRICS_FILE = BASE_DIR / "metrics_filtered/all_texts_filtered.csv"
OUTPUT_DIR = BASE_DIR / "analysis2"

print("=" * 80)
print("EXPLORAÇÃO: DIMENSÕES ADICIONAIS E MÉTRICAS INDIVIDUAIS")
print("=" * 80)

# Carregar dados
df = pd.read_csv(METRICS_FILE)
df_orig = df[df['condition'] == 'original'].copy()

metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df_orig.columns if col not in metadata_cols]

print(f"\n✓ {len(df_orig)} textos originais, {len(metric_cols)} métricas")

# ============================================================================
# PARTE 1: PCA COM 5 COMPONENTES
# ============================================================================
print("\n" + "=" * 80)
print("[1/3] ANÁLISE DE 5 COMPONENTES PRINCIPAIS")
print("=" * 80)

# Preparar dados
df_metrics = df_orig[metric_cols].copy()
df_metrics = df_metrics.fillna(df_metrics.mean())

scaler = StandardScaler()
metrics_scaled = scaler.fit_transform(df_metrics)

# PCA com 5 componentes
pca = PCA(n_components=5)
pca_coords = pca.fit_transform(metrics_scaled)

for i in range(5):
    df_orig[f'PC{i+1}'] = pca_coords[:, i]

var_explained = pca.explained_variance_ratio_

print("\nVariância explicada por componente:")
cumulative_var = 0
for i, var in enumerate(var_explained, 1):
    cumulative_var += var
    print(f"   PC{i}: {var*100:.2f}% (acumulado: {cumulative_var*100:.2f}%)")

# Loadings para todos os PCs
loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i}' for i in range(1, 6)],
    index=metric_cols
)

print("\n" + "-" * 80)
print("LOADINGS: Top 10 métricas por componente")
print("-" * 80)

for pc_idx in range(1, 6):
    pc_name = f'PC{pc_idx}'
    print(f"\n{pc_name} ({var_explained[pc_idx-1]*100:.2f}% da variância):")
    
    loadings_sorted = loadings[pc_name].abs().sort_values(ascending=False)
    for i, (metric, _) in enumerate(loadings_sorted.head(10).items(), 1):
        loading_val = loadings.loc[metric, pc_name]
        direction = "+" if loading_val > 0 else "-"
        print(f"   {i:2d}. {metric:40s} {direction}{abs(loading_val):.4f}")

loadings.to_csv(OUTPUT_DIR / "pca_loadings_5components.csv")
print(f"\n✓ Loadings salvos: pca_loadings_5components.csv")

# ============================================================================
# PARTE 2: TESTE DE SIGNIFICÂNCIA ESTATÍSTICA (ANOVA) PARA CADA MÉTRICA
# ============================================================================
print("\n" + "=" * 80)
print("[2/3] MÉTRICAS COM DIFERENÇAS ESTATISTICAMENTE SIGNIFICATIVAS")
print("=" * 80)
print("\n[Conceito] ANOVA (Analysis of Variance):")
print("Testa se as médias de uma métrica diferem significativamente entre autores.")
print("p-value < 0.05 = diferença estatisticamente significativa")
print()

# ANOVA para cada métrica
anova_results = []

for metric in metric_cols:
    # Separar dados por autor
    groups = [df_orig[df_orig['author'] == author][metric].dropna() 
              for author in df_orig['author'].unique()]
    
    # ANOVA
    f_stat, p_value = stats.f_oneway(*groups)
    
    # Calcular effect size (eta-squared)
    author_means = df_orig.groupby('author')[metric].mean()
    overall_mean = df_orig[metric].mean()
    
    ss_between = sum(len(df_orig[df_orig['author'] == author]) * 
                     (author_means[author] - overall_mean)**2 
                     for author in df_orig['author'].unique())
    ss_total = sum((df_orig[metric] - overall_mean)**2)
    
    eta_squared = ss_between / ss_total if ss_total > 0 else 0
    
    # CV inter-autor
    cv = author_means.std() / author_means.mean() if author_means.mean() != 0 else 0
    
    anova_results.append({
        'metric': metric,
        'f_statistic': f_stat,
        'p_value': p_value,
        'eta_squared': eta_squared,
        'cv': abs(cv),
        'significant': 'Sim' if p_value < 0.05 else 'Não',
        'type': 'Léxica' if metric.startswith('basic_') else 'Sintática'
    })

anova_df = pd.DataFrame(anova_results).sort_values('eta_squared', ascending=False)

print("Top 20 métricas com maior effect size (eta-squared):")
print("(eta² > 0.14 = efeito grande, > 0.06 = médio, > 0.01 = pequeno)")
print()
print(anova_df.head(20)[['metric', 'eta_squared', 'cv', 'p_value', 'significant', 'type']].to_string(index=False))

anova_df.to_csv(OUTPUT_DIR / "metrics_statistical_significance.csv", index=False)
print(f"\n✓ Resultados ANOVA salvos: metrics_statistical_significance.csv")

# ============================================================================
# PARTE 3: MÉTRICAS INDIVIDUAIS ALTAMENTE INTERPRETÁVEIS
# ============================================================================
print("\n" + "=" * 80)
print("[3/3] MÉTRICAS INDIVIDUAIS COM INTERPRETAÇÃO DIRETA")
print("=" * 80)
print("\nSelecionando métricas facilmente interpretáveis e significativas:")
print()

# Métricas interpretáveis candidatas
interpretable_metrics = {
    # Léxicas - básicas
    'basic_ttr': 'Riqueza vocabular (Type-Token Ratio)',
    'basic_avg_word_length': 'Tamanho médio de palavras',
    'basic_tokens_per_sentence_mean': 'Tamanho médio de frases',
    
    # UPOS - classes gramaticais principais
    'NOUN_prop': 'Densidade de substantivos',
    'VERB_prop': 'Densidade de verbos',
    'ADJ_prop': 'Densidade de adjetivos',
    'ADV_prop': 'Densidade de advérbios',
    'PRON_prop': 'Densidade de pronomes',
    'DET_prop': 'Densidade de determinantes',
    'ADP_prop': 'Densidade de preposições',
    'PROPN_prop': 'Densidade de nomes próprios',
    'PUNCT_prop': 'Densidade de pontuação',
    
    # DEPREL - relações sintáticas chave
    'nsubj_prop': 'Sujeitos (relação sujeito-verbo)',
    'obj_prop': 'Objetos diretos',
    'nmod_prop': 'Modificadores nominais',
    'amod_prop': 'Modificadores adjetivais',
    'advmod_prop': 'Modificadores adverbiais',
    'root_prop': 'Raízes sintáticas (orações principais)',
    'compound_prop': 'Compostos nominais',
    'case_prop': 'Marcadores de caso (preposições)',
    'det_prop': 'Determinantes',
    'cop_prop': 'Cópulas (verbos de ligação)',
    'aux_prop': 'Verbos auxiliares',
    'conj_prop': 'Conjunções coordenativas',
    'cc_prop': 'Coordenadores',
    'mark_prop': 'Marcadores de subordinação',
    'acl_prop': 'Cláusulas adjetivais',
    'advcl_prop': 'Cláusulas adverbiais',
    'appos_prop': 'Aposições',
    
    # Distâncias médias
    'mean_dependency_distance': 'Distância média de dependência (complexidade)',
    'VERB_md': 'Distância média dos verbos',
    'NOUN_md': 'Distância média dos substantivos',
}

# Filtrar apenas as que existem no dataset
available_interpretable = {k: v for k, v in interpretable_metrics.items() 
                          if k in metric_cols}

print(f"Métricas interpretáveis disponíveis: {len(available_interpretable)}")

# Verificar significância e effect size
interpretable_stats = anova_df[anova_df['metric'].isin(available_interpretable.keys())].copy()
interpretable_stats['description'] = interpretable_stats['metric'].map(available_interpretable)

# Filtrar apenas significativas com effect size relevante
significant_interpretable = interpretable_stats[
    (interpretable_stats['p_value'] < 0.05) & 
    (interpretable_stats['eta_squared'] > 0.1)  # Efeito médio/grande
].sort_values('eta_squared', ascending=False)

print(f"\nMétricas interpretáveis com diferença significativa (p<0.05, η²>0.1):")
print(f"Total: {len(significant_interpretable)}")
print()

for _, row in significant_interpretable.head(20).iterrows():
    print(f"• {row['metric']:40s} (η²={row['eta_squared']:.3f})")
    print(f"  → {row['description']}")
    
    # Mostrar valores por autor
    author_means = df_orig.groupby('author')[row['metric']].mean().sort_values(ascending=False)
    print(f"     Ranking: ", end="")
    for i, (author, value) in enumerate(author_means.items()):
        print(f"{author}={value:.3f}", end="  ")
    print("\n")

significant_interpretable.to_csv(OUTPUT_DIR / "significant_interpretable_metrics.csv", index=False)
print(f"✓ Métricas interpretáveis significativas salvas: significant_interpretable_metrics.csv")

# ============================================================================
# VISUALIZAÇÃO: PCs ADICIONAIS
# ============================================================================
print("\n" + "=" * 80)
print("VISUALIZAÇÕES: COMPONENTES ADICIONAIS")
print("=" * 80)

colors = {'lispector': '#E63946', 'woolf': '#457B9D', 
          'wikipedia_pt': '#F1A208', 'wikipedia_eng': '#2A9D8F'}

# PC3 vs PC4
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# PC1 vs PC2 (para referência)
ax = axes[0, 0]
for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    ax.scatter(df_author['PC1'], df_author['PC2'], 
               c=colors.get(author, 'gray'), label=author, 
               s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_xlabel(f'PC1 ({var_explained[0]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_ylabel(f'PC2 ({var_explained[1]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_title('PC1 vs PC2', fontsize=13, weight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# PC1 vs PC3
ax = axes[0, 1]
for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    ax.scatter(df_author['PC1'], df_author['PC3'], 
               c=colors.get(author, 'gray'), label=author, 
               s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_xlabel(f'PC1 ({var_explained[0]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_ylabel(f'PC3 ({var_explained[2]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_title('PC1 vs PC3', fontsize=13, weight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# PC2 vs PC3
ax = axes[1, 0]
for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    ax.scatter(df_author['PC2'], df_author['PC3'], 
               c=colors.get(author, 'gray'), label=author, 
               s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_xlabel(f'PC2 ({var_explained[1]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_ylabel(f'PC3 ({var_explained[2]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_title('PC2 vs PC3', fontsize=13, weight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# PC3 vs PC4
ax = axes[1, 1]
for author in df_orig['author'].unique():
    df_author = df_orig[df_orig['author'] == author]
    ax.scatter(df_author['PC3'], df_author['PC4'], 
               c=colors.get(author, 'gray'), label=author, 
               s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_xlabel(f'PC3 ({var_explained[2]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_ylabel(f'PC4 ({var_explained[3]*100:.1f}%)', fontsize=11, weight='bold')
ax.set_title('PC3 vs PC4', fontsize=13, weight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.suptitle('Componentes Principais Adicionais', fontsize=15, weight='bold', y=0.995)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pca_additional_components.png", dpi=150, bbox_inches='tight')
print(f"\n✓ Gráfico PCs adicionais salvo: pca_additional_components.png")

# ============================================================================
# SÍNTESE
# ============================================================================
print("\n" + "=" * 80)
print("SÍNTESE")
print("=" * 80)
print(f"""
Arquivos gerados:
  • pca_loadings_5components.csv - Loadings de PC1 a PC5
  • metrics_statistical_significance.csv - ANOVA para todas as métricas
  • significant_interpretable_metrics.csv - Métricas interpretáveis significativas
  • pca_additional_components.png - Visualização de PC3 e PC4

Achados principais:
  • Variância acumulada (5 PCs): {sum(var_explained)*100:.1f}%
  • Métricas interpretáveis significativas: {len(significant_interpretable)}
  • Effect size médio/grande (η²>0.1): {len(anova_df[anova_df['eta_squared'] > 0.1])} métricas

Próximo passo:
  Analisar interpretabilidade linguística de PC3, PC4 e PC5 se houver
  padrões claros de separação entre autores.
""")

print("=" * 80)
print("✅ EXPLORAÇÃO CONCLUÍDA")
print("=" * 80)
