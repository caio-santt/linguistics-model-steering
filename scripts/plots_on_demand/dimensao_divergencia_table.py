#!/usr/bin/env python3
"""
Gera tabela de divergência por dimensão linguística

Agrupa métricas em 3 dimensões:
- Léxicas: básicas (TTR, n-gramas, tamanho)
- Sintáticas básicas: UPOS (classes gramaticais)
- Sintáticas profundas: DEPREL (relações de dependência)

Calcula divergência média de baseline em cada dimensão.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
METRICS_FILE = BASE_DIR / "metrics_filtered/all_texts_filtered.csv"
DIVERGENCE_FILE = BASE_DIR / "analysis/03_method_comparison/data/metrics_divergence.csv"
OUTPUT_FILE = BASE_DIR / "scripts/plots_on_demand/divergence_by_dimension.csv"

print("=" * 70)
print("ANÁLISE DE DIVERGÊNCIA POR DIMENSÃO LINGUÍSTICA")
print("=" * 70)

# Carregar dados
print("\n[1/3] Carregando dados...")
df_metrics = pd.read_csv(METRICS_FILE)
df_divergence = pd.read_csv(DIVERGENCE_FILE)

# Separar métricas por dimensão
metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
all_metrics = [col for col in df_metrics.columns if col not in metadata_cols]

lexical_metrics = [m for m in all_metrics if m.startswith('basic_')]
syntactic_upos = [m for m in all_metrics if 'UPOS_' in m and '_prop' in m]
syntactic_deprel = [m for m in all_metrics if 'DEPREL_' in m and '_prop' in m]
syntactic_other = [m for m in all_metrics if m not in lexical_metrics + syntactic_upos + syntactic_deprel]

print(f"   ✓ {len(lexical_metrics)} métricas léxicas")
print(f"   ✓ {len(syntactic_upos)} métricas sintáticas (UPOS)")
print(f"   ✓ {len(syntactic_deprel)} métricas sintáticas (DEPREL)")
print(f"   ✓ {len(syntactic_other)} outras sintáticas")

# Calcular divergência média por dimensão para cada método
print("\n[2/3] Calculando divergências por dimensão...")

methods = ['baseline', 'prompt_steering', 'activation_steering']
dimensions = {
    'Léxica (básica)': lexical_metrics,
    'Sintática UPOS (classes gram.)': syntactic_upos,
    'Sintática DEPREL (dependências)': syntactic_deprel,
    'Sintática (outras)': syntactic_other
}

results = []

for method in methods:
    df_method = df_divergence[df_divergence['method'] == method]
    
    for dim_name, metrics_list in dimensions.items():
        # Pegar divergência média das métricas dessa dimensão
        available_metrics = [m for m in metrics_list if m in df_method['metric'].values]
        
        if available_metrics:
            divergences = df_method[df_method['metric'].isin(available_metrics)]['mean_rel_diff']
            mean_div = divergences.mean()
            std_div = divergences.std()
            n_metrics = len(available_metrics)
        else:
            mean_div = np.nan
            std_div = np.nan
            n_metrics = 0
        
        results.append({
            'method': method,
            'dimension': dim_name,
            'mean_divergence': mean_div,
            'std_divergence': std_div,
            'n_metrics': n_metrics
        })

results_df = pd.DataFrame(results)

# Adicionar classificação qualitativa (para baseline)
baseline_results = results_df[results_df['method'] == 'baseline'].copy()
baseline_results = baseline_results.sort_values('mean_divergence')

# Definir thresholds (baseado em quantis)
low_threshold = baseline_results['mean_divergence'].quantile(0.33)
high_threshold = baseline_results['mean_divergence'].quantile(0.67)

def classify_divergence(div):
    if pd.isna(div):
        return '?'
    elif div < low_threshold:
        return 'Baixa ✅'
    elif div < high_threshold:
        return 'Média ⚠️'
    else:
        return 'Alta ❌'

results_df['classification'] = results_df['mean_divergence'].apply(classify_divergence)

# Salvar
results_df.to_csv(OUTPUT_FILE, index=False)
print(f"   ✓ Tabela salva em: {OUTPUT_FILE.relative_to(BASE_DIR)}")

# Gerar tabela formatada para apresentação (apenas baseline)
print("\n[3/3] Tabela para slides (BASELINE):")
print("=" * 70)

baseline_table = results_df[results_df['method'] == 'baseline'].copy()
baseline_table = baseline_table.sort_values('mean_divergence')

print(f"\n{'Dimensão':<35} | {'Divergência':<12} | {'Classificação':<15}")
print("-" * 70)
for _, row in baseline_table.iterrows():
    dim = row['dimension']
    div = f"{row['mean_divergence']:.4f}" if not pd.isna(row['mean_divergence']) else "N/A"
    classif = row['classification']
    print(f"{dim:<35} | {div:<12} | {classif:<15}")

print("\n" + "=" * 70)
print("✅ ANÁLISE CONCLUÍDA")
print("=" * 70)
print(f"\nInterpretação:")
print(f"  • Divergência baixa (<{low_threshold:.3f}): Dimensão bem preservada")
print(f"  • Divergência alta (>{high_threshold:.3f}): Dimensão problemática")
print()
