#!/usr/bin/env python3
"""
Análise de Decaimento Temporal (TTR Decay)

Investiga evolução de métricas léxicas ao longo do texto.
Testa hipótese de TTR decay: diversidade vocabular diminui com progressão textual.

Analisa:
- TTR decay global
- TTR decay por condição
- TTR decay por autor
- Outras métricas temporais
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
WINDOWED_FILE = BASE_DIR / "metrics/windowed/lexical_windowed.csv"
OUTPUT_DIR = BASE_DIR / "analysis/04_temporal_decay"
DATA_DIR = OUTPUT_DIR / "data"
PLOTS_DIR = OUTPUT_DIR / "plots"

# Criar diretórios
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("ANÁLISE DE DECAIMENTO TEMPORAL")
print("=" * 70)

# 1. Carregar dados
print("\n[1/5] Carregando dados temporais...")
df = pd.read_csv(WINDOWED_FILE)
print(f"   ✓ {len(df)} janelas temporais")
print(f"   ✓ {df['text_id'].nunique()} textos únicos")
print(f"   ✓ {df['window_idx'].nunique()} posições por texto")

# Métricas disponíveis
temporal_metrics = ['ttr', 'tokens_per_sentence_mean', 'chars_per_token_mean',
                   'n_unique_unigrams', 'n_unique_bigrams', 'n_repeated_bigrams',
                   'n_unique_trigrams', 'n_repeated_trigrams']

print(f"   ✓ Métricas temporais: {len(temporal_metrics)}")

# 2. Calcular slopes de decay
print("\n[2/5] Calculando slopes de decay...")

slopes = []
for text_id in df['text_id'].unique():
    df_text = df[df['text_id'] == text_id].sort_values('window_idx')
    
    if len(df_text) >= 3:  # Mínimo 3 pontos para regressão confiável
        text_info = df_text.iloc[0]
        
        # Para cada métrica, calcular slope
        text_slopes = {
            'text_id': text_id,
            'author': text_info['author'],
            'title': text_info['title'],
            'sample_idx': text_info['sample_idx'],
            'rep': text_info['rep'],
            'condition': text_info['condition'],
            'lang': text_info['lang'],
            'n_windows': len(df_text)
        }
        
        for metric in temporal_metrics:
            x = df_text['window_position_numeric'].values
            y = df_text[metric].values
            
            # Remover NaN
            mask = ~np.isnan(y)
            if mask.sum() >= 3:
                x_clean = x[mask]
                y_clean = y[mask]
                
                # Regressão linear
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
                
                text_slopes[f'{metric}_slope'] = slope
                text_slopes[f'{metric}_r2'] = r_value ** 2
                text_slopes[f'{metric}_p_value'] = p_value
                text_slopes[f'{metric}_initial'] = y_clean[0]
                text_slopes[f'{metric}_final'] = y_clean[-1]
            else:
                text_slopes[f'{metric}_slope'] = np.nan
                text_slopes[f'{metric}_r2'] = np.nan
                text_slopes[f'{metric}_p_value'] = np.nan
                text_slopes[f'{metric}_initial'] = np.nan
                text_slopes[f'{metric}_final'] = np.nan
        
        slopes.append(text_slopes)

slopes_df = pd.DataFrame(slopes)
slopes_df.to_csv(DATA_DIR / "temporal_slopes.csv", index=False)
print(f"   ✓ Slopes calculados para {len(slopes_df)} textos")

# 3. Análise de TTR decay
print("\n[3/5] Analisando TTR decay...")

# TTR decay por condição
ttr_stats = []
for condition in df['condition'].unique():
    slopes_cond = slopes_df[slopes_df['condition'] == condition]['ttr_slope'].dropna()
    
    if len(slopes_cond) > 0:
        ttr_stats.append({
            'condition': condition,
            'n_texts': len(slopes_cond),
            'mean_slope': slopes_cond.mean(),
            'std_slope': slopes_cond.std(),
            'median_slope': slopes_cond.median(),
            'pct_negative': (slopes_cond < 0).sum() / len(slopes_cond) * 100,
            'pct_significant': (slopes_df[slopes_df['condition'] == condition]['ttr_p_value'] < 0.05).sum() / len(slopes_cond) * 100
        })
        print(f"   • {condition}:")
        print(f"     - Slope médio: {slopes_cond.mean():.4f}")
        print(f"     - % negativo (decay): {(slopes_cond < 0).sum() / len(slopes_cond) * 100:.1f}%")

ttr_stats_df = pd.DataFrame(ttr_stats)
ttr_stats_df.to_csv(DATA_DIR / "ttr_decay_stats.csv", index=False)

# Teste estatístico: Kruskal-Wallis (slopes entre condições)
conditions = ['original', 'baseline', 'prompt_steering', 'activation_steering']
groups = [slopes_df[slopes_df['condition'] == c]['ttr_slope'].dropna() for c in conditions]
h_stat, p_value = stats.kruskal(*groups)
print(f"\n   ✓ Kruskal-Wallis test: H={h_stat:.3f}, p={p_value:.4f}")

# 4. Visualizações
print("\n[4/5] Gerando visualizações...")

# Plot 1: Evolução do TTR por condição
fig, ax = plt.subplots(figsize=(12, 6))

for condition in conditions:
    df_cond = df[df['condition'] == condition]
    
    # Média por posição
    ttr_by_position = df_cond.groupby('window_position_numeric')['ttr'].agg(['mean', 'std', 'count'])
    
    x = ttr_by_position.index
    y = ttr_by_position['mean']
    err = ttr_by_position['std'] / np.sqrt(ttr_by_position['count'])  # SEM
    
    ax.plot(x, y, marker='o', linewidth=2, label=condition.replace('_', ' ').title())
    ax.fill_between(x, y - err, y + err, alpha=0.2)

ax.set_xlabel('Posição no Texto', fontsize=12)
ax.set_ylabel('TTR (Type-Token Ratio)', fontsize=12)
ax.set_title('Evolução Temporal do TTR', fontsize=14, weight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8])
ax.set_xticklabels(['0%\n(início)', '20%', '40%', '60%', '80%\n(fim)'])
plt.tight_layout()
plt.savefig(PLOTS_DIR / "ttr_evolution_by_condition.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: ttr_evolution_by_condition.png")

# Plot 2: Distribuição dos slopes
fig, ax = plt.subplots(figsize=(10, 6))

data_plot = [slopes_df[slopes_df['condition'] == c]['ttr_slope'].dropna() for c in conditions]
labels = [c.replace('_', '\n') for c in conditions]

bp = ax.boxplot(data_plot, labels=labels, patch_artist=True)
for patch, color in zip(bp['boxes'], ['lightcoral', 'lightblue', 'lightgreen', 'lightyellow']):
    patch.set_facecolor(color)

ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax.set_ylabel('TTR Slope (taxa de decaimento)', fontsize=12)
ax.set_title('Distribuição das Taxas de Decaimento do TTR', fontsize=14, weight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "ttr_slopes_distribution.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: ttr_slopes_distribution.png")

# Plot 3: TTR inicial vs final
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

for idx, condition in enumerate(conditions):
    ax = axes[idx // 2, idx % 2]
    
    df_cond = slopes_df[slopes_df['condition'] == condition]
    
    x = df_cond['ttr_initial'].dropna()
    y = df_cond['ttr_final'].dropna()
    
    # Scatter
    ax.scatter(x, y, alpha=0.6, s=50)
    
    # Linha identidade
    lims = [min(ax.get_xlim()[0], ax.get_ylim()[0]), 
            max(ax.get_xlim()[1], ax.get_ylim()[1])]
    ax.plot(lims, lims, 'r--', alpha=0.5, linewidth=2, label='Sem decay (y=x)')
    
    ax.set_xlabel('TTR Inicial (0%)', fontsize=11)
    ax.set_ylabel('TTR Final (80%)', fontsize=11)
    ax.set_title(condition.replace('_', ' ').title(), fontsize=12, weight='bold')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(PLOTS_DIR / "ttr_initial_vs_final.png", dpi=150, bbox_inches='tight')
plt.close()
print("   ✓ Plot salvo: ttr_initial_vs_final.png")

# 5. Relatório
print("\n[5/5] Gerando relatório...")

report = f"""# Análise de Decaimento Temporal

## Dados
- Arquivo: `metrics/windowed/lexical_windowed.csv`
- N janelas: {len(df)}
- N textos: {df['text_id'].nunique()}
- Posições temporais: 5 (0%, 20%, 40%, 60%, 80%)

## Método
Regressão linear simples para cada texto: TTR ~ posição. Slope negativo = decay (TTR diminui), slope positivo = aumento anômalo. Teste de Kruskal-Wallis para comparar slopes entre condições (H₀: slopes iguais).

## Resultados

### 1. TTR Decay por Condição

| Condição | N Textos | Slope Médio | Desvio Padrão | % Decay | % Sig (p<0.05) |
|----------|----------|-------------|---------------|---------|----------------|
"""

for _, row in ttr_stats_df.iterrows():
    report += f"| {row['condition']} | {row['n_texts']} | {row['mean_slope']:.4f} | {row['std_slope']:.4f} | {row['pct_negative']:.1f}% | {row['pct_significant']:.1f}% |\n"

report += f"""

**Teste de Kruskal-Wallis:** H = {h_stat:.3f}, p = {p_value:.4f}

"""

if p_value < 0.05:
    report += "**Interpretação:** Diferença significativa entre condições (p < 0.05).\n"
else:
    report += "**Interpretação:** Sem diferença significativa entre condições (p ≥ 0.05).\n"

report += """

### 2. Observações Qualitativas

**Padrão de decay esperado (originais):**
"""

orig_slope = slopes_df[slopes_df['condition'] == 'original']['ttr_slope'].mean()
report += f"- Slope médio: {orig_slope:.4f}\n"
report += f"- Este é o **decay natural** em textos humanos\n"

report += """

**Comparação com gerados:**
"""

for condition in ['baseline', 'prompt_steering', 'activation_steering']:
    gen_slope = slopes_df[slopes_df['condition'] == condition]['ttr_slope'].mean()
    diff = gen_slope - orig_slope
    pct_diff = (diff / abs(orig_slope)) * 100 if orig_slope != 0 else 0
    
    if abs(pct_diff) < 10:
        status = "similar"
    elif gen_slope < orig_slope:
        status = "decay mais acentuado"
    else:
        status = "decay menos acentuado"
    
    report += f"- **{condition}**: {gen_slope:.4f} ({status}, {pct_diff:+.1f}%)\n"

report += """

## Interpretação Técnica

TTR decay é fenômeno natural: à medida que texto progride, autor reutiliza vocabulário estabelecido (coerência lexical). Slope negativo indica decay esperado. Comparação entre originais e gerados revela se LLMs replicam esse padrão natural ou apresentam decay artificial (vocabulário esgota prematuramente) ou ausência de decay (geração aleatória sem coerência). Slopes similares sugerem captura do fenômeno linguístico subjacente.

## Interpretação Simplificada

No início de um texto, usamos palavras novas frequentemente. Conforme avançamos, repetimos mais as palavras já usadas (para manter coerência). Isso causa "decay" do TTR. Textos gerados deveriam imitar esse padrão natural. Se o decay for igual ao dos originais, o modelo está gerando texto com coerência lexical natural. Se o decay for mais acentuado, o modelo "esgota vocabulário" cedo demais.

## Implicações Linguísticas

TTR decay reflete **gerenciamento informacional**: introdução de entidades e conceitos (TTR alto) seguida de manutenção referencial (TTR baixo). Textos literários podem ter decay mais suave (maior variação lexical sustentada) vs. textos expositivos (terminologia repetitiva). Gerados que replicam slope original demonstram aprendizado de padrões discursivos além de estatísticas superficiais, sugerindo sensibilidade a estrutura informacional do texto.
"""

report_file = OUTPUT_DIR / "report.md"
report_file.write_text(report)
print(f"   ✓ Relatório salvo em: {report_file.relative_to(BASE_DIR)}")

print("\n" + "=" * 70)
print("✅ ANÁLISE TEMPORAL CONCLUÍDA")
print("=" * 70)
print(f"\nResultado Kruskal-Wallis: H={h_stat:.3f}, p={p_value:.4f}")
print(f"\nOutputs:")
print(f"  • {(DATA_DIR / 'temporal_slopes.csv').relative_to(BASE_DIR)}")
print(f"  • {(DATA_DIR / 'ttr_decay_stats.csv').relative_to(BASE_DIR)}")
print(f"  • {PLOTS_DIR.relative_to(BASE_DIR)}/*.png (3 gráficos)")
print(f"  • {report_file.relative_to(BASE_DIR)}")
print()
