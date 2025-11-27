"""
Script de teste rápido para validar módulos antes da execução completa.
"""

import sys
from pathlib import Path

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent))

from basic_metrics import BasicMetrics
from syntactic_metrics import SyntacticMetrics
from windowed_analysis import WindowedAnalysis, validate_text_for_windowed_analysis


def test_basic_metrics():
    """Testa métricas léxicas."""
    print("="*60)
    print("TESTE: Métricas Léxicas")
    print("="*60)
    
    text_pt = (
        "Este é um texto de exemplo em português. "
        "Este texto contém várias sentenças. "
        "Vamos repetir algumas palavras para testar. "
        "Palavras repetidas são importantes para análise."
    )
    
    text_en = (
        "This is an example text in English. "
        "This text contains several sentences. "
        "We will repeat some words to test. "
        "Repeated words are important for analysis."
    )
    
    print("\n1. Português:")
    metrics_pt = BasicMetrics(text_pt, lang='pt')
    results_pt = metrics_pt.run()
    
    for key in ['ttr', 'tokens_per_sentence_mean', 'n_unique_unigrams', 'n_unique_bigrams']:
        print(f"  {key}: {results_pt.get(key, 'N/A')}")
    
    print("\n2. English:")
    metrics_en = BasicMetrics(text_en, lang='eng')
    results_en = metrics_en.run()
    
    for key in ['ttr', 'tokens_per_sentence_mean', 'n_unique_unigrams', 'n_unique_bigrams']:
        print(f"  {key}: {results_en.get(key, 'N/A')}")
    
    print("\n✅ Métricas léxicas OK")
    return True


def test_windowed_analysis():
    """Testa análise em janelas."""
    print("\n" + "="*60)
    print("TESTE: Análise Windowed")
    print("="*60)
    
    text = (
        "This is sentence one. This is sentence two. "
        "This is sentence three. This is sentence four. "
        "This is sentence five. This is sentence six. "
        "This is sentence seven. This is sentence eight. "
        "This is sentence nine. This is sentence ten. " * 3
    )
    
    print("\n1. Validação:")
    is_valid, reason = validate_text_for_windowed_analysis(text, 'eng', min_tokens=100)
    print(f"  Valid: {is_valid}")
    print(f"  Reason: {reason}")
    
    if is_valid:
        print("\n2. Criando 5 janelas (por tokens):")
        wa = WindowedAnalysis(text, lang='eng', n_windows=5, respect_sentences=False)
        windows = wa.create_windows()
        
        for w in windows:
            print(f"  Window {w['idx']} ({w['position']}): {w['n_tokens']} tokens")
        
        print("\n3. Criando 3 segmentos (por sentenças):")
        wa_sent = WindowedAnalysis(text, lang='eng', n_windows=3, respect_sentences=True)
        segments = wa_sent.create_windows()
        
        for s in segments:
            print(f"  Segment {s['idx']} ({s['position']}): {s['n_sentences']} sentences, {s['n_tokens']} tokens")
    
    print("\n✅ Análise windowed OK")
    return True


def test_syntactic_metrics():
    """Testa métricas sintáticas (requer API UDPipe)."""
    print("\n" + "="*60)
    print("TESTE: Métricas Sintáticas (UDPipe)")
    print("="*60)
    print("\n⚠️  Este teste requer conexão com API UDPipe")
    print("    Pode demorar ~30 segundos...")
    
    response = input("\nExecutar teste de UDPipe? (s/N): ")
    
    if response.lower() != 's':
        print("⏭️  Pulando teste de métricas sintáticas")
        return True
    
    text = "The cat sat on the mat. The dog ran in the park."
    
    print("\nProcessando texto...")
    try:
        metrics = SyntacticMetrics(
            text=text,
            lang='eng',
            text_id='test_syntactic',
            conllu_path='test_udpipe_output'
        )
        results = metrics.run()
        
        print(f"\n✅ {len(results)} métricas calculadas")
        print("\nAmostra de resultados:")
        for key in list(results.keys())[:5]:
            print(f"  {key}: {results[key]}")
        
        # Limpar arquivo de teste
        import shutil
        test_dir = Path('test_udpipe_output')
        if test_dir.exists():
            shutil.rmtree(test_dir)
        
        print("\n✅ Métricas sintáticas OK")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao testar métricas sintáticas: {e}")
        print("    Verifique conexão com API UDPipe")
        return False


def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("VALIDAÇÃO DE MÓDULOS")
    print("="*60)
    
    results = []
    
    # Teste 1: Métricas léxicas
    try:
        results.append(("Métricas Léxicas", test_basic_metrics()))
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        results.append(("Métricas Léxicas", False))
    
    # Teste 2: Análise windowed
    try:
        results.append(("Análise Windowed", test_windowed_analysis()))
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        results.append(("Análise Windowed", False))
    
    # Teste 3: Métricas sintáticas (opcional)
    try:
        results.append(("Métricas Sintáticas", test_syntactic_metrics()))
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        results.append(("Métricas Sintáticas", False))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 Todos os testes passaram!")
        print("   Sistema pronto para execução completa.")
    else:
        print("\n⚠️  Alguns testes falharam.")
        print("   Verifique erros acima antes de executar pipeline completo.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
