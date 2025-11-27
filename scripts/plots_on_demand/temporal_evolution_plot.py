#!/usr/bin/env python3
"""
Gera gráfico de linha: Evolução temporal de TTR

Mostra evolução de Type-Token Ratio (diversidade lexical) ao longo de 5 janelas temporais.
Compara Original vs Baseline vs Prompt Steering vs Activation Steering.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuração visual
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
WINDOWED_FILE = BASE_DIR / "metrics/windowed/lexical_windowed.csv"
OUTPUT_FILE = BASE_DIR / "scripts/plots_on_demand/temporal_evolution_ttr.png"

print("=" * 70)
print("GRÁFICO: EVOLUÇÃO TEMPORAL DE TTR")
print("=" * 70)

# Carregar dados
print("\n[1/3] Carregando dados windowed...")
df = pd.read_csv(WINDOWED_FILE)

print(f"   ✓ {len(df)} janelas carregadas")
print(f"   ✓ {df['text_id'].nunique()} textos únicos")
print(f"   ✓ Condições: {df['condition'].unique().tolist()}")

# Calcular média de TTR por condição e janela
print("\n[2/3] Calculando médias por janela...")
ttr_by_window = df.groupby(['condition', 'window_idx'])['ttr'].agg(['mean', 'std']).reset_index()

# Configurar cores e estilos
condition_colors = {
    'original': '#2E86AB',      # Azul escuro
    'baseline': '#A23B72',      # Roxo
    'prompt_steering': '#F18F01',  # Laranja
    'activation_steering': '#06A77D'  # Verde
}

condition_labels = {
    'original': 'Original',
    'baseline': 'Baseline',
    'prompt_steering': 'Prompt Steering',
    'activation_steering': 'Activation Steering'
}

# Criar gráfico
print("\n[3/3] Gerando gráfico...")
fig, ax = plt.subplots(figsize=(10, 6))

# Configurar quais condições plotar (modificar conforme necessário)
# Para RQ1 (baseline vs original): ['original', 'baseline']
# Para todas: ttr_by_window['condition'].unique()
conditions_to_plot = ['original', 'baseline']  # ← MODIFICAR AQUI

for condition in conditions_to_plot:
    if condition not in ttr_by_window['condition'].values:
        print(f"   ⚠️ Condição '{condition}' não encontrada, pulando...")
        continue
    df_cond = ttr_by_window[ttr_by_window['condition'] == condition]
    
    if len(df_cond) == 0:
        continue
    
    color = condition_colors.get(condition, 'gray')
    label = condition_labels.get(condition, condition)
    
    # Linha principal
    ax.plot(df_cond['window_idx'], df_cond['mean'], 
            'o-', color=color, linewidth=2.5, markersize=8, 
            label=label, alpha=0.9)
    
    # Área de desvio padrão (sombreada)
    ax.fill_between(df_cond['window_idx'], 
                    df_cond['mean'] - df_cond['std'],
                    df_cond['mean'] + df_cond['std'],
                    color=color, alpha=0.15)

# Configurações do eixo
ax.set_xlabel('Posição Temporal (janela)', fontsize=13, weight='bold')
ax.set_ylabel('Type-Token Ratio (TTR)', fontsize=13, weight='bold')
ax.set_title('Evolução Temporal da Diversidade Lexical', 
             fontsize=15, weight='bold', pad=20)

# Eixo X: 0-4 (5 janelas)
ax.set_xticks(range(5))
ax.set_xticklabels(['Início\n(0-20%)', '1\n(20-40%)', '2\n(40-60%)', 
                    '3\n(60-80%)', 'Fim\n(80-100%)'])

# Grade e legenda
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='best', fontsize=11, framealpha=0.95)

# Anotação com achado principal (se baseline estiver presente)
if 'baseline' in ttr_by_window['condition'].values:
    baseline_data = ttr_by_window[ttr_by_window['condition'] == 'baseline']
    initial_ttr = baseline_data[baseline_data['window_idx'] == 0]['mean'].values[0]
    final_ttr = baseline_data[baseline_data['window_idx'] == 4]['mean'].values[0]
    decay_pct = ((initial_ttr - final_ttr) / initial_ttr) * 100
    
    ax.text(0.98, 0.02, f'Baseline decay: {decay_pct:.1f}%',
            transform=ax.transAxes, fontsize=10,
            ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches='tight')
print(f"   ✓ Gráfico salvo em: {OUTPUT_FILE.relative_to(BASE_DIR)}")

# Estatísticas descritivas
print("\n" + "=" * 70)
print("ESTATÍSTICAS DESCRITIVAS")
print("=" * 70)

for condition in conditions_to_plot:
    if condition in ttr_by_window['condition'].values:
        df_cond = ttr_by_window[ttr_by_window['condition'] == condition]
        initial = df_cond[df_cond['window_idx'] == 0]['mean'].values[0]
        final = df_cond[df_cond['window_idx'] == 4]['mean'].values[0]
        diff = final - initial
        pct_change = (diff / initial) * 100
        
        print(f"\n{condition_labels.get(condition, condition)}:")
        print(f"  • TTR inicial: {initial:.4f}")
        print(f"  • TTR final: {final:.4f}")
        print(f"  • Mudança: {diff:+.4f} ({pct_change:+.2f}%)")
        print(f"  • Tendência: {'Decaimento ↘️' if diff < 0 else 'Estável/Crescimento ↗️'}")

print("\n" + "=" * 70)
print("✅ GRÁFICO GERADO COM SUCESSO")
print("=" * 70)
print()
