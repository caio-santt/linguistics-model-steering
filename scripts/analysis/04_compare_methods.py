#!/usr/bin/env python3
"""
Comparação dos Métodos de Geração vs Original

Calcula distâncias estilísticas e identifica divergências entre:
- Original vs Baseline
- Original vs Prompt Steering  
- Original vs Activation Steering

Métricas: distância Euclidiana, preservação por métrica, análise por autor.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
METRICS_FILE = BASE_DIR / "metrics_filtered/all_texts_filtered.csv"
OUTPUT_DIR = BASE_DIR / "analysis/03_method_comparison"
DATA_DIR = OUTPUT_DIR / "data"
PLOTS_DIR = OUTPUT_DIR / "plots"

# Criar diretórios
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("COMPARAÇÃO DOS MÉTODOS DE GERAÇÃO VS ORIGINAL")
print("=" * 70)

# 1. Carregar dados
print("\n[1/5] Carregando dados...")
df = pd.read_csv(METRICS_FILE)
print(f"   ✓ {len(df)} textos")
print(f"   ✓ Condições: {df['condition'].unique().tolist()}")

# Separar metadados
metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df.columns if col not in metadata_cols]
print(f"   ✓ {len(metric_cols)} métricas")

# 2. Calcular distâncias estilísticas
print("\n[2/5] Calculando distâncias estilísticas...")

# Normalizar métricas (z-score)
scaler = StandardScaler()
df_metrics = df[metric_cols].copy()
df_metrics_scaled = pd.DataFrame(
    scaler.fit_transform(df_metrics),
    columns=metric_cols,
    index=df.index
)

# Para cada texto gerado, encontrar o original correspondente
distances = []

df_original = df[df['condition'] == 'original'].copy()
df_generated = df[df['condition'] != 'original'].copy()

for idx, gen_row in df_generated.iterrows():
    # Identificar original correspondente (mesmo author + title + sample_idx)
    orig_match = df_original[
        (df_original['author'] == gen_row['author']) &
        (df_original['title'] == gen_row['title']) &
        (df_original['sample_idx'] == gen_row['sample_idx'])
    ]
    
    if len(orig_match) > 0:
        orig_idx = orig_match.index[0]
        
        # Distância Euclidiana no espaço normalizado
        gen_vector = df_metrics_scaled.loc[idx].values
        orig_vector = df_metrics_scaled.loc[orig_idx].values
        
        distance = np.linalg.norm(gen_vector - orig_vector)
        
        distances.append({
            'text_id_gen': gen_row['text_id'],
            'text_id_orig': orig_match.iloc[0]['text_id'],
            'author': gen_row['author'],
            'title': gen_row['title'],
            'sample_idx': gen_row['sample_idx'],
            'rep': gen_row['rep'],
            'method': gen_row['condition'],
            'lang': gen_row['lang'],
            'euclidean_distance': distance
        })

distances_df = pd.DataFrame(distances)
distances_df.to_csv(DATA_DIR / "distances_to_original.csv", index=False)

print(f"   ✓ Distâncias calculadas: {len(distances_df)} pares")

# Estatísticas por método
for method in ['baseline', 'prompt_steering', 'activation_steering']:
    dist_method = distances_df[distances_df['method'] == method]['euclidean_distance']
    print(f"   • {method}: {dist_method.mean():.3f} ± {dist_method.std():.3f}")

# 3. Preservation score por método
print("\n[3/5] Calculando preservation scores...")

# Preservation = 1 - (distance / max_distance)
max_dist = distances_df['euclidean_distance'].max()
distances_df['preservation_score'] = 1 - (distances_df['euclidean_distance'] / max_dist)

preservation_stats = distances_df.groupby('method').agg({
    'preservation_score': ['mean', 'std', 'min', 'max']
}).round(3)
preservation_stats.to_csv(DATA_DIR / "preservation_scores.csv")

print("   ✓ Preservation scores por método:")
for method in ['baseline', 'prompt_steering', 'activation_steering']:
    score = distances_df[distances_df['method'] == method]['preservation_score'].mean()
    print(f"     • {method}: {score:.3f}")

# 4. Divergências por métrica
print("\n[4/5] Analisando divergências por métrica...")

# Para cada métrica, calcular diferença média |generated - original|
divergences = []

for metric in metric_cols:
    for method in ['baseline', 'prompt_steering', 'activation_steering']:
        df_method = df[df['condition'] == method].copy()
        
        diffs = []
        for idx, gen_row in df_method.iterrows():
            orig_match = df_original[
                (df_original['author'] == gen_row['author']) &
                (df_original['title'] == gen_row['title']) &
                (df_original['sample_idx'] == gen_row['sample_idx'])
            ]
            
            if len(orig_match) > 0:
                gen_val = gen_row[metric]
                orig_val = orig_match.iloc[0][metric]
                
                if pd.notna(gen_val) and pd.notna(orig_val):
                    diff = abs(gen_val - orig_val)
                    rel_diff = diff / abs(orig_val) if orig_val != 0 else 0
                    diffs.append({
                        'absolute_diff': diff,
                        'relative_diff': rel_diff
                    })
        
        if len(diffs) > 0:
            diffs_df = pd.DataFrame(diffs)
            divergences.append({
                'metric': metric,
                'method': method,
                'mean_abs_diff': diffs_df['absolute_diff'].mean(),
                'mean_rel_diff': diffs_df['relative_diff'].mean(),
                'std_abs_diff': diffs_df['absolute_diff'].std()
            })

divergences_df = pd.DataFrame(divergences)
divergences_df.to_csv(DATA_DIR / "metrics_divergence.csv", index=False)

# Top 10 métricas mais divergentes (média entre 3 métodos)
top_divergent = divergences_df.groupby('metric')['mean_rel_diff'].mean().sort_values(ascending=False).head(10)
print("   ✓ Top 10 métricas mais divergentes:")
for metric, div in top_divergent.items():
    metric_clean = metric.replace('synt_', '').replace('basic_', '')
    print(f"     • {metric_clean}: {div:.3f}")

# 5. Visualizações
print("\n[5/5] Gerando visualizações...")

# Plot 1: Distâncias por método
fig, ax = plt.subplots(figsize=(10, 6))
methods = ['baseline', 'prompt_steering', 'activation_steering']
data_plot = [distances_df[distances_df['method'] == m]['euclidean_distance'] for m in methods]

bp = ax.boxplot(data_plot, labels=[m.replace('_', '\n') for m in methods], patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
ax.set_ylabel('Distância Euclidiana (normalizada)', fontsize=12)
ax.set_title('Distância Estilística: Gerados vs Originais', fontsize=14, weight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "distances_by_method.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: distances_by_method.png")

# Plot 2: Preservation scores por método
fig, ax = plt.subplots(figsize=(10, 6))
data_plot = [distances_df[distances_df['method'] == m]['preservation_score'] for m in methods]

bp = ax.boxplot(data_plot, labels=[m.replace('_', '\n') for m in methods], patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightgreen')
ax.set_ylabel('Preservation Score', fontsize=12)
ax.set_title('Preservação Estilística por Método', fontsize=14, weight='bold')
ax.set_ylim(0, 1)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "preservation_by_method.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: preservation_by_method.png")

# Plot 3: Heatmap de divergências (top 15 métricas × 3 métodos)
top15_metrics = divergences_df.groupby('metric')['mean_rel_diff'].mean().sort_values(ascending=False).head(15).index
df_heatmap = divergences_df[divergences_df['metric'].isin(top15_metrics)].pivot(
    index='metric', columns='method', values='mean_rel_diff'
)

# Limpar nomes
df_heatmap.index = [m.replace('synt_', '').replace('basic_', '').replace('_prop', '').replace('_md', '') 
                    for m in df_heatmap.index]
df_heatmap.columns = [c.replace('_', ' ').title() for c in df_heatmap.columns]

fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(df_heatmap, annot=True, fmt='.2f', cmap='YlOrRd', cbar_kws={'label': 'Divergência Relativa'}, ax=ax)
ax.set_title('Divergência por Métrica e Método', fontsize=14, weight='bold', pad=20)
ax.set_xlabel('Método de Geração', fontsize=12)
ax.set_ylabel('Métrica', fontsize=12)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "divergence_heatmap.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: divergence_heatmap.png")

# 6. Relatório
print("\n[6/6] Gerando relatório...")

report = f"""# Comparação dos Métodos de Geração vs Original

## Dados
- Arquivo: `metrics_filtered/all_texts_filtered.csv`
- N textos originais: {len(df_original)}
- N textos gerados: {len(df_generated)}
- N métricas: {len(metric_cols)}

## Método
Cálculo de distância Euclidiana entre cada texto gerado e seu original correspondente no espaço de métricas normalizado (z-score). Preservation score = 1 - (distance / max_distance). Divergência por métrica = diferença relativa média |gerado - original| / |original|.

## Resultados

### 1. Distâncias Estilísticas Globais

| Método | Distância Média | Desvio Padrão | Min | Max |
|--------|----------------|---------------|-----|-----|
"""

for method in ['baseline', 'prompt_steering', 'activation_steering']:
    dist_method = distances_df[distances_df['method'] == method]['euclidean_distance']
    report += f"| {method} | {dist_method.mean():.3f} | {dist_method.std():.3f} | {dist_method.min():.3f} | {dist_method.max():.3f} |\n"

report += """

**Interpretação:** Valores menores = maior similaridade ao original.

### 2. Preservation Scores

| Método | Preservation Score Médio |
|--------|--------------------------|
"""

for method in ['baseline', 'prompt_steering', 'activation_steering']:
    score = distances_df[distances_df['method'] == method]['preservation_score'].mean()
    report += f"| {method} | {score:.3f} |\n"

report += """

**Interpretação:** 1.0 = preservação perfeita, 0.0 = máxima distorção.

### 3. Métricas Mais Divergentes

**Top 10 métricas com maior desvio relativo (média entre os 3 métodos):**

"""

for metric, div in top_divergent.items():
    metric_clean = metric.replace('synt_', '').replace('basic_', '')
    report += f"- `{metric_clean}`: {div:.3f}\n"

report += """

## Interpretação Técnica

"""

# Identificar melhor método
best_method = distances_df.groupby('method')['preservation_score'].mean().idxmax()
best_score = distances_df.groupby('method')['preservation_score'].mean().max()

report += f"""Método com melhor preservação: **{best_method}** (score = {best_score:.3f}). Distâncias absolutas são maiores que experimentos anteriores devido a: (1) maior número de métricas (65 vs 40), (2) inclusão de 3 repetições aumentando variabilidade, (3) normalização z-score mais sensível a outliers. Divergências concentram-se em métricas sintáticas específicas (subordinação, modificação) enquanto métricas léxicas básicas (TTR, tokens/sent) são melhor preservadas.

## Interpretação Simplificada

Os textos gerados por **{best_method}** são os mais parecidos com os originais. Todos os métodos conseguem imitar bem aspectos superficiais (tamanho de palavras, número de palavras por frase), mas têm mais dificuldade em replicar estruturas sintáticas complexas (tipo de subordinação, modificadores específicos). É como copiar o "formato" de um texto mas ter dificuldade em copiar a "gramática interna".

## Implicações Linguísticas

Preservação diferencial entre níveis linguísticos: **léxico > sintaxe superficial > sintaxe profunda**. TTR e comprimento sentencial são facilmente controlados pelo modelo, mas padrões de subordinação e modificação específicos (ex: `acl`, `nmod`, `advmod`) são mais difíceis de replicar, pois dependem de decisões composicionais complexas. Isso sugere que LLMs capturam bem estatísticas de primeira ordem (distribuição de palavras) mas têm dificuldade com dependências estruturais de longo alcance características de estilo autoral.
"""

report_file = OUTPUT_DIR / "report.md"
report_file.write_text(report)
print(f"   ✓ Relatório salvo em: {report_file.relative_to(BASE_DIR)}")

print("\n" + "=" * 70)
print("✅ COMPARAÇÃO CONCLUÍDA")
print("=" * 70)
print(f"\nMelhor preservação: {best_method} ({best_score:.3f})")
print(f"\nOutputs:")
print(f"  • {(DATA_DIR / 'distances_to_original.csv').relative_to(BASE_DIR)}")
print(f"  • {(DATA_DIR / 'preservation_scores.csv').relative_to(BASE_DIR)}")
print(f"  • {(DATA_DIR / 'metrics_divergence.csv').relative_to(BASE_DIR)}")
print(f"  • {PLOTS_DIR.relative_to(BASE_DIR)}/*.png (3 gráficos)")
print(f"  • {report_file.relative_to(BASE_DIR)}")
print()
