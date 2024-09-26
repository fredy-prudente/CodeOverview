# CodeOverview/logic/processador.py

import os
from PyQt5.QtWidgets import QMessageBox

class ProcessadorEstrutura:
    def processar_projeto(self, diretorio, extensoes):
        """
        Percorre o diretório, coleta os arquivos com as extensões especificadas,
        e gera uma estrutura de texto.

        :param diretorio: Diretório do projeto
        :param extensoes: Lista de extensões de arquivo a incluir
        :return: Tuple (estrutura_texto, lista_de_erros)
        """
        estrutura = ""
        erros = []
        try:
            for raiz, dirs, arquivos in os.walk(diretorio):
                for arquivo in arquivos:
                    _, ext = os.path.splitext(arquivo)
                    if ext.lower() in extensoes:
                        caminho_completo = os.path.join(raiz, arquivo)
                        caminho_relativo = os.path.relpath(caminho_completo, diretorio)
                        estrutura += f"{caminho_relativo}:\n\n"
                        try:
                            with open(caminho_completo, 'r', encoding='utf-8') as f:
                                conteudo = f.read()
                        except UnicodeDecodeError:
                            conteudo = "# Não foi possível decodificar o arquivo."
                            erros.append(f"Erro de decodificação: {caminho_relativo}")
                        except Exception as e:
                            conteudo = f"# Erro ao ler o arquivo: {str(e)}"
                            erros.append(f"Erro ao ler {caminho_relativo}: {str(e)}")
                        estrutura += conteudo + "\n\n"
            return estrutura, erros
        except Exception as e:
            # Erro crítico, não conseguiu percorrer o diretório
            raise e

    def salvar_estrutura(self, caminho_arquivo, estrutura):
        """
        Salva a estrutura gerada em um arquivo de texto.

        :param caminho_arquivo: Caminho completo do arquivo de saída
        :param estrutura: Texto da estrutura do projeto
        """
        with open(caminho_arquivo, 'w', encoding='utf-8') as out_file:
            out_file.write(estrutura)

    def copiar_para_clipboard(self, estrutura):
        """
        Copia a estrutura para a área de transferência.

        :param estrutura: Texto da estrutura do projeto
        """
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(estrutura)
