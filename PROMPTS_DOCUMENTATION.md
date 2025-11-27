# Prompts de Geração - Documentação

Este arquivo documenta os prompts utilizados para geração dos textos nas três condições experimentais.

## 📝 System Prompt (Universal)

**ID:** `continuation_system`  
**Línguas:** Todas  

```
You are a model specialized in continuing narratives.
Rules:
- Write ONLY the continuation of the story.
- Do not repeat the introductory section.
- Do not explain what you are doing, just narrate.
- Maintain the same language as the introductory text: {target_lang}.
- The continuation should have approximately {tokens} tokens.
```

---

## 🇧🇷 Prompts em Português

### **Baseline (continue_plain)**

**Método:** Raw prompt sem instruções estilísticas  
**Template:**

```
Continue a narrativa abaixo mantendo o mesmo estilo, tom e foco narrativo.
Não repita trechos já apresentados.

TEXTO:
{text}
```

**Características:**
- Instrução genérica: "mantendo o mesmo estilo"
- Sem especificações estilométricas
- Modelo decide autonomamente como interpretar "estilo"

---

### **Prompt Steering (continue_with_style)**

**Método:** Prompt com descrição estilométrica detalhada  
**Template:**

```
Continue este texto mantendo as seguintes características estilísticas:
- Use frases curtas e diretas, com estrutura sintática simples
- Mantenha alta densidade de verbos e advérbios, criando dinamismo narrativo
- Prefira vocabulário variado, mas com palavras curtas e acessíveis
- Evite excesso de adjetivos e substantivos, priorizando ação e modificação
- Mantenha tom introspectivo e fluxo narrativo contínuo

TEXTO:
{text}
```

**Características estilísticas especificadas:**
1. **Sintaxe:** Frases curtas, estrutura simples
2. **Classes gramaticais:** Alta densidade de verbos/advérbios, baixa de adjetivos/substantivos
3. **Léxico:** Variado, palavras curtas
4. **Tom:** Introspectivo, fluxo contínuo

**Observação crítica:** Este perfil descreve estilo **literário genérico**, não específico de Lispector. As instruções focam em dinamismo e simplicidade sintática, o que pode não capturar complexidade subordinativa de textos literários.

---

## 🇬🇧 Prompts em Inglês

### **Baseline (continue_plain)**

**Método:** Raw prompt sem instruções estilísticas  
**Template:**

```
Continue the story below, keeping the same style, tone, and narrative focus.
Do not repeat text that is already given.

TEXT:
{text}
```

---

### **Prompt Steering (continue_with_style)**

**Método:** Prompt com descrição estilométrica detalhada  
**Template:**

```
Continue this text maintaining the following stylistic features:
- Use complex syntactic structures with high dependency distances
- Employ high pronoun density for subjective, stream-of-consciousness narrative
- Keep moderate sentence length with intricate internal structure
- Use short, simple words but arrange them in elaborate patterns
- Maintain low nominal and adjectival density, focusing on psychological depth
- Create flowing, interconnected clauses that mirror thought processes

TEXT:
{text}
```

**Características estilísticas especificadas:**
1. **Sintaxe:** Estruturas complexas, alta dependency distance
2. **Classes gramaticais:** Alta densidade pronominal, baixa nominal/adjetival
3. **Sentenças:** Tamanho moderado, estrutura interna intrincada
4. **Léxico:** Palavras curtas e simples
5. **Tom:** Profundidade psicológica, stream-of-consciousness
6. **Coesão:** Cláusulas interconectadas, fluxo de pensamento

**Observação crítica:** Este perfil descreve estilo de **Woolf/modernismo** de forma mais precisa que o português. Captura aspectos como stream-of-consciousness e alta subordinação.

---

## 🔄 Activation Steering

**Método:** Manipulação de representações internas (camada 12)  
**Prompt usado:** `continue_plain` (raw prompt, sem instruções)

**Diferença:** Não usa prompt especializado. O controle vem da adição de vetores de steering calculados contrafactualmente:
```
steering_vector = mean(activations_literary) - mean(activations_encyclopedic)
```

Aplicado durante geração na camada 12, escala 1.0.

---

## 📄 Metadados

**Modelo:** `openai/gpt-oss-20b`  
**Tokens de continuação:** ~500 tokens por geração  
**Temperatura:** [Não especificado - **ADICIONAR**]  
**Top-p:** [Não especificado - **ADICIONAR**]  
**Repetições:** 3 por condição/sample  

**Última atualização:** Novembro 2025
