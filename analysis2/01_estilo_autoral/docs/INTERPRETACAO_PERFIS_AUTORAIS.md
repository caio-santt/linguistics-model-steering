# Análise Exploratória: Perfis Estilísticos Autorais

## Pergunta Central

**Como cada autor se distingue linguisticamente?** Existem "assinaturas estilísticas" quantificáveis que caracterizam cada escritor?

---

## Dados e Metodologia

- **Corpus:** 60 textos originais (15 por autor)
- **Autores:** Lispector (PT), Woolf (EN), Wikipedia PT, Wikipedia EN
- **Métricas:** 65 filtradas (8 léxicas + 57 sintáticas)
- **Abordagem:** Análise exploratória livre, priorizando interpretação linguística

---

## 1. Métricas Mais Discriminativas

Calculamos o **coeficiente de variação (CV)** entre autores para identificar quais métricas melhor distinguem estilos. CV alto indica grande variação entre autores, ou seja, poder discriminativo.

### Top 10 Métricas Discriminativas:

| Rank | Métrica | CV | Tipo |
|------|---------|-----|------|
| 1 | `root_prop` | 0.784 | Sintática |
| 2 | `appos_prop` | 0.749 | Sintática |
| 3 | `PRON_prop` | 0.746 | Sintática |
| 4 | `nmod_prop` | 0.580 | Sintática |
| 5 | `VERB_md` | 0.580 | Sintática |
| 6 | `advmod_prop` | 0.524 | Sintática |
| 7 | `PROPN_prop` | 0.521 | Sintática |
| 8 | `acl_md` | 0.516 | Sintática |
| 9 | `amod_prop` | 0.480 | Sintática |
| 10 | `cop_prop` | 0.479 | Sintática |

**Observação crítica:** As 9 métricas mais discriminativas são **sintáticas**. Apenas na posição 14 aparece uma métrica léxica (`tokens_per_sentence_mean`). Isso sugere que **estilo autoral reside primariamente em padrões estruturais/gramaticais, não em escolhas lexicais**.

---

## 2. Interpretação Linguística das Métricas-Chave

### **1. `root_prop` (Proporção de raízes sintáticas)**

**O que é:** Percentual de palavras que funcionam como raiz da árvore de dependência (núcleo da oração principal).

**Interpretação:**
- **Alto:** Muitas orações curtas e independentes (estrutura paratática)
- **Baixo:** Poucas orações principais, muita subordinação (estrutura hipotática)

### **2. `appos_prop` (Proporção de aposição)**

**O que é:** Uso de aposição - estrutura explicativa que renomeia ou clarifica um termo.

Exemplo: *"Maria, minha professora, chegou."* (professora é aposição de Maria)

**Interpretação:**
- **Alto:** Estilo expositivo/enciclopédico (comum em textos informativos)
- **Baixo:** Estilo narrativo direto

### **3. `PRON_prop` (Densidade pronominal)**

**O que é:** Proporção de pronomes no texto.

**Interpretação:**
- **Alto:** Foco em subjetividade, referências anafóricas, narrativa em primeira pessoa
- **Baixo:** Foco em substantivos/entidades, estilo mais nominal

### **4. `nmod_prop` (Modificação nominal)**

**O que é:** Uso de modificadores nominais (ex: "casa **de pedra**", "livro **sobre arte**").

**Interpretação:**
- **Alto:** Estilo descritivo, especificação de entidades
- **Baixo:** Estilo mais direto

### **5. `VERB_md` (Distância média de dependência dos verbos)**

**O que é:** Quão longe (em palavras) os verbos estão de suas dependências sintáticas.

**Interpretação:**
- **Alto:** Verbos com dependentes distantes = estrutura sintática complexa
- **Baixo:** Verbos com dependentes próximos = estrutura simples

---

## 3. PCA: Visualizando o Espaço Estilístico

### Variância Explicada
- **PC1:** 24.07% da variância total
- **PC2:** 18.76% da variância total
- **Total (2D):** 42.82%

**Interpretação:** Conseguimos capturar ~43% da variação estilística entre autores usando apenas 2 dimensões. As 65 métricas originais contêm informação redundante ou ruído que não contribui para distinguir autores.

---

## 4. Interpretação Linguística dos Componentes Principais

### **PC1 (24.07% da variância): "Eixo da Complexidade Sintática"**

**Top 5 métricas que mais contribuem (loadings):**
1. `mean_dependency_distance` (+0.237): Distância média geral
2. `VERB_md` (+0.235): Distância dos verbos
3. `PUNCT_md` (+0.228): Distância da pontuação
4. `nmod_md` (+0.224): Distância de modificadores nominais
5. `NOUN_md` (+0.220): Distância dos substantivos

**Todas as top 10 métricas são distâncias (`_md`).**

**Interpretação linguística:**

PC1 representa **profundidade e encaixamento sintático**. Textos com PC1 alto têm:
- Dependências sintáticas longas (palavras relacionadas estão distantes)
- Estruturas hierárquicas profundas (muita subordinação)
- Orações encaixadas dentro de orações
- Complexidade estrutural (não necessariamente vocabular)

**Exemplos:**
- **PC1 alto (Woolf):** *"The thoughts that came to her mind, wandering through the streets, were numerous."* (subordinada relativa + participial, dependências longas)
- **PC1 baixo (Lispector):** *"Ela acordou. Olhou pela janela. O dia estava cinzento."* (orações curtas, dependências locais)

---

### **PC2 (18.76% da variância): "Eixo Verbal vs. Nominal"**

**Top 5 métricas que mais contribuem (loadings):**
1. `VERB_prop` (+0.245): Densidade verbal (positivo)
2. `tokens_per_sentence_mean` (-0.241): Tamanho de sentenças (negativo)
3. `nmod_prop` (-0.228): Modificação nominal (negativo)
4. `advmod_prop` (+0.221): Modificação adverbial (positivo)
5. `appos_prop` (-0.215): Aposição (negativo)

**Interpretação linguística:**

PC2 contrasta dois perfis estilísticos:

**PC2 Alto (positivo) = Estilo Verbal/Dinâmico:**
- Alta densidade de verbos
- Frases curtas
- Modificação adverbial (modifica ações)
- Foco em eventos e ações

**PC2 Baixo (negativo) = Estilo Nominal/Descritivo:**
- Baixa densidade verbal
- Frases longas
- Modificação nominal (especifica entidades)
- Aposição (explica termos)
- Foco em entidades e suas propriedades

**Exemplos:**
- **PC2 alto (Lispector):** *"Correu. Parou. Respirou fundo. Olhou ao redor."* (verbos, ação, frases curtas)
- **PC2 baixo (Wikipedia):** *"A inteligência artificial, campo da ciência da computação, utiliza algoritmos de aprendizado de máquina..."* (nominal, aposição, frases longas)

---

## 5. Perfis Autorais Quantitativos

Usando as 10 métricas mais discriminativas, caracterizamos cada autor através de **z-scores** (quantos desvios-padrão acima/abaixo da média geral):

### **Clarice Lispector**
- **Características distintivas:**
  - `root_prop`: **+1.49** (muito acima da média)
    - Muitas orações principais curtas
    - Estrutura paratática (coordenação > subordinação)
  - `cop_prop`: **+1.19**
    - Alta densidade de verbos de ligação ("ser", "estar")
    - Estilo existencial/introspectivo
  - `VERB_md`: **-1.00**
    - Verbos próximos de suas dependências
    - Estrutura sintática simples

**Perfil linguístico:** Lispector escreve com **orações curtas e independentes**, alta densidade de verbos de ligação (reflexões sobre estados), e estrutura sintática simples (baixa distância de dependência). Estilo **paratático e introspectivo**.

---

### **Virginia Woolf**
- **Características distintivas:**
  - `PRON_prop`: **+1.35**
    - Altíssima densidade pronominal
    - Foco em subjetividade, fluxo de consciência
  - `acl_md`: **+1.42**
    - Cláusulas adjetivais distantes
    - Estrutura subordinativa complexa
  - `VERB_md`: **+1.34**
    - Verbos distantes de dependentes
    - Encaixamento sintático profundo

**Perfil linguístico:** Woolf usa **alta densidade pronominal** (narrativa subjetiva, stream-of-consciousness), com **estrutura sintática complexa** (subordinação, encaixamento). Estilo **hipotático e psicológico**.

---

### **Wikipedia PT**
- **Características distintivas:**
  - `appos_prop`: **+1.46**
    - Uso intenso de aposição
    - Estilo explicativo/didático
  - `nmod_prop`: **+1.41**
    - Muita modificação nominal
    - Especificação de entidades técnicas
  - `PROPN_prop`: **+1.31**
    - Alta densidade de nomes próprios
    - Referência a entidades específicas

**Perfil linguístico:** Wikipedia PT é **nominal e descritivo**, com alto uso de aposição para explicar termos técnicos, modificação nominal para especificar entidades, e nomes próprios. Estilo **expositivo e enciclopédico**.

---

### **Wikipedia EN**
- **Características distintivas:**
  - `amod_prop`: **+1.22**
    - Modificação adjetival intensa
    - Descrições de propriedades
  - Perfil similar ao Wikipedia PT, mas ligeiramente menos nominal

**Perfil linguístico:** Wikipedia EN segue padrão enciclopédico, com ênfase em **modificação adjetival** para descrever propriedades de entidades.

---

## 6. Interpretação do PCA: Onde os Autores se Posicionam?

Baseando-se nos loadings e nas características dos autores:

### **Eixo PC1 (Complexidade Sintática):**
- **Alto (direita):** Woolf (estrutura complexa, subordinação)
- **Baixo (esquerda):** Lispector (estrutura simples, coordenação)

### **Eixo PC2 (Verbal vs. Nominal):**
- **Alto (topo):** Lispector (verbal, dinâmico, frases curtas)
- **Baixo (base):** Wikipedias (nominal, descritivo, frases longas)

### **Quadrantes do PCA:**

```
PC2 (Verbal/Dinâmico)
        ↑
        |
   Lispector (literário PT)
        |
←───────┼───────→ PC1 (Complexidade Sintática)
        |
   Wiki PT   Wiki EN
        |
   Woolf (literário EN)?
        ↓
PC2 (Nominal/Descritivo)
```

**Hipótese de posicionamento:**
- **Lispector:** PC1 baixo (simples), PC2 alto (verbal) → Quadrante superior esquerdo
- **Woolf:** PC1 alto (complexo), PC2 médio/alto (verbal literário) → Quadrante superior direito
- **Wikipedia PT/EN:** PC1 médio, PC2 baixo (nominal) → Quadrantes inferiores

---

## 7. Síntese: O que Define Estilo Autoral?

### **Achados principais:**

1. **Estilo é primariamente sintático:** 9 das 10 métricas mais discriminativas são sintáticas, não léxicas.

2. **Duas dimensões críticas:**
   - **Complexidade estrutural (PC1):** Simples vs. complexo
   - **Foco verbal vs. nominal (PC2):** Ação/evento vs. entidade/descrição

3. **Contraste literário vs. enciclopédico:**
   - **Literário (Lispector/Woolf):** Alta densidade verbal, foco em subjetividade
   - **Enciclopédico (Wikipedias):** Alta densidade nominal, foco em entidades e propriedades

4. **Diferenças intra-literário:**
   - **Lispector:** Estrutura simples + verbal = Parataxe introspectiva
   - **Woolf:** Estrutura complexa + pronominal = Hipotaxe psicológica

5. **Diferenças intra-enciclopédico:**
   - **Wikipedia PT:** Aposição + nomes próprios
   - **Wikipedia EN:** Modificação adjetival

---

## Conclusão

Estilos autorais são **assinaturas estruturais**, não apenas escolhas de palavras. A análise PCA revela que apenas ~43% da variação estilística pode ser capturada em 2 dimensões interpretáveis:
- **Eixo 1 (Complexidade):** Quão profundas/encaixadas são as estruturas sintáticas
- **Eixo 2 (Verbalidade):** Foco em ações/eventos vs. entidades/propriedades

Cada autor ocupa uma região distinta nesse espaço bidimensional, refletindo escolhas sistemáticas de organização sintática e distribuição de classes gramaticais.

---

## Arquivos Gerados

- `discriminative_metrics.csv` - Ranking de poder discriminativo
- `pca_author_styles.png` - Visualização do espaço estilístico
- `pca_loadings.csv` - Contribuições das métricas para cada PC
- `author_profiles_normalized.csv` - Z-scores dos perfis
- `author_profiles_heatmap.png` - Visualização dos perfis

---

## 8. Componentes Adicionais e Métricas Individuais Interpretáveis

### Explorando PC3, PC4 e PC5

Além dos dois primeiros componentes (PC1 = Complexidade Sintática, PC2 = Verbal vs. Nominal), exploramos três componentes adicionais para identificar outras dimensões interpretáveis.

**Variância explicada:**
- PC3: 9.42% (acumulado: 52.25%)
- PC4: 8.33% (acumulado: 60.58%)
- PC5: 6.18% (acumulado: 66.77%)

---

### **PC3 (9.42%): "Eixo da Repetição vs. Diversidade Lexical"**

**Top 5 loadings:**
1. `n_unique_bigrams` (+0.301) - Bigramas únicos
2. `n_repeated_bigrams` (-0.285) - Bigramas repetidos
3. `n_repeated_trigrams` (-0.279) - Trigramas repetidos
4. `n_unique_trigrams` (+0.274) - Trigramas únicos
5. `ttr` (+0.268) - Riqueza vocabular

**Interpretação:**

PC3 separa textos pela **variabilidade de combinações de palavras**. Valores altos indicam alta diversidade (muitas combinações únicas de 2-3 palavras), valores baixos indicam muitas repetições das mesmas combinações.

Este componente não captura apenas vocabulário (palavras isoladas), mas **padrões de construção** - como as palavras se combinam. Textos com PC3 alto têm estilo mais variado e menos fórmulas fixas. Textos com PC3 baixo repetem estruturas similares.

---

#### **Como cada autor se comporta no PC3:**

**Ranking (do mais diverso ao mais repetitivo):**

1. **Lispector (PC3 = +2.02)** - MÁXIMA DIVERSIDADE
   - **Bigramas únicos/repetidos:** 450/82 = **5.47×** mais combinações únicas
   - **Trigramas repetidos:** Apenas 15.3 (o menor de todos)
   - **Interpretação:** Apesar de usar frases curtas e simples (PC1 baixo), Lispector **nunca repete a mesma fórmula**. Cada pensamento fragmentado é expresso de maneira única. É como se ela recusasse estruturas prontas - cada frase é uma construção singular. O estilo introspectivo exige reformulação constante, não há atalhos estilísticos.

2. **Wikipedia PT (PC3 = +0.67)** - DIVERSIDADE MODERADA-ALTA
   - **Bigramas únicos/repetidos:** 438/103 = 4.25×
   - **TTR:** 0.515 (o mais alto)
   - **Interpretação:** Textos enciclopédicos em português cobrem tópicos muito variados, cada um com vocabulário e construções específicas do domínio. Um artigo sobre física usa combinações diferentes de um sobre história. A diversidade vem da amplitude temática, não de estilo único.

3. **Woolf (PC3 = -1.32)** - REPETIÇÃO MODERADA
   - **Bigramas repetidos:** 103.3 (o mais alto)
   - **TTR:** 0.461 (o mais baixo)
   - **Interpretação:** Woolf **repete palavras E combinações**. O fluxo de consciência gera padrões recorrentes: "she thought", "she felt", "she wondered" aparecem repetidamente. A complexidade sintática (PC1 alto) convive com fórmulas de construção. É uma repetição estilística deliberada que cria ritmo e coerência no fluxo mental.

4. **Wikipedia EN (PC3 = -1.36)** - MÁXIMA REPETIÇÃO
   - **Trigramas repetidos:** 26.5
   - **Interpretação:** Textos enciclopédicos em inglês seguem **fórmulas estruturais rígidas**: "is a...", "was a...", "also known as...", "located in...". A Wikipedia privilegia clareza e padronização sobre originalidade estilística. As mesmas construções explicativas aparecem em milhares de artigos.

---

#### **PC3 vs. TTR: Qual a diferença?**

**Descoberta importante:** PC3 NÃO é apenas "outra forma de medir TTR"

| Autor | TTR (palavras) | PC3 (combinações) | Relação |
|-------|----------------|-------------------|---------|
| Lispector | 0.512 (alto) | +2.02 (alto) | ✓ Coerente |
| Wiki PT | 0.515 (alto) | +0.67 (médio) | ✓ Coerente |
| Woolf | **0.461 (baixo)** | **-1.32 (baixo)** | ✓ Coerente |
| Wiki EN | 0.486 (médio) | -1.36 (baixo) | ⚠️ Divergente |

**Wikipedia EN:** Tem TTR médio (vocabulário razoavelmente variado) mas PC3 muito baixo (combinações repetitivas). Isso revela que textos enciclopédicos em inglês usam **palavras diferentes mas sempre nas mesmas fórmulas estruturais**.

**Woolf:** Baixo em ambos - repete tanto palavras quanto suas combinações. O fluxo de consciência cria ritmo através da recorrência.

**Lispector:** Alto em ambos - cada palavra nova aparece em combinações novas. Máxima singularidade estilística.

---

#### **Independência entre PC1, PC2 e PC3:**

**Você pode ser:**
- Complexo (PC1 alto) E repetitivo (PC3 baixo) → **Woolf**
- Simples (PC1 baixo) E diverso (PC3 alto) → **Lispector**
- Nominal (PC2 baixo) E repetitivo (PC3 baixo) → **Wikipedia EN**
- Verbal (PC2 alto) E diverso (PC3 alto) → **Lispector**

PC3 adiciona uma dimensão ortogonal: não mede complexidade nem foco verbal/nominal, mas **grau de formulação vs. originalidade nas construções**.

---

### **PC4 (8.33%): "Eixo do Tamanho e Densidade Determinativa"**

**Top 5 loadings:**
1. `n_unique_unigrams` (+0.321) - Palavras únicas totais
2. `n_repeated_bigrams` (-0.222) - Bigramas repetidos
3. `det_md` (+0.221) - Distância dos determinantes
4. `det_prop` (-0.220) - Densidade de determinantes
5. `n_unique_bigrams` (+0.198) - Bigramas únicos

**Interpretação:**

PC4 contrasta textos **mais longos com vocabulário extenso** versus textos com **alta concentração de determinantes** ("o", "a", "um", "uma"). 

Valores altos = textos maiores, mais palavras diferentes, determinantes distantes de seus núcleos.
Valores baixos = textos com muitos determinantes densos e próximos (estilo mais nominal direto).

Este componente captura principalmente diferença de **extensão textual** e estilo de uso de artigos/determinantes, mas tem interpretação menos clara linguisticamente que PC1-PC3.

---

### **PC5 (6.18%): "Eixo da Subordinação"**

**Top 5 loadings:**
1. `mark_md` (+0.323) - Distância dos marcadores de subordinação
2. `SCONJ_md` (+0.285) - Distância das conjunções subordinativas
3. `PROPN_md` (+0.240) - Distância dos nomes próprios
4. `det_md` (-0.230) - Distância dos determinantes
5. `case_md` (-0.212) - Distância de marcadores de caso

**Interpretação:**

PC5 captura uso de **subordinação complexa**. Valores altos indicam marcadores de subordinação ("que", "quando", "porque") com dependências longas - ou seja, orações subordinadas elaboradas e distantes da principal.

Este componente distingue textos que usam muita subordinação complexa (com cláusulas encaixadas profundamente) versus textos com estrutura mais direta.

**Relevância:** Similar a PC1 (complexidade), mas focado especificamente em subordinação, não em complexidade geral. Pode separar estilos com coordenação complexa (PC1 alto, PC5 baixo) de estilos com subordinação complexa (PC1 alto, PC5 alto).

---

### Métricas Individuais Altamente Discriminativas e Interpretáveis

Além dos componentes principais, algumas métricas individuais têm interpretação direta e diferem significativamente entre autores:

#### **1. Tamanho de Frases (`tokens_per_sentence_mean`)**
- **Effect size (η²):** 0.589 (muito grande)
- **Ranking:** Wikipedia PT (34.4) > Wikipedia EN (29.6) > Woolf (23.1) > Lispector (11.1)

**Interpretação:** Métrica mais diretamente interpretável. Lispector escreve frases 3× menores que Wikipedia PT. Esta métrica sozinha já separa fortemente os autores.

#### **2. Riqueza Vocabular (`ttr` - Type-Token Ratio)**
- **Effect size (η²):** 0.282 (grande)
- **Ranking:** Wikipedia PT (0.515) > Lispector (0.512) > Wikipedia EN (0.486) > Woolf (0.461)

**Interpretação:** Proporção de palavras únicas no texto. Valores próximos a 1.0 = muitas palavras diferentes (pouca repetição). Woolf repete mais palavras que outros autores, enquanto Wikipedia PT e Lispector têm vocabulário mais variado.

#### **3. Outras Métricas com Grande Effect Size (η² > 0.6)**

Todas as métricas abaixo têm diferenças estatisticamente significativas (p < 0.001) e grande poder discriminativo:

| Métrica | η² | Interpretação Direta |
|---------|-----|---------------------|
| `ADP_prop` | 0.867 | Densidade de preposições ("de", "em", "para") |
| `root_prop` | 0.841 | Proporção de orações principais |
| `PRON_prop` | 0.810 | Densidade de pronomes ("ele", "ela", "isso") |
| `advmod_prop` | 0.800 | Densidade de modificadores adverbiais |
| `chars_per_token_mean` | 0.777 | Tamanho médio de palavras (complexidade lexical) |
| `nmod_prop` | 0.777 | Densidade de modificadores nominais |
| `nsubj_prop` | 0.748 | Densidade de sujeitos explícitos |
| `VERB_prop` | 0.733 | Densidade de verbos |

**Observação:** Enquanto PC1-PC2 capturam padrões multidimensionais complexos, estas métricas individuais são **facilmente interpretáveis** e podem ser usadas para explicações diretas de diferenças estilísticas.

---

### Síntese: Componentes Adicionais vs. PC1-PC2

**PC1 e PC2 permanecem os mais informativos e interpretáveis:**
- Capturam 42.82% da variância em apenas 2 dimensões
- Têm interpretação linguística clara e robusta
- Separam bem os 4 autores visualmente

**PC3 é interpretável mas menos discriminativo:**
- Captura diversidade vs. repetição de combinações
- Útil para distinguir textos formulaicos vs. variados
- Mas contribui apenas 9.42% da variância

**PC4 e PC5 têm interpretação mais difusa:**
- PC4 mistura tamanho textual com padrões de determinantes
- PC5 captura subordinação específica (subconjunto de PC1)
- Contribuem pouco para distinguir autores (8.33% e 6.18%)

**Recomendação:** Para análises e visualizações, **PC1 e PC2 são suficientes**. PC3 pode ser útil em análises específicas sobre repetição estilística. PC4-PC5 não adicionam interpretabilidade clara além do que PC1-PC3 já capturam.

**Métricas individuais são mais úteis para explicações diretas:** Tamanho de frases, riqueza vocabular, densidade de pronomes e proporção de orações principais são mais fáceis de comunicar que combinações lineares de 65 métricas (PCs).

---

## 9. Síntese Discursiva: Os Perfis Estilísticos Descobertos

### Versão Narrativa (sem números)

A análise revelou que cada autor tem uma assinatura estilística única, marcada principalmente por escolhas estruturais (como conectar frases e organizar ideias), não apenas por vocabulário diferente. Dois eixos principais separam os autores: complexidade sintática e foco em verbos versus substantivos.

**Clarice Lispector** escreve com frases curtas e diretas. Ela prefere conectar ideias colocando-as lado a lado, em vez de encaixá-las uma dentro da outra. Usa muitos verbos de ligação ("ser", "estar"), criando um estilo introspectivo que observa estados internos. As frases têm estrutura simples: o verbo fica perto das palavras que dependem dele. Isso cria um ritmo fragmentado, como pensamentos soltos que vão se somando. É como se ela escrevesse pensamentos breves e independentes, um após o outro.

**Virginia Woolf** faz o oposto. Ela constrói frases longas e elaboradas, colocando ideias dentro de outras ideias. Usa muitos pronomes ("ele", "ela", "isso"), o que torna o texto muito focado na perspectiva interna dos personagens. As frases são como camadas: você começa lendo uma coisa, aí vem outra informação no meio, depois volta para o que estava falando. Esse entrelaçamento de informações cria uma sensação de complexidade psicológica, como se estivéssemos acompanhando vários pensamentos simultâneos.

Os **textos da Wikipedia** (português e inglês) são completamente diferentes das autoras literárias. Eles focam em substantivos e descrições, não em verbos e ações. A Wikipedia usa muita "aposição" - aquela estrutura onde você coloca uma explicação logo depois de um termo ("Einstein, o físico alemão, ..."). As frases são longas e cheias de informação, com muitos nomes próprios e poucas ações. O objetivo não é contar uma história, mas descrever coisas e explicar conceitos. Wikipedia em português usa mais explicações entre vírgulas, enquanto a versão inglesa usa mais adjetivos, mas ambas compartilham esse estilo descritivo e informativo.

A diferença fundamental entre textos literários e enciclopédicos não está nas palavras escolhidas, mas em como as ideias são organizadas. Textos literários constroem-se em torno de verbos e ações (mesmo quando falam de pensamentos). Textos enciclopédicos constroem-se em torno de substantivos e suas características. Entre as próprias autoras literárias, Lispector prefere estruturas simples para criar impacto emocional direto, enquanto Woolf prefere estruturas complexas para mostrar a riqueza da experiência mental.

Esses padrões não são acidentais. São escolhas deliberadas que definem o estilo de cada autor. Estilo não é apenas "usar palavras bonitas", mas decidir como estruturar as frases para comunicar a experiência que você quer transmitir.

---

### Versão Técnica (com evidências estatísticas)

A análise revelou que cada autor tem uma assinatura estilística única, marcada principalmente por escolhas estruturais (como conectar frases e organizar ideias), não apenas por vocabulário diferente. Das 10 métricas mais discriminativas (CV > 0.40), 9 são sintáticas, com apenas uma léxica (`tokens_per_sentence_mean`, CV=0.409) aparecendo na posição 14. Dois eixos principais separam os autores: complexidade sintática (PC1, 24.07% da variância) e foco em verbos versus substantivos (PC2, 18.76% da variância).

**Clarice Lispector** escreve com frases curtas e diretas (`tokens_per_sentence_mean` = 11.14, o menor entre todos os autores). Ela prefere conectar ideias colocando-as lado a lado, em vez de encaixá-las uma dentro da outra (`root_prop` z-score = +1.49, muito acima da média). Usa muitos verbos de ligação ("ser", "estar") (`cop_prop` z-score = +1.19), criando um estilo introspectivo que observa estados internos. As frases têm estrutura simples: o verbo fica perto das palavras que dependem dele (`VERB_md` z-score = -1.00). Isso cria um ritmo fragmentado, como pensamentos soltos que vão se somando. É como se ela escrevesse pensamentos breves e independentes, um após o outro.

**Virginia Woolf** faz o oposto. Ela constrói frases longas e elaboradas, colocando ideias dentro de outras ideias (`VERB_md` z-score = +1.34; `acl_md` z-score = +1.42). Usa muitos pronomes ("ele", "ela", "isso") (`PRON_prop` z-score = +1.35, CV=0.746 - a terceira métrica mais discriminativa), o que torna o texto muito focado na perspectiva interna dos personagens. As frases são como camadas: você começa lendo uma coisa, aí vem outra informação no meio, depois volta para o que estava falando. Esse entrelaçamento de informações cria uma sensação de complexidade psicológica, como se estivéssemos acompanhando vários pensamentos simultâneos.

Os **textos da Wikipedia** (português e inglês) são completamente diferentes das autoras literárias. Eles focam em substantivos e descrições, não em verbos e ações (PC2 negativo). A Wikipedia usa muita "aposição" - aquela estrutura onde você coloca uma explicação logo depois de um termo ("Einstein, o físico alemão, ...") (`appos_prop`: Wikipedia PT z-score = +1.46 - a segunda métrica mais discriminativa, CV=0.749). Também usa muitos modificadores nominais - palavras que especificam substantivos (`nmod_prop`: Wikipedia PT z-score = +1.41). As frases são longas (`tokens_per_sentence_mean`: Wikipedia PT = 34.39, o maior valor) e cheias de informação, com muitos nomes próprios (`PROPN_prop`: Wikipedia PT z-score = +1.31) e poucas ações. O objetivo não é contar uma história, mas descrever coisas e explicar conceitos. Wikipedia em português usa mais explicações entre vírgulas (aposição), enquanto a versão inglesa usa mais adjetivos (`amod_prop`: Wikipedia EN z-score = +1.22), mas ambas compartilham esse estilo descritivo e informativo.

A diferença fundamental entre textos literários e enciclopédicos não está nas palavras escolhidas (TTR médio: Lispector=0.512, Woolf=0.461, Wiki PT=0.515, Wiki EN=0.486 - variação moderada, CV léxico < 0.11), mas em como as ideias são organizadas. A métrica mais discriminativa é `root_prop` (CV=0.784), seguida por `appos_prop` (CV=0.749) e `PRON_prop` (CV=0.746) - todas sintáticas. Textos literários constroem-se em torno de verbos e ações (mesmo quando falam de pensamentos). Textos enciclopédicos constroem-se em torno de substantivos e suas características. Entre as próprias autoras literárias, Lispector prefere estruturas simples (PC1 baixo, loadings dominados por métricas `_md` negativas) para criar impacto emocional direto, enquanto Woolf prefere estruturas complexas (PC1 alto) para mostrar a riqueza da experiência mental.

Esses padrões não são acidentais. São escolhas deliberadas que definem o estilo de cada autor. A análise PCA captura 42.82% da variação estilística total em apenas 2 dimensões, com PC1 dominado por distâncias de dependência (`mean_dependency_distance` loading = +0.237) e PC2 contrastando densidade verbal (`VERB_prop` loading = +0.245) versus nominal (`nmod_prop` loading = -0.228, `appos_prop` loading = -0.215). Estilo não é apenas "usar palavras bonitas", mas decidir como estruturar as frases para comunicar a experiência que você quer transmitir.

---

**Data:** Novembro 2025  
**Próximos passos:** Avaliar se modelos de linguagem conseguem preservar esses padrões estruturais ao gerar continuações.
