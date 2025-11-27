"""
Módulo para análise temporal (windowed) de métricas.
Divide textos em janelas e calcula métricas para cada janela.
"""

import nltk
from typing import List, Dict, Tuple
from pathlib import Path


class WindowedAnalysis:
    """
    Divide textos em janelas e prepara para análise temporal.
    
    Parameters
    ----------
    text : str
        Texto completo a ser dividido
    lang : str
        Idioma do texto ('pt' ou 'eng')
    n_windows : int
        Número de janelas a criar (padrão: 5)
    respect_sentences : bool
        Se True, divide respeitando limites de sentença (para sintáticas)
        Se False, divide por tokens simples (para léxicas)
    """
    
    def __init__(
        self,
        text: str,
        lang: str = 'eng',
        n_windows: int = 5,
        respect_sentences: bool = False
    ):
        self.text = text
        self.lang = lang
        self.n_windows = n_windows
        self.respect_sentences = respect_sentences
        
        # Mapear idioma para NLTK
        self.nltk_lang = "portuguese" if lang == "pt" else "english"
        
    def create_windows(self) -> List[Dict[str, any]]:
        """
        Cria janelas do texto.
        
        Returns
        -------
        list of dict
            Lista de dicionários, cada um contendo:
            - idx: índice da janela (0 a n_windows-1)
            - position: posição relativa no texto (0%, 20%, 40%, etc.)
            - text: texto da janela
            - n_tokens: número de tokens
            - n_sentences: número de sentenças (se respect_sentences=True)
        """
        if self.respect_sentences:
            return self._create_windows_by_sentences()
        else:
            return self._create_windows_by_tokens()
    
    def _create_windows_by_tokens(self) -> List[Dict[str, any]]:
        """
        Cria janelas dividindo por tokens simples.
        Usado para métricas léxicas.
        """
        # Tokenizar
        tokens = nltk.word_tokenize(self.text, language=self.nltk_lang)
        total_tokens = len(tokens)
        
        if total_tokens == 0:
            return []
        
        window_size = total_tokens // self.n_windows
        windows = []
        
        for i in range(self.n_windows):
            start = i * window_size
            # Última janela pega tokens restantes
            end = start + window_size if i < self.n_windows - 1 else total_tokens
            
            window_tokens = tokens[start:end]
            window_text = ' '.join(window_tokens)
            
            windows.append({
                'idx': i,
                'position': f'{i * 100 // self.n_windows}%',
                'position_numeric': i / self.n_windows,
                'start_token': start,
                'end_token': end,
                'text': window_text,
                'n_tokens': len(window_tokens),
                'n_sentences': None  # Não calculado para divisão por tokens
            })
        
        return windows
    
    def _create_windows_by_sentences(self) -> List[Dict[str, any]]:
        """
        Cria janelas dividindo por sentenças completas.
        Usado para métricas sintáticas (preserva integridade da árvore).
        """
        # Tokenizar sentenças
        sentences = nltk.sent_tokenize(self.text, language=self.nltk_lang)
        
        if not sentences:
            return []
        
        # Calcular tamanho de cada sentença em tokens
        sent_lens = []
        for sent in sentences:
            tokens = nltk.word_tokenize(sent, language=self.nltk_lang)
            sent_lens.append(len(tokens))
        
        total_tokens = sum(sent_lens)
        target_per_window = total_tokens // self.n_windows
        
        # Dividir sentenças em janelas
        windows = []
        current_sentences = []
        current_size = 0
        
        for i, (sent, sent_len) in enumerate(zip(sentences, sent_lens)):
            current_sentences.append(sent)
            current_size += sent_len
            
            # Quando passar do target, fechar janela (exceto última)
            if current_size >= target_per_window and len(windows) < self.n_windows - 1:
                window_text = ' '.join(current_sentences)
                windows.append({
                    'idx': len(windows),
                    'position': f'{len(windows) * 100 // self.n_windows}%',
                    'position_numeric': len(windows) / self.n_windows,
                    'text': window_text,
                    'n_tokens': current_size,
                    'n_sentences': len(current_sentences)
                })
                current_sentences = []
                current_size = 0
        
        # Última janela pega sentenças restantes
        if current_sentences or len(windows) < self.n_windows:
            window_text = ' '.join(current_sentences)
            windows.append({
                'idx': len(windows),
                'position': f'{len(windows) * 100 // self.n_windows}%',
                'position_numeric': len(windows) / self.n_windows,
                'text': window_text,
                'n_tokens': current_size,
                'n_sentences': len(current_sentences)
            })
        
        return windows


def validate_text_for_windowed_analysis(text: str, lang: str, min_tokens: int = 100) -> Tuple[bool, str]:
    """
    Valida se um texto é adequado para análise windowed.
    
    Parameters
    ----------
    text : str
        Texto a validar
    lang : str
        Idioma do texto
    min_tokens : int
        Número mínimo de tokens requerido
    
    Returns
    -------
    tuple
        (is_valid, reason)
        - is_valid: True se o texto é adequado, False caso contrário
        - reason: Mensagem explicando validação
    """
    nltk_lang = "portuguese" if lang == "pt" else "english"
    
    try:
        tokens = nltk.word_tokenize(text, language=nltk_lang)
        n_tokens = len(tokens)
        
        if n_tokens < min_tokens:
            return False, f"Texto muito curto: {n_tokens} tokens (mínimo: {min_tokens})"
        
        return True, f"OK: {n_tokens} tokens"
    
    except Exception as e:
        return False, f"Erro ao tokenizar: {str(e)}"


if __name__ == "__main__":
    # Teste simples
    text_example = (
        "This is the first sentence. This is the second sentence. "
        "This is the third sentence. This is the fourth sentence. "
        "This is the fifth sentence. This is the sixth sentence. "
        "This is the seventh sentence. This is the eighth sentence. "
        "This is the ninth sentence. This is the tenth sentence."
    )
    
    print("=== Testing WindowedAnalysis ===\n")
    
    # Teste divisão por tokens
    print("1. Division by tokens (for lexical metrics):")
    wa_tokens = WindowedAnalysis(text_example, lang='eng', n_windows=5, respect_sentences=False)
    windows_tokens = wa_tokens.create_windows()
    
    for w in windows_tokens:
        print(f"  Window {w['idx']} ({w['position']}): {w['n_tokens']} tokens")
        print(f"    Preview: {w['text'][:60]}...")
    
    print("\n2. Division by sentences (for syntactic metrics):")
    wa_sents = WindowedAnalysis(text_example, lang='eng', n_windows=5, respect_sentences=True)
    windows_sents = wa_sents.create_windows()
    
    for w in windows_sents:
        print(f"  Window {w['idx']} ({w['position']}): {w['n_sentences']} sentences, {w['n_tokens']} tokens")
    
    print("\n3. Validation test:")
    is_valid, reason = validate_text_for_windowed_analysis(text_example, 'eng', min_tokens=100)
    print(f"  Valid: {is_valid}, Reason: {reason}")
    
    short_text = "Too short."
    is_valid, reason = validate_text_for_windowed_analysis(short_text, 'eng', min_tokens=100)
    print(f"  Valid: {is_valid}, Reason: {reason}")
