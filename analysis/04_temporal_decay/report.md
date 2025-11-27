# Análise de Decaimento Temporal

## Dados
- Arquivo: `metrics/windowed/lexical_windowed.csv`
- N janelas: 2990
- N textos: 240
- Posições temporais: 5 (0%, 20%, 40%, 60%, 80%)

## Método
Regressão linear simples para cada texto: TTR ~ posição. Slope negativo = decay (TTR diminui), slope positivo = aumento anômalo. Teste de Kruskal-Wallis para comparar slopes entre condições (H₀: slopes iguais).

## Resultados

### 1. TTR Decay por Condição

| Condição | N Textos | Slope Médio | Desvio Padrão | % Decay | % Sig (p<0.05) |
|----------|----------|-------------|---------------|---------|----------------|
| original | 60 | 0.0057 | 0.0828 | 41.7% | 1.7% |
| baseline | 180 | -0.0934 | 0.0743 | 90.6% | 6.7% |


**Teste de Kruskal-Wallis:** H = nan, p = nan

**Interpretação:** Sem diferença significativa entre condições (p ≥ 0.05).


### 2. Observações Qualitativas

**Padrão de decay esperado (originais):**
- Slope médio: 0.0057
- Este é o **decay natural** em textos humanos


**Comparação com gerados:**
- **baseline**: -0.0934 (decay mais acentuado, -1732.2%)
- **prompt_steering**: nan (decay menos acentuado, +nan%)
- **activation_steering**: nan (decay menos acentuado, +nan%)


## Interpretação Técnica

TTR decay é fenômeno natural: à medida que texto progride, autor reutiliza vocabulário estabelecido (coerência lexical). Slope negativo indica decay esperado. Comparação entre originais e gerados revela se LLMs replicam esse padrão natural ou apresentam decay artificial (vocabulário esgota prematuramente) ou ausência de decay (geração aleatória sem coerência). Slopes similares sugerem captura do fenômeno linguístico subjacente.

## Interpretação Simplificada

No início de um texto, usamos palavras novas frequentemente. Conforme avançamos, repetimos mais as palavras já usadas (para manter coerência). Isso causa "decay" do TTR. Textos gerados deveriam imitar esse padrão natural. Se o decay for igual ao dos originais, o modelo está gerando texto com coerência lexical natural. Se o decay for mais acentuado, o modelo "esgota vocabulário" cedo demais.

## Implicações Linguísticas

TTR decay reflete **gerenciamento informacional**: introdução de entidades e conceitos (TTR alto) seguida de manutenção referencial (TTR baixo). Textos literários podem ter decay mais suave (maior variação lexical sustentada) vs. textos expositivos (terminologia repetitiva). Gerados que replicam slope original demonstram aprendizado de padrões discursivos além de estatísticas superficiais, sugerindo sensibilidade a estrutura informacional do texto.
