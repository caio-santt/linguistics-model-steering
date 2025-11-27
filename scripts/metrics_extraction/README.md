# Sistema de Extração de Métricas Estilométricas

Este diretório contém o sistema completo para extração de métricas léxicas e sintáticas dos textos originais e gerados.

## 📋 Estrutura

```
scripts/metrics_extraction/
├── basic_metrics.py           # Métricas léxicas (TTR, n-gramas, comprimentos)
├── syntactic_metrics.py       # Métricas sintáticas (UDPipe)
├── windowed_analysis.py       # Análise temporal (divisão em janelas)
├── extract_all_metrics.py     # Script principal (orquestra tudo)
└── README.md                  # Esta documentação

metrics/                        # Resultados (criado após execução)
├── full_text/
│   ├── individual/            # Métricas por texto
│   │   ├── all_texts.csv
│   │   ├── original.csv
│   │   ├── baseline.csv
│   │   ├── prompt_steering.csv
│   │   └── activation_steering.csv
│   └── summary/               # Médias agregadas
│       ├── by_author.csv
│       └── by_condition.csv
├── windowed/                  # Análise temporal
│   └── lexical_windowed.csv
└── udpipe_output/             # Arquivos CoNLL-U (intermediários)
```

## 🚀 Uso Rápido

### Instalação de dependências

```bash
# No diretório raiz do projeto
pip install pandas numpy nltk tqdm
```

### Execução completa

```bash
cd scripts/metrics_extraction

# Extração completa (full text + windowed)
python extract_all_metrics.py

# Apenas full text (pular windowed)
python extract_all_metrics.py --skip-windowed

# Customizar threshold de tokens mínimos para windowed
python extract_all_metrics.py --min-tokens 150
```

### Parâmetros

- `--data-dir`: Diretório com pasta `data/` (padrão: diretório atual)
- `--output-dir`: Diretório de saída (padrão: `metrics/`)
- `--skip-windowed`: Pular análise temporal
- `--min-tokens`: Mínimo de tokens para análise windowed (padrão: 100)

## 📊 Métricas Calculadas

### Métricas Léxicas (8 métricas)

**Calculadas por:** `BasicMetrics`

1. **ttr** - Type-Token Ratio (diversidade lexical)
2. **tokens_per_sentence_mean** - Média de tokens por sentença
3. **chars_per_token_mean** - Média de caracteres por token
4. **n_unique_unigrams** - Número de unigramas únicos
5. **n_unique_bigrams** - Número de bigramas únicos
6. **n_repeated_bigrams** - Número de bigramas repetidos
7. **n_unique_trigrams** - Número de trigramas únicos
8. **n_repeated_trigrams** - Número de trigramas repetidos

**Observações:**
- N-gramas calculados após lematização (EN) ou stemming (PT)
- TTR calculado no texto original (sem normalização)
- Usa NLTK para tokenização e processamento

### Métricas Sintáticas (~218 métricas)

**Calculadas por:** `SyntacticMetrics` (via UDPipe API)

1. **mean_dependency_distance** - Distância média de dependência sintática

2. **Relações DEPREL** (para cada relação encontrada):
   - `DEPREL_{relação}_prop` - Proporção da relação
   - `DEPREL_{relação}_md` - Distância média
   - `DEPREL_count_{relação}` - Contagem absoluta
   
   Exemplos: nsubj, obj, advmod, nmod, obl, etc.

3. **Tags UPOS** (para cada tag encontrada):
   - `UPOS_{tag}_prop` - Proporção da tag
   - `UPOS_{tag}_md` - Distância média
   - `UPOS_count_{tag}` - Contagem absoluta
   
   Exemplos: NOUN, VERB, ADJ, ADV, etc.

**Observações:**
- Usa modelos Universal Dependencies v2.12
- PT: `portuguese-petrogold`
- EN: `english-gum`
- Requer conexão com API UDPipe
- Gera arquivos CoNLL-U intermediários

## 🔍 Análise Temporal (Windowed)

### Métricas Léxicas Windowed

**Configuração:**
- Número de janelas: **5** (fixo)
- Divisão: Por tokens simples
- Tamanho: Adaptativo (total_tokens / 5)
- Mínimo de tokens: 100 (configurável)

**Posições das janelas:**
- Janela 0: 0-20% do texto (início)
- Janela 1: 20-40%
- Janela 2: 40-60% (meio)
- Janela 3: 60-80%
- Janela 4: 80-100% (fim)

**Uso:** Detectar decaimento estilístico ao longo da geração.

### Filtragem de Textos Anômalos

**Critério:** Textos com < 100 tokens são excluídos da análise windowed.

**Razão:** Janelas de ~20 tokens são estatisticamente inviáveis (alta variância, contexto insuficiente).

**Impacto esperado:**
- ~2 textos excluídos (0.5% do total)
- Análise full text preserva TODOS os textos
- Documentado em `metrics/windowed/excluded_texts.log` (se houver)

## 🛠️ Arquitetura

### Modularidade

Cada módulo é independente e pode ser usado separadamente:

```python
# Apenas métricas léxicas
from basic_metrics import BasicMetrics

text = "Your text here..."
metrics = BasicMetrics(text, lang='eng')
results = metrics.run()
print(results['ttr'])

# Apenas métricas sintáticas
from syntactic_metrics import SyntacticMetrics

metrics = SyntacticMetrics(text, lang='eng', text_id='example')
results = metrics.run()
print(results['mean_dependency_distance'])

# Análise em janelas
from windowed_analysis import WindowedAnalysis

wa = WindowedAnalysis(text, lang='eng', n_windows=5)
windows = wa.create_windows()

for window in windows:
    print(f"Window {window['idx']}: {window['n_tokens']} tokens")
    # Processar janela...
```

### Robustez

- **Fallbacks:** Se recursos NLTK não disponíveis, usa tokenização simples
- **Tratamento de erros:** Falhas individuais não quebram pipeline completo
- **Validação:** Textos muito curtos são flaggados
- **Progress bars:** Feedback visual via tqdm

## 📈 Outputs Esperados

### Full Text Individual

**Arquivo:** `metrics/full_text/individual/all_texts.csv`

**Linhas:** 600 (60 originais + 540 gerados)

**Colunas:**
- Metadados: text_id, author, title, sample_idx, rep, condition, lang
- Métricas: basic_*, synt_*

### Full Text Summary

**Arquivos:** 
- `by_author.csv` - Médias por autor (4 linhas)
- `by_condition.csv` - Médias por condição (4 linhas: original + 3 geradas)

**Uso:** Comparações rápidas entre autores/condições

### Windowed Lexical

**Arquivo:** `metrics/windowed/lexical_windowed.csv`

**Linhas:** ~2990 (598 textos válidos × 5 janelas)

**Colunas:**
- Metadados: text_id, author, condition, window_idx, window_position, window_n_tokens
- Métricas: ttr, tokens_per_sentence_mean, etc. (8 métricas)

**Uso:** Análise de decaimento temporal

## ⏱️ Tempo de Execução Estimado

- **Full text léxicas:** ~10-15 minutos (600 textos)
- **Full text sintáticas:** ~6-8 horas (600 chamadas API × 30-40s cada)
- **Windowed léxicas:** ~1-2 horas (3000 janelas)

**Total estimado:** 7-11 horas (principalmente devido à API UDPipe)

**Dicas:**
- Executar em horários de menor uso da API
- Considerar cache de resultados intermediários
- Começar com `--skip-windowed` para testar pipeline

## 🐛 Solução de Problemas

### Erro: NLTK resources not found

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('rslp')"
```

### Erro: UDPipe API timeout

- API pode estar sobrecarregada
- Tentar novamente mais tarde
- Considerar instalar UDPipe localmente

### Métricas vazias (NaN)

- Verificar formato do texto de entrada
- Verificar logs de erro no console
- Textos muito curtos podem gerar NaN para algumas métricas

## 📝 Notas de Implementação

### Decisões Metodológicas

1. **Divisão de janelas para sintáticas:** 
   - Deve respeitar limites de sentença (não quebrar árvore de dependência)
   - Implementado em `windowed_analysis.py` com `respect_sentences=True`
   - Por enquanto, apenas léxicas implementadas no pipeline principal

2. **Threshold de 100 tokens:**
   - Baseado em análise empírica do dataset
   - Exclui apenas 2 textos anômalos (~0.5%)
   - Documentação completa em `ANALISE_METRICAS_ORIGINAIS.md`

3. **Lematização vs Stemming:**
   - PT: RSLPStemmer (stemming)
   - EN: WordNetLemmatizer (lematização)
   - Aplicado antes de calcular n-gramas

## 🔮 Próximos Passos

1. ✅ Implementar extração full text
2. ✅ Implementar windowed léxicas
3. ⏳ Implementar windowed sintáticas (opcional)
4. ⏳ Adicionar análise estatística (variância, consistência)
5. ⏳ Gerar visualizações
6. ⏳ Análise de RQ1 e RQ2

## 📚 Referências

- **UDPipe:** http://ufal.mff.cuni.cz/udpipe
- **Universal Dependencies:** https://universaldependencies.org/
- **NLTK:** https://www.nltk.org/
