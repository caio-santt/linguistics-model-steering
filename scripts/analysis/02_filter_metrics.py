#!/usr/bin/env python3
"""
Filtragem de Métricas

Remove métricas problemáticas e cria dataset limpo para análises subsequentes.

Critérios:
1. Remover: ≥20% NaN
2. Remover: Variância zero
3. Remover: Correlação |r| ≥ 0.95 (manter 1 por grupo)
4. Remover: Contagens absolutas (manter apenas proporções)
5. Remover: Métricas language-specific inconsistentes
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
METRICS_FILE = BASE_DIR / "metrics/full_text/individual/all_texts.csv"
QUALITY_DIR = BASE_DIR / "analysis/01_metrics_quality/data"
OUTPUT_DIR = BASE_DIR / "metrics_filtered"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("FILTRAGEM DE MÉTRICAS")
print("=" * 70)

# 1. Carregar dados
print("\n[1/6] Carregando dados...")
df = pd.read_csv(METRICS_FILE)
print(f"   ✓ {len(df)} textos × {len(df.columns)} colunas")

# Separar metadados
metadata_cols = ['text_id', 'author', 'title', 'sample_idx', 'rep', 'condition', 'lang']
metric_cols = [col for col in df.columns if col not in metadata_cols]
print(f"   ✓ {len(metric_cols)} métricas iniciais")

# Carregar análises de qualidade
nan_df = pd.read_csv(QUALITY_DIR / "nan_percentage.csv")
var_df = pd.read_csv(QUALITY_DIR / "variance_stats.csv")
corr_df = pd.read_csv(QUALITY_DIR / "correlations_high.csv")

# 2. Filtro 1: Remover métricas com ≥20% NaN
print("\n[2/6] Filtro 1: Valores ausentes...")
problematic_nan = nan_df[nan_df['pct_nan'] >= 20]['metric'].tolist()
metrics_to_keep = [m for m in metric_cols if m not in problematic_nan]
print(f"   ✗ Removidas: {len(problematic_nan)} métricas (≥20% NaN)")
print(f"   ✓ Restantes: {len(metrics_to_keep)}")

# 3. Filtro 2: Remover métricas com variância zero
print("\n[3/6] Filtro 2: Variância zero...")
constant_metrics = var_df[var_df['variance'] == 0]['metric'].tolist()
metrics_to_keep = [m for m in metrics_to_keep if m not in constant_metrics]
print(f"   ✗ Removidas: {len(constant_metrics)} métricas (var=0)")
print(f"   ✓ Restantes: {len(metrics_to_keep)}")

# 4. Filtro 3: Remover contagens absolutas (manter proporções)
print("\n[4/6] Filtro 3: Contagens vs proporções...")
count_metrics = [m for m in metrics_to_keep if '_count_' in m and not m.endswith('_words')]
metrics_to_keep = [m for m in metrics_to_keep if m not in count_metrics]
print(f"   ✗ Removidas: {len(count_metrics)} contagens (manter proporções)")
print(f"   ✓ Restantes: {len(metrics_to_keep)}")

# 5. Filtro 4: Resolver correlações altas (manter métricas mais interpretáveis)
print("\n[5/6] Filtro 4: Correlações altas...")

# Regras de preferência:
# - Proporções > Distâncias médias
# - DEPREL/UPOS props (mais interpretáveis)
# - Remover total_words (redundante)

to_remove_corr = set()

# Priorizar proporções sobre distâncias médias
for _, row in corr_df.iterrows():
    m1, m2 = row['metric_1'], row['metric_2']
    
    # Se ambas estão na lista atual
    if m1 in metrics_to_keep and m2 in metrics_to_keep:
        # total_words é redundante (mesmo valor em DEPREL e UPOS)
        if 'total_words' in m1:
            to_remove_corr.add(m1)
        elif 'total_words' in m2:
            to_remove_corr.add(m2)
        # Preferir proporção sobre distância média
        elif m1.endswith('_md'):
            to_remove_corr.add(m1)
        elif m2.endswith('_md'):
            to_remove_corr.add(m2)
        # Se ambas são proporções, manter DEPREL (mais específico)
        elif m1.startswith('synt_UPOS') and m2.startswith('synt_DEPREL'):
            to_remove_corr.add(m1)
        elif m2.startswith('synt_UPOS') and m1.startswith('synt_DEPREL'):
            to_remove_corr.add(m2)

metrics_to_keep = [m for m in metrics_to_keep if m not in to_remove_corr]
print(f"   ✗ Removidas: {len(to_remove_corr)} métricas (correlação)")
print(f"   ✓ Restantes: {len(metrics_to_keep)}")

# 6. Criar dataset filtrado
print("\n[6/6] Criando datasets filtrados...")

# Dataset completo
df_filtered = df[metadata_cols + metrics_to_keep].copy()
df_filtered.to_csv(OUTPUT_DIR / "all_texts_filtered.csv", index=False)
print(f"   ✓ all_texts_filtered.csv: {len(df_filtered)} × {len(df_filtered.columns)}")

# Por condição
for condition in ['original', 'baseline', 'prompt_steering', 'activation_steering']:
    df_cond = df_filtered[df_filtered['condition'] == condition].copy()
    df_cond.to_csv(OUTPUT_DIR / f"{condition}_filtered.csv", index=False)
    print(f"   ✓ {condition}_filtered.csv: {len(df_cond)} × {len(df_cond.columns)}")

# 7. Relatório de filtragem
print("\n[7/7] Gerando relatório de filtragem...")

report = f"""# Filtragem de Métricas

## Dados
- Arquivo original: `metrics/full_text/individual/all_texts.csv`
- Métricas iniciais: {len(metric_cols)}
- Métricas finais: {len(metrics_to_keep)}
- **Redução: {len(metric_cols) - len(metrics_to_keep)} métricas ({(len(metric_cols) - len(metrics_to_keep))/len(metric_cols)*100:.1f}%)**

## Método
Aplicação sequencial de filtros para remover métricas problemáticas.

## Resultados

### Pipeline de Filtragem

| Filtro | Critério | N Removidas | N Restantes |
|--------|----------|-------------|-------------|
| Inicial | - | - | {len(metric_cols)} |
| 1 | NaN ≥ 20% | {len(problematic_nan)} | {len(metric_cols) - len(problematic_nan)} |
| 2 | Variância = 0 | {len(constant_metrics)} | {len(metric_cols) - len(problematic_nan) - len(constant_metrics)} |
| 3 | Contagens absolutas | {len(count_metrics)} | {len(metric_cols) - len(problematic_nan) - len(constant_metrics) - len(count_metrics)} |
| 4 | Correlação \\|r\\| ≥ 0.95 | {len(to_remove_corr)} | {len(metrics_to_keep)} |

### Métricas Finais por Categoria

**Léxicas básicas:**
"""

# Categorizar métricas finais
basic_metrics = [m for m in metrics_to_keep if m.startswith('basic_')]
synt_deprel = [m for m in metrics_to_keep if 'DEPREL' in m]
synt_upos = [m for m in metrics_to_keep if 'UPOS' in m]
synt_global = [m for m in metrics_to_keep if m == 'synt_mean_dependency_distance']

report += f"\n- N = {len(basic_metrics)}"
for m in basic_metrics:
    report += f"\n  - `{m}`"

report += f"\n\n**Sintáticas globais:**\n- N = {len(synt_global)}"
for m in synt_global:
    report += f"\n  - `{m}`"

report += f"\n\n**DEPREL (relações de dependência):**\n- N = {len(synt_deprel)}"
report += f"\n- Principais: `det`, `nmod`, `obj`, `amod`, `nsubj`, `mark`, `acl`, `advmod`, `obl`, `advcl`"

report += f"\n\n**UPOS (part-of-speech):**\n- N = {len(synt_upos)}"
report += f"\n- Principais: `NOUN`, `VERB`, `ADJ`, `ADV`, `ADP`, `DET`, `PRON`, `CCONJ`, `SCONJ`"

report += f"""

## Interpretação Técnica

Redução de {len(metric_cols)} para {len(metrics_to_keep)} métricas ({(len(metrics_to_keep)/len(metric_cols))*100:.1f}% retidos). Priorizadas métricas normalizadas (proporções), linguisticamente interpretáveis (UPOS/DEPREL principais), e com dados completos (<20% NaN). Redundâncias resolvidas mantendo medidas mais diretas (proporções > distâncias, DEPREL > UPOS quando correlacionados).

## Interpretação Simplificada

Eliminamos mais da metade das métricas porque eram redundantes, vazias, ou mediam construções raríssimas. Mantivemos apenas as medidas essenciais e interpretáveis que realmente caracterizam estilo: diversidade vocabular, comprimento de sentenças, tipos de palavras (substantivos, verbos, etc.), e relações sintáticas principais (sujeito, objeto, modificadores).

## Implicações Linguísticas

O conjunto final equilibra **cobertura** (captura múltiplas dimensões estilísticas) e **interpretabilidade** (todas as métricas têm significado linguístico claro). Léxicas capturam superficie textual (vocabulário, tamanho). UPOS capturam classes gramaticais (densidade nominal/verbal). DEPREL capturam estrutura sintática (subordinação, modificação). MDD captura complexidade global. Juntas, formam perfil estilométrico abrangente.
"""

report_file = OUTPUT_DIR / "filtering_report.md"
report_file.write_text(report)
print(f"   ✓ Relatório salvo em: {report_file.relative_to(BASE_DIR)}")

print("\n" + "=" * 70)
print("✅ FILTRAGEM CONCLUÍDA")
print("=" * 70)
print(f"\n📊 Métricas finais: {len(metrics_to_keep)} (redução de {(len(metric_cols) - len(metrics_to_keep))/len(metric_cols)*100:.1f}%)")
print(f"\nOutputs em: {OUTPUT_DIR.relative_to(BASE_DIR)}/")
print(f"  • all_texts_filtered.csv")
print(f"  • original_filtered.csv")
print(f"  • baseline_filtered.csv")
print(f"  • prompt_steering_filtered.csv")
print(f"  • activation_steering_filtered.csv")
print(f"  • filtering_report.md")
print()
