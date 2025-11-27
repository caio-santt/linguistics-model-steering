# Síntese: Steering de Modelos de Linguagem e Preservação de Estilo Autoral

Este trabalho investigou como diferentes técnicas de steering (direcionamento) conseguem instruir modelos de linguagem a gerar texto preservando o estilo autoral de escritores específicos. Analisamos três abordagens distintas e seus efeitos sobre características linguísticas profundas do texto gerado.

## O Problema Central

Quando pedimos para um modelo de linguagem escrever "no estilo de Machado de Assis", o que exatamente ele precisa preservar? Estilo autoral não é apenas vocabulário ou temas recorrentes, mas sim padrões estruturais profundos: como o autor organiza subordinação sintática, modifica substantivos, distribui classes gramaticais, e mantém diversidade lexical ao longo do texto. Nossa investigação mediu objetivamente essas dimensões em textos originais e gerados.

## Três Estratégias de Controle

Comparamos três formas de controlar a geração. O **método baseline** simplesmente instrui o modelo via prompt textual ("escreva como [autor]"). O **prompt steering** adiciona instruções explícitas detalhadas sobre características do estilo. Já o **activation steering** manipula diretamente as representações internas do modelo, ajustando vetores de ativação para direcionar o comportamento sem instruções textuais explícitas.

## Descoberta Principal: Controle Interno Supera Instruções Textuais

O activation steering emergiu como a técnica mais eficaz em todas as dimensões avaliadas. Ele preserva melhor o estilo original, mantém consistência entre múltiplas gerações do mesmo texto, e evita padrões artificiais de empobrecimento vocabular. Enquanto prompt steering obteve os piores resultados, o baseline surpreendentemente performou quase tão bem quanto activation steering na preservação bruta, mas falhou criticamente em aspectos temporais.

## O Problema do Empobrecimento Vocabular

Uma descoberta crítica foi identificar que o baseline sofre de **decaimento temporal artificial**: à medida que o modelo gera mais tokens, a diversidade lexical cai drasticamente, sugerindo que o vocabulário do modelo "esgota" prematuramente. Textos originais praticamente não apresentam esse padrão. Este fenômeno revela uma limitação fundamental de métodos puramente baseados em prompt: eles não controlam efetivamente a dinâmica geracional do modelo ao longo do tempo.

O activation steering, por contraste, mantém dinâmica temporal próxima aos originais, indicando que a manipulação direta de representações internas sustenta processos gerativos mais naturais. Isso sugere que estilo autoral está codificado não apenas em escolhas lexicais pontuais, mas em mecanismos atencionais e de seleção vocabular que persistem durante toda a geração.

## Consistência e Controle

Analisamos também a **previsibilidade** dos métodos: quando geramos três vezes o mesmo texto, quão similares são os resultados? Activation steering mostrou-se significativamente mais determinístico, produzindo variações mínimas. Prompt steering, ao contrário, apresentou alta variabilidade, sugerindo que instruções textuais complexas introduzem ambiguidade interpretativa no modelo.

Esta diferença tem implicações práticas importantes. Aplicações que requerem reprodutibilidade (tradução automática, sumarização) beneficiam-se de métodos consistentes. Já aplicações criativas (escrita auxiliada, brainstorming) podem preferir variabilidade controlada. O baseline ficou em posição intermediária, oferecendo consistência razoável sem manipulação complexa.

## Limitações do Controle Sintático

Apesar dos avanços, nenhum método conseguiu controlar completamente estruturas sintáticas profundas. Métricas relacionadas a subordinação, apposição e modificação adverbial apresentaram alta divergência em relação aos originais, independentemente da técnica usada. Isso indica que **padrões gramaticais complexos são menos acessíveis via steering** do que aspectos lexicais ou distribuições superficiais de classes gramaticais.

Curiosamente, métricas léxicas simples (tamanho de palavras, contagem de tokens) foram extremamente preservadas. Isto sugere uma hierarquia de controlabilidade: o steering atual afeta primariamente escolhas lexicais e distribuições estatísticas, mas não penetra profundamente na organização sintática gerativa. Estruturas como orações subordinadas e encaixes sintáticos parecem ser emergentes da arquitetura do modelo, resistindo a intervenções externas.

## Perfis Autorais: O Que Distingue Escritores?

A análise dos textos originais revelou que autores se distinguem principalmente por três dimensões. Primeiro, a **densidade de subordinação** (quantas orações funcionam como raízes sintáticas independentes). Segundo, o uso de **apposição** (estruturas explicativas ou renomeações). Terceiro, a distribuição de **classes gramaticais**, especialmente a razão entre pronomes e substantivos.

Essas dimensões capturam diferenças estilísticas fundamentais: textos literários tendem a usar mais pronomes e subordinação complexa (estilo mais "oral" e intrincado), enquanto textos expositivos privilegiam substantivos e estruturas mais diretas. Os métodos de steering conseguiram aproximar-se dessas distribuições em graus variados, mas nenhum replicou perfeitamente a assinatura autoral original.

## Implicações para Geração Controlada

Nossos resultados sugerem que **controle estilístico efetivo requer intervenção nas representações internas do modelo**, não apenas em prompts. Prompt engineering, por mais sofisticado, opera na "superfície" do modelo e introduz instabilidade. Activation steering, apesar de mais complexo tecnicamente, oferece controle mais profundo e confiável.

Contudo, mesmo técnicas avançadas ainda não dominam a gramática generativa profunda. Isso implica que aplicações exigentes (geração de textos jurídicos, médicos, ou literários que demandem precisão estrutural) ainda necessitam supervisão humana extensiva. O steering atual é promissor para controlar tom, registro e distribuições estatísticas, mas não substitui completamente o controle humano sobre estrutura discursiva complexa.

## Direções Futuras

A lacuna entre controle lexical e sintático aponta para uma fronteira de pesquisa: desenvolver métodos de steering que acessem camadas mais profundas da representação linguística nos modelos. Isso pode envolver manipulação de atenção em múltiplas camadas simultaneamente, ou treinamento de vetores de steering específicos para fenômenos sintáticos.

Outra questão em aberto é a **generalização**: steering treinado em autores específicos transfere-se para outros estilos? E para outras línguas? Nossa análise sugere que características universais (subordinação, modificação) são mais resistentes ao steering, enquanto escolhas idiossincráticas (vocabulário, preferências lexicais) são mais facilmente manipuláveis. Entender essa distinção pode informar o design de técnicas de steering mais robustas e interpretáveis.

---

**Em síntese**, este trabalho demonstra que geração controlada de estilo autoral é viável com técnicas modernas de steering, mas revela limites claros: controle lexical e estatístico é eficaz, controle sintático profundo permanece desafiador. Activation steering emerge como a técnica mais promissora, equilibrando preservação, consistência e naturalidade temporal. O caminho para controle estilístico completo passa necessariamente por compreender e manipular as representações linguísticas internas dos modelos de linguagem, não apenas suas interfaces textuais.
