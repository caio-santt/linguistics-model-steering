"""
Script principal para extração de métricas de todos os textos.

Executa:
1. Métricas full text (léxicas + sintáticas) para todos os 600 textos
2. Métricas windowed léxicas (5 janelas) para textos >= 100 tokens
3. Métricas windowed sintáticas (3 segmentos) para textos >= 100 tokens (opcional)

Uso:
    python extract_all_metrics.py [--skip-windowed] [--skip-syntactic-windowed]
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import sys
import warnings

# Adicionar path do módulo
sys.path.append(str(Path(__file__).parent))

from basic_metrics import BasicMetrics
from syntactic_metrics import SyntacticMetrics
from windowed_analysis import WindowedAnalysis, validate_text_for_windowed_analysis

warnings.filterwarnings('ignore')


class MetricsExtractor:
    """
    Orquestra extração de métricas para todos os textos.
    """
    
    def __init__(
        self,
        data_dir: Path,
        output_dir: Path,
        min_tokens_windowed: int = 100,
        n_windows_lexical: int = 5,
        n_segments_syntactic: int = 3
    ):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.min_tokens_windowed = min_tokens_windowed
        self.n_windows_lexical = n_windows_lexical
        self.n_segments_syntactic = n_segments_syntactic
        
        # Criar diretórios de output
        (self.output_dir / 'full_text' / 'individual').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'full_text' / 'summary').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'windowed').mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'udpipe_output').mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Data directory: {self.data_dir}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"⚙️  Min tokens for windowed: {self.min_tokens_windowed}")
        print(f"⚙️  Windows (lexical): {self.n_windows_lexical}")
        print(f"⚙️  Segments (syntactic): {self.n_segments_syntactic}")
    
    def read_text_file(self, filepath: Path) -> str:
        """Lê arquivo de texto."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_metadata_from_path(self, filepath: Path, dataset_type: str) -> dict:
        """
        Extrai metadados do caminho do arquivo.
        
        Parameters
        ----------
        filepath : Path
            Caminho do arquivo
        dataset_type : str
            Tipo: 'original', 'baseline', 'prompt_steering', 'activation_steering'
        
        Returns
        -------
        dict
            Metadados: author, title, sample_idx, rep, condition, etc.
        """
        parts = filepath.stem.split('__')
        
        if dataset_type == 'original':
            # original: {title}__s{sample}.txt
            title = parts[0]
            sample_idx = int(parts[1].replace('s', ''))
            rep = None
        else:
            # generated: {title}__s{sample}__r{rep}.txt
            title = parts[0]
            sample_idx = int(parts[1].replace('s', ''))
            rep = int(parts[2].replace('r', ''))
        
        author = filepath.parent.name
        
        # Mapear lang
        if author in ['lispector', 'wikipedia_pt']:
            lang = 'pt'
        else:
            lang = 'eng'
        
        return {
            'text_id': filepath.stem,
            'author': author,
            'title': title,
            'sample_idx': sample_idx,
            'rep': rep,
            'condition': dataset_type,
            'lang': lang
        }
    
    def collect_all_texts(self) -> pd.DataFrame:
        """
        Coleta todos os textos do dataset.
        
        Returns
        -------
        DataFrame com colunas: text_id, filepath, author, title, sample_idx, 
                               rep, condition, lang, text
        """
        records = []
        
        # Originais
        print("\n📖 Coletando textos ORIGINAIS...")
        original_dir = self.data_dir / 'data' / 'original'
        for author_dir in original_dir.iterdir():
            if not author_dir.is_dir():
                continue
            for txt_file in author_dir.glob('*.txt'):
                metadata = self.extract_metadata_from_path(txt_file, 'original')
                metadata['filepath'] = str(txt_file)
                metadata['text'] = self.read_text_file(txt_file)
                records.append(metadata)
        print(f"  ✓ {len(records)} textos originais")
        
        # Gerados - 3 condições
        conditions = [
            ('00_BASELINE-raw_prompt', 'baseline'),
            ('01_PROMPT_STEERING-style-description', 'prompt_steering'),
            ('02_ACTIVATION_STEERING-raw-prompt', 'activation_steering')
        ]
        
        for folder_name, condition_name in conditions:
            print(f"\n📖 Coletando textos {condition_name.upper()}...")
            gen_dir = self.data_dir / 'data' / 'generated' / folder_name
            count_before = len(records)
            
            for author_dir in gen_dir.iterdir():
                if not author_dir.is_dir():
                    continue
                for txt_file in author_dir.glob('*.txt'):
                    metadata = self.extract_metadata_from_path(txt_file, condition_name)
                    metadata['filepath'] = str(txt_file)
                    metadata['text'] = self.read_text_file(txt_file)
                    records.append(metadata)
            
            print(f"  ✓ {len(records) - count_before} textos {condition_name}")
        
        df = pd.DataFrame(records)
        print(f"\n✅ Total coletado: {len(df)} textos")
        return df
    
    def extract_full_text_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extrai métricas full text (léxicas + sintáticas) para todos os textos.
        """
        print("\n" + "="*60)
        print("EXTRAINDO MÉTRICAS FULL TEXT")
        print("="*60)
        
        results = []
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing texts"):
            text = row['text']
            lang = row['lang']
            condition = row['condition']
            # Include condition in text_id to avoid overwriting CoNLL-U files
            text_id = f"{row['text_id']}_{condition}"
            
            # Metadados
            record = {
                'text_id': text_id,
                'author': row['author'],
                'title': row['title'],
                'sample_idx': row['sample_idx'],
                'rep': row['rep'],
                'condition': row['condition'],
                'lang': lang
            }
            
            # Métricas léxicas
            try:
                basic = BasicMetrics(text, lang=lang)
                basic_results = basic.run()
                for k, v in basic_results.items():
                    record[f'basic_{k}'] = v
            except Exception as e:
                print(f"\n⚠️  Erro ao calcular métricas básicas para {text_id}: {e}")
                # Preencher com NaN
                for k in ['ttr', 'tokens_per_sentence_mean', 'chars_per_token_mean',
                         'n_unique_unigrams', 'n_unique_bigrams', 'n_repeated_bigrams',
                         'n_unique_trigrams', 'n_repeated_trigrams']:
                    record[f'basic_{k}'] = np.nan
            
            # Métricas sintáticas
            try:
                synt_lang = 'pt' if lang == 'pt' else 'eng'
                conllu_path = str(self.output_dir / 'udpipe_output')
                synt = SyntacticMetrics(
                    text=text,
                    lang=synt_lang,
                    text_id=text_id,
                    conllu_path=conllu_path
                )
                synt_results = synt.run()
                for k, v in synt_results.items():
                    record[f'synt_{k}'] = v
            except Exception as e:
                print(f"\n⚠️  Erro ao calcular métricas sintáticas para {text_id}: {e}")
                # Preencher com NaN
                record['synt_mean_dependency_distance'] = np.nan
            
            results.append(record)
        
        df_metrics = pd.DataFrame(results)
        print(f"\n✅ Métricas full text extraídas: {len(df_metrics)} textos")
        return df_metrics
    
    def extract_windowed_lexical_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extrai métricas léxicas em janelas para textos >= min_tokens.
        """
        print("\n" + "="*60)
        print("EXTRAINDO MÉTRICAS WINDOWED LÉXICAS")
        print("="*60)
        
        # Filtrar textos válidos
        valid_texts = []
        for idx, row in df.iterrows():
            is_valid, reason = validate_text_for_windowed_analysis(
                row['text'], row['lang'], self.min_tokens_windowed
            )
            if is_valid:
                valid_texts.append(row)
        
        print(f"📊 Textos válidos para windowed: {len(valid_texts)}/{len(df)}")
        print(f"   Excluídos: {len(df) - len(valid_texts)} textos < {self.min_tokens_windowed} tokens")
        
        results = []
        
        for row in tqdm(valid_texts, desc="Processing windows"):
            text = row['text']
            lang = row['lang']
            text_id = row['text_id']
            
            # Criar janelas
            wa = WindowedAnalysis(
                text=text,
                lang=lang,
                n_windows=self.n_windows_lexical,
                respect_sentences=False  # Divisão por tokens para léxicas
            )
            windows = wa.create_windows()
            
            # Calcular métricas para cada janela
            for window in windows:
                record = {
                    'text_id': text_id,
                    'author': row['author'],
                    'title': row['title'],
                    'sample_idx': row['sample_idx'],
                    'rep': row['rep'],
                    'condition': row['condition'],
                    'lang': lang,
                    'window_idx': window['idx'],
                    'window_position': window['position'],
                    'window_position_numeric': window['position_numeric'],
                    'window_n_tokens': window['n_tokens']
                }
                
                # Calcular métricas básicas para a janela
                try:
                    basic = BasicMetrics(window['text'], lang=lang)
                    basic_results = basic.run()
                    for k, v in basic_results.items():
                        record[k] = v
                except Exception as e:
                    print(f"\n⚠️  Erro na janela {window['idx']} de {text_id}: {e}")
                    for k in ['ttr', 'tokens_per_sentence_mean', 'chars_per_token_mean',
                             'n_unique_unigrams', 'n_unique_bigrams', 'n_repeated_bigrams',
                             'n_unique_trigrams', 'n_repeated_trigrams']:
                        record[k] = np.nan
                
                results.append(record)
        
        df_windowed = pd.DataFrame(results)
        print(f"\n✅ Métricas windowed extraídas: {len(df_windowed)} janelas")
        return df_windowed
    
    def save_results(
        self,
        df_full: pd.DataFrame,
        df_windowed: pd.DataFrame = None
    ):
        """
        Salva resultados em CSVs organizados.
        """
        print("\n" + "="*60)
        print("SALVANDO RESULTADOS")
        print("="*60)
        
        # Full text individual
        output_path = self.output_dir / 'full_text' / 'individual' / 'all_texts.csv'
        df_full.to_csv(output_path, index=False)
        print(f"✓ Full text individual: {output_path}")
        
        # Full text por condição
        for condition in df_full['condition'].unique():
            df_cond = df_full[df_full['condition'] == condition]
            output_path = self.output_dir / 'full_text' / 'individual' / f'{condition}.csv'
            df_cond.to_csv(output_path, index=False)
            print(f"  ├─ {condition}: {len(df_cond)} textos")
        
        # Sumário por autor
        metric_cols = [c for c in df_full.columns if c.startswith('basic_') or c.startswith('synt_')]
        df_summary_author = df_full.groupby('author')[metric_cols].mean().reset_index()
        output_path = self.output_dir / 'full_text' / 'summary' / 'by_author.csv'
        df_summary_author.to_csv(output_path, index=False)
        print(f"✓ Sumário por autor: {output_path}")
        
        # Sumário por condição
        df_summary_cond = df_full.groupby('condition')[metric_cols].mean().reset_index()
        output_path = self.output_dir / 'full_text' / 'summary' / 'by_condition.csv'
        df_summary_cond.to_csv(output_path, index=False)
        print(f"✓ Sumário por condição: {output_path}")
        
        # Windowed
        if df_windowed is not None and len(df_windowed) > 0:
            output_path = self.output_dir / 'windowed' / 'lexical_windowed.csv'
            df_windowed.to_csv(output_path, index=False)
            print(f"✓ Windowed léxicas: {output_path}")
            print(f"  └─ {len(df_windowed)} janelas")
        
        print("\n✅ Todos os resultados salvos!")


def main():
    parser = argparse.ArgumentParser(description='Extract metrics from all texts')
    parser.add_argument(
        '--data-dir',
        type=str,
        default='.',
        help='Directory containing data/ folder'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='metrics',
        help='Output directory for metrics'
    )
    parser.add_argument(
        '--skip-windowed',
        action='store_true',
        help='Skip windowed analysis'
    )
    parser.add_argument(
        '--min-tokens',
        type=int,
        default=100,
        help='Minimum tokens for windowed analysis'
    )
    
    args = parser.parse_args()
    
    # Inicializar extractor
    extractor = MetricsExtractor(
        data_dir=Path(args.data_dir),
        output_dir=Path(args.output_dir),
        min_tokens_windowed=args.min_tokens
    )
    
    # Coletar textos
    df_texts = extractor.collect_all_texts()
    
    # Extrair métricas full text
    df_full = extractor.extract_full_text_metrics(df_texts)
    
    # Extrair métricas windowed
    df_windowed = None
    if not args.skip_windowed:
        df_windowed = extractor.extract_windowed_lexical_metrics(df_texts)
    
    # Salvar resultados
    extractor.save_results(df_full, df_windowed)
    
    print("\n" + "="*60)
    print("EXTRAÇÃO CONCLUÍDA COM SUCESSO! 🎉")
    print("="*60)


if __name__ == "__main__":
    main()
