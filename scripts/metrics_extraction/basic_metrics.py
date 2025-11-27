"""
Módulo para cálculo de métricas léxicas básicas.
Adaptado do código original com melhorias de robustez e documentação.
"""

from __future__ import division
import numpy as np
import nltk
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer, RSLPStemmer
from nltk.data import find
from typing import Dict, List, Optional


# ======================================================
# Helpers para garantir recursos NLTK sem quebrar
# ======================================================

def _ensure_nltk_resource(path: str, download_name: Optional[str] = None) -> bool:
    """
    Tenta localizar um recurso NLTK. Se não achar e download_name for dado,
    tenta fazer nltk.download(download_name). Se nada der certo, devolve False.
    """
    try:
        find(path)
        return True
    except LookupError:
        if download_name is None:
            return False
        try:
            nltk.download(download_name, quiet=True)
            find(path)
            return True
        except Exception:
            return False


# Verificar recursos disponíveis
HAS_PUNKT = _ensure_nltk_resource("tokenizers/punkt", "punkt") or _ensure_nltk_resource("tokenizers/punkt_tab", "punkt_tab")
HAS_WORDNET = _ensure_nltk_resource("corpora/wordnet", "wordnet")
HAS_OMW = _ensure_nltk_resource("corpora/omw-1.4", "omw-1.4")
HAS_RSLP = _ensure_nltk_resource("stemmers/rslp", "rslp")


def _sent_tokenize_safe(text: str, language: str) -> List[str]:
    """
    Usa nltk.sent_tokenize se possível; senão, faz um fallback grosseiro.
    """
    if HAS_PUNKT:
        try:
            return nltk.sent_tokenize(text, language=language)
        except (LookupError, ValueError):
            pass
    # fallback: tudo em uma sentença só
    return [text]


def _word_tokenize_safe(sent: str, language: str) -> List[str]:
    """
    Usa nltk.word_tokenize se possível; senão, split por espaço.
    """
    if HAS_PUNKT:
        try:
            return nltk.word_tokenize(sent, language=language)
        except (LookupError, ValueError):
            pass
    return sent.split()


class BasicMetrics:
    """
    Calcula métricas léxicas e de n-gramas para UM texto.
    
    Parameters
    ----------
    text : str
        Texto completo a ser analisado
    lang : str
        Idioma do texto ('pt' para português, 'eng' para inglês)
    
    Attributes
    ----------
    results : dict
        Dicionário com todas as métricas calculadas
    
    Métricas calculadas
    -------------------
    - ttr: Type-Token Ratio (diversidade lexical)
    - tokens_per_sentence_mean: Média de tokens por sentença
    - chars_per_token_mean: Média de caracteres por token (apenas tokens alfabéticos)
    - n_unique_unigrams: Número de unigramas únicos
    - n_unique_bigrams: Número de bigramas únicos
    - n_repeated_bigrams: Número de bigramas repetidos
    - n_unique_trigrams: Número de trigramas únicos
    - n_repeated_trigrams: Número de trigramas repetidos
    """

    def __init__(self, text: str, lang: str = "eng"):
        self.text = text
        self.lang = lang
        self.results = {}

    def run(self) -> Dict[str, float]:
        """
        Executa todos os cálculos de métricas.
        
        Returns
        -------
        dict
            Dicionário com todas as métricas calculadas
        """
        # Métricas pré-lematização
        self.metrics_pre_lemmatization()

        # Aplicar redução radical (lemmatization/stemming)
        lemma_text = self.radical_reduction(self.text, self.lang)
        
        # Calcular n-gramas no texto normalizado
        self.generate_unigrams(lemma_text)
        self.generate_bigrams(lemma_text)
        self.generate_trigrams(lemma_text)

        return self.results

    def generate_unigrams(self, text: str) -> None:
        """Calcula métricas de unigramas."""
        unigrams = self.ngram_convertor(text, 1)
        self.results.update({
            'n_unique_unigrams': len(set(unigrams))
        })

    def generate_bigrams(self, text: str) -> None:
        """Calcula métricas de bigramas (únicos e repetidos)."""
        bigrams = self.ngram_convertor(text, 2)
        unique_bi = set(bigrams)

        # Contar repetições
        repet = {}
        for bg in bigrams:
            repet[bg] = repet.get(bg, 0) + 1
        repet = {bg: c for bg, c in repet.items() if c > 1}

        self.results.update({
            'n_unique_bigrams': len(unique_bi),
            'n_repeated_bigrams': sum(repet.values())
        })

    def generate_trigrams(self, text: str) -> None:
        """Calcula métricas de trigramas (únicos e repetidos)."""
        trigrams = self.ngram_convertor(text, 3)
        unique_tri = set(trigrams)

        # Contar repetições
        repet = {}
        for tg in trigrams:
            repet[tg] = repet.get(tg, 0) + 1
        repet = {tg: c for tg, c in repet.items() if c > 1}

        self.results.update({
            'n_unique_trigrams': len(unique_tri),
            'n_repeated_trigrams': sum(repet.values())
        })

    def metrics_pre_lemmatization(self) -> None:
        """
        Calcula métricas antes da lematização:
        - TTR (type-token ratio)
        - média de tokens por sentença
        - média de caracteres por token (apenas tokens alfabéticos)
        """
        language = "portuguese" if self.lang == "pt" else "english"

        sentences = _sent_tokenize_safe(self.text, language=language)
        tokens_per_sentence = []
        all_tokens = []
        chars_per_token = []

        for sent in sentences:
            tokens = _word_tokenize_safe(sent, language=language)
            tokens_per_sentence.append(len(tokens))
            all_tokens.extend(tokens)

        chars_per_token = [len(t) for t in all_tokens if t.isalpha()]

        if all_tokens:
            ttr = len(set(all_tokens)) / len(all_tokens)
        else:
            ttr = 0

        mean_tok_sent = np.mean(tokens_per_sentence) if tokens_per_sentence else 0
        mean_char_tok = np.mean(chars_per_token) if chars_per_token else 0

        self.results.update({
            'ttr': ttr,
            'tokens_per_sentence_mean': mean_tok_sent,
            'chars_per_token_mean': mean_char_tok
        })

    @staticmethod
    def ngram_convertor(text: str, n: int) -> List[tuple]:
        """
        Converte um texto em lista de n-gramas de tamanho n.
        Usa split simples — assume que `text` já está tokenizado de forma razoável.
        """
        tokens = text.split()
        return list(ngrams(tokens, n)) if len(tokens) >= n else []

    @staticmethod
    def radical_reduction(text: str, lang: str = "eng") -> str:
        """
        Para 'eng': tokeniza, lematiza com WordNet e recompõe o texto.
        Para 'pt': tokeniza, aplica stemmer RSLP e recompõe o texto.
        
        Se recursos não estiverem disponíveis, retorna texto original.
        """
        if lang == "pt":
            language = "portuguese"
            if not HAS_RSLP:
                return text

            stemmer = RSLPStemmer()
            sentences = _sent_tokenize_safe(text, language=language)
            proc_sents = []
            for sent in sentences:
                words = _word_tokenize_safe(sent, language=language)
                stemmed = [stemmer.stem(w) for w in words]
                proc_sents.append(' '.join(stemmed))
            return ' '.join(proc_sents)
        else:
            language = "english"
            if not HAS_WORDNET:
                return text

            lemmatizer = WordNetLemmatizer()
            sentences = _sent_tokenize_safe(text, language=language)
            proc_sents = []
            for sent in sentences:
                words = _word_tokenize_safe(sent, language=language)
                lemmatized = [lemmatizer.lemmatize(w) for w in words]
                proc_sents.append(' '.join(lemmatized))
            return ' '.join(proc_sents)


if __name__ == "__main__":
    # Teste simples
    exemplo_pt = (
        "Este é apenas um pequeno exemplo para demonstrar como calculamos "
        "as métricas em um único texto. Repetimos algumas palavras, "
        "palavras repetimos, e assim por diante."
    )

    exemplo_en = (
        "This is just a small example to show how we compute metrics "
        "on a single text. We repeat some words, words repeat, and so on."
    )

    print("---- Português ----")
    bm_pt = BasicMetrics(exemplo_pt, lang="pt")
    resultados_pt = bm_pt.run()
    for k, v in resultados_pt.items():
        print(f"{k:25}: {v}")

    print("\n---- English ----")
    bm_en = BasicMetrics(exemplo_en, lang="eng")
    resultados_en = bm_en.run()
    for k, v in resultados_en.items():
        print(f"{k:25}: {v}")
