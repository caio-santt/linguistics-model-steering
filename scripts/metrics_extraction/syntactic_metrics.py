"""
Módulo para cálculo de métricas sintáticas usando UDPipe.
Adaptado do código original com melhorias de robustez e documentação.
"""

import os
import re
import shlex
import subprocess
from typing import Dict, List, Optional
from pathlib import Path


class SyntacticMetrics:
    """
    Calcula métricas sintáticas usando a API UDPipe.
    
    Parameters
    ----------
    text : str
        Texto a ser analisado
    lang : str
        Idioma do texto ('pt' ou 'eng')
    text_id : str
        Identificador único do texto (para nomear arquivo CoNLL-U)
    conllu_path : str
        Caminho para salvar arquivos CoNLL-U
    parser_url : str
        URL da API UDPipe
    
    Attributes
    ----------
    final_results : dict
        Dicionário com todas as métricas calculadas
    sentence_tree : list
        Árvore de sentenças parseada do CoNLL-U
    
    Métricas calculadas
    -------------------
    - mean_dependency_distance: Distância média de dependência sintática
    - Para cada relação DEPREL:
        * {DEPREL}_prop: Proporção da relação
        * {DEPREL}_md: Distância média
        * count_{DEPREL}: Contagem absoluta
    - Para cada tag UPOS:
        * {UPOS}_prop: Proporção da tag
        * {UPOS}_md: Distância média
        * count_{UPOS}: Contagem absoluta
    """

    def __init__(
        self, 
        text: str,
        lang: str = 'eng',
        text_id: str = 'text',
        conllu_path: str = 'udpipe_output',
        parser_url: str = "http://lindat.mff.cuni.cz/services/udpipe/api/process"
    ):
        self.text = text
        self.lang = lang
        self.text_id = text_id
        self.final_results = {}
        self.parser_url = parser_url
        self.conllu_path = Path(conllu_path)
        
        # Selecionar modelo baseado no idioma
        if lang == 'pt':
            self.model = 'portuguese-petrogold-ud-2.12-230717'
        else:
            self.model = 'english-gum-ud-2.12-230717'

        # Criar diretório de output se não existir
        self.conllu_path.mkdir(parents=True, exist_ok=True)
        
        # Processar texto
        self.collect_udpipe_output()

    def collect_udpipe_output(self) -> None:
        """
        Envia texto para API UDPipe e salva output CoNLL-U.
        """
        try:
            # Escapar texto para shell
            text_escaped = shlex.quote(self.text)
            
            # Montar comando curl
            command = (
                f"echo {text_escaped} | "
                f"curl -X POST -F 'data=<-' "
                f"-F model={self.model} "
                f"-F tokenizer= -F tagger= -F parser= "
                f"{self.parser_url} | "
                f"python3 -c \"import sys,json; sys.stdout.write(json.load(sys.stdin)['result'])\""
            )
            
            # Executar comando
            output = subprocess.check_output(command, shell=True, text=True)
            
            # Salvar output
            output_filename = f"{self.text_id}.conllu"
            output_file_path = self.conllu_path / output_filename
            
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(output)
            
            # Processar output
            self.process_udpipe_output(output_file_path)
            
        except subprocess.CalledProcessError as e:
            print(f"Erro ao processar texto {self.text_id}: {e}")
            # Inicializar com valores vazios
            self.sentence_tree = []

    def process_udpipe_output(self, output_file_path: Path) -> None:
        """
        Processa arquivo CoNLL-U e constrói árvore de sentenças.
        """
        sentence_tree = []
        temporary_tree = {}
        
        with open(output_file_path, "r", encoding="utf-8") as output_file:
            udpipe_file = output_file.readlines()

            for line in udpipe_file:
                line = line.strip()
                
                if line.startswith('# sent_id ='):
                    if temporary_tree:
                        sentence_tree.append(self.process_tree(temporary_tree))
                    temporary_tree = {'sent_id': line.split('=')[1].strip()}
                    
                elif line.startswith('# text ='):
                    temporary_tree['text'] = line.split('=')[1].strip()
                    
                elif line and not line.startswith('#'):
                    fields = line.split('\t')
                    if len(fields) >= 10:
                        word = {
                            'ID': fields[0],
                            'FORM': fields[1],
                            'LEMMA': fields[2],
                            'UPOS': fields[3],
                            'XPOS': fields[4],
                            'FEATS': fields[5],
                            'HEAD': fields[6],
                            'DEPREL': fields[7],
                            'DEPS': fields[8],
                            'MISC': fields[9]
                        }
                        temporary_tree.setdefault('words', []).append(word)
        
        if temporary_tree:
            sentence_tree.append(self.process_tree(temporary_tree))
        
        self.sentence_tree = sentence_tree

    def process_tree(self, tree: Dict) -> Dict:
        """
        Processa árvore de uma sentença.
        """
        return {
            "sent_id": tree.get("sent_id", ""),
            "text": tree.get("text", ""),
            "words": tree.get("words", [])
        }

    def calculate_dependency_distance(self, words: List[Dict]) -> int:
        """
        Calcula distância total de dependência para uma sentença.
        """
        sentence_total_distance = 0
        for word in words:
            if word['HEAD'].isdigit() and word['ID'].isdigit():
                distance = abs(int(word['ID']) - int(word['HEAD']))
                sentence_total_distance += distance
        return sentence_total_distance

    def mean_dependency_distance(self) -> float:
        """
        Calcula distância média de dependência para todo o texto.
        """
        sample_num_sentences = len(self.sentence_tree)
        sample_num_words = 0
        sample_total_distance = 0

        for sentence in self.sentence_tree:
            words = []
            for word in sentence['words']:
                if word['ID'].isdigit():
                    words.append(word)
            
            sentence_distance = self.calculate_dependency_distance(words)
            sample_total_distance += sentence_distance
            sample_num_words += len(words)

        if sample_num_words and sample_num_sentences:
            return sample_total_distance / (sample_num_words - sample_num_sentences)
        return 0

    def syntactic_dependencies(self, tag: str) -> tuple:
        """
        Calcula estatísticas de relações sintáticas (DEPREL ou UPOS).
        
        Returns
        -------
        tuple
            (statistics, relations_count, total_words)
            - statistics: dict com (proporção, distância_média) por relação
            - relations_count: dict com contagem por relação
            - total_words: total de palavras analisadas
        """
        relations_count = {}
        sum_distances = {}
        total_words = 0

        for sentence in self.sentence_tree:
            for word in sentence['words']:
                if not word['ID'].isdigit():
                    continue

                relation = word[tag]
                head_id = int(word['HEAD']) if word['HEAD'].isdigit() else None
                word_id = int(word['ID'])

                if head_id is None or not relation:
                    continue

                distance = abs(head_id - word_id)
                relations_count[relation] = relations_count.get(relation, 0) + 1
                sum_distances[relation] = sum_distances.get(relation, 0) + distance
                total_words += 1

        # Calcular estatísticas
        statistics = {}
        for relation, count in relations_count.items():
            proportion = count / total_words if total_words > 0 else 0
            mean_distance = sum_distances[relation] / count if count > 0 else 0
            statistics[relation] = (proportion, mean_distance)

        return statistics, relations_count, total_words

    def run(self) -> Dict[str, float]:
        """
        Executa todos os cálculos de métricas sintáticas.
        
        Returns
        -------
        dict
            Dicionário com todas as métricas calculadas
        """
        # Distância média de dependência
        mdd = self.mean_dependency_distance()
        self.final_results.update({'mean_dependency_distance': mdd})

        # Processar DEPREL e UPOS
        tags = ['DEPREL', 'UPOS']
        for tag in tags:
            statistics, relations_count, total_words = self.syntactic_dependencies(tag)
            
            # Adicionar proporção e distância média
            for key, value in statistics.items():
                self.final_results.update({
                    f'{tag}_{key}_prop': value[0],
                    f'{tag}_{key}_md': value[1]
                })
            
            # Adicionar contagens
            for key, value in relations_count.items():
                self.final_results.update({f'{tag}_count_{key}': value})
            
            # Adicionar total de palavras
            self.final_results.update({f'{tag}_total_words': total_words})

        return self.final_results


if __name__ == "__main__":
    # Teste simples
    text_example = (
        "The wind blew a steady gale, and the snow swirled and eddied around "
        "the house. Inside, the fire crackled warmly."
    )
    
    print("Testing SyntacticMetrics...")
    metrics = SyntacticMetrics(text_example, lang='eng', text_id='test')
    results = metrics.run()
    
    print(f"\nCalculated {len(results)} metrics")
    print("\nSample metrics:")
    for key in list(results.keys())[:10]:
        print(f"  {key}: {results[key]}")
