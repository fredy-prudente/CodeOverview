from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QPushButton,
    QFileDialog, QMessageBox, QCheckBox, QVBoxLayout, QHBoxLayout, QGroupBox
)
from CodeOverview.logic.processador import ProcessadorEstrutura
import os
import sys

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funciona para desenvolvimento e para PyInstaller."""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeOverview - Gerador de Estrutura de Projeto")
        self.setGeometry(100, 100, 700, 550)
        self.processador = ProcessadorEstrutura()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Definir o ícone da janela
        icon_path = resource_path(os.path.join(os.path.dirname(__file__), '..', 'resources', 'icons', 'icon.ico'))
        self.setWindowIcon(QIcon(icon_path))

        # Diretório do Projeto
        grupo_diretorio = QGroupBox("Diretório do Projeto")
        layout_diretorio = QHBoxLayout()

        self.entrada_diretorio = QLineEdit()
        self.botao_diretorio = QPushButton("Selecionar")
        self.botao_diretorio.clicked.connect(self.selecionar_diretorio)

        layout_diretorio.addWidget(self.entrada_diretorio)
        layout_diretorio.addWidget(self.botao_diretorio)
        grupo_diretorio.setLayout(layout_diretorio)
        layout.addWidget(grupo_diretorio)

        # Arquivo de Saída (Opcional)
        grupo_saida = QGroupBox("Arquivo de Saída (Opcional)")
        layout_saida = QHBoxLayout()

        self.entrada_saida = QLineEdit()
        self.botao_saida = QPushButton("Selecionar")
        self.botao_saida.clicked.connect(self.selecionar_arquivo_saida)

        layout_saida.addWidget(self.entrada_saida)
        layout_saida.addWidget(self.botao_saida)
        grupo_saida.setLayout(layout_saida)
        layout.addWidget(grupo_saida)

        # Tipos de Arquivo
        grupo_tipos = QGroupBox("Tipos de Arquivo a Incluir")
        layout_tipos = QHBoxLayout()

        self.check_py = QCheckBox(".py")
        self.check_py.setChecked(True)
        self.check_json = QCheckBox(".json")
        self.check_html = QCheckBox(".html")
        self.check_css = QCheckBox(".css")
        self.check_js = QCheckBox(".js")
        self.check_outros = QCheckBox("Outros")
        self.entrada_outros = QLineEdit()
        self.entrada_outros.setPlaceholderText("Ex: .txt, .md")
        self.entrada_outros.setEnabled(False)

        self.check_outros.stateChanged.connect(self.toggle_entrada_outros)

        layout_tipos.addWidget(self.check_py)
        layout_tipos.addWidget(self.check_json)
        layout_tipos.addWidget(self.check_html)
        layout_tipos.addWidget(self.check_css)
        layout_tipos.addWidget(self.check_js)
        layout_tipos.addWidget(self.check_outros)
        layout_tipos.addWidget(self.entrada_outros)
        grupo_tipos.setLayout(layout_tipos)
        layout.addWidget(grupo_tipos)

        # Ações
        grupo_acoes = QGroupBox("Ações")
        layout_acoes = QHBoxLayout()

        self.botao_processar_salvar = QPushButton("Gerar e Salvar")
        self.botao_processar_salvar.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.botao_processar_salvar.clicked.connect(self.processar_e_salvar)

        self.botao_processar_copiar = QPushButton("Copiar para Clipboard")
        self.botao_processar_copiar.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px;")
        self.botao_processar_copiar.clicked.connect(self.processar_e_copiar)

        # Checkbox para Ignorar Mensagem de Confirmação
        self.checkbox_sem_mensagem = QCheckBox("Não exibir mensagem de confirmação")
        layout_acoes.addWidget(self.botao_processar_salvar)
        layout_acoes.addWidget(self.botao_processar_copiar)
        layout_acoes.addWidget(self.checkbox_sem_mensagem)
        grupo_acoes.setLayout(layout_acoes)
        layout.addWidget(grupo_acoes)

        # Área de Log
        grupo_log = QGroupBox("Log de Processamento")
        layout_log = QVBoxLayout()

        self.area_log = QtWidgets.QTextEdit()
        self.area_log.setReadOnly(True)
        layout_log.addWidget(self.area_log)

        grupo_log.setLayout(layout_log)
        layout.addWidget(grupo_log)

        self.setLayout(layout)

    def toggle_entrada_outros(self, state):
        self.entrada_outros.setEnabled(state == QtCore.Qt.Checked)
        if not self.entrada_outros.isEnabled():
            self.entrada_outros.clear()

    def selecionar_diretorio(self):
        diretorio = QFileDialog.getExistingDirectory(self, "Selecionar Diretório do Projeto")
        if diretorio:
            self.entrada_diretorio.setText(diretorio)

    def selecionar_arquivo_saida(self):
        arquivo, _ = QFileDialog.getSaveFileName(self, "Selecionar Arquivo de Saída", "", "Text Files (*.txt);;All Files (*)")
        if arquivo:
            self.entrada_saida.setText(arquivo)

    def obter_extensoes_selecionadas(self):
        extensoes = []
        if self.check_py.isChecked():
            extensoes.append('.py')
        if self.check_json.isChecked():
            extensoes.append('.json')
        if self.check_html.isChecked():
            extensoes.append('.html')
        if self.check_css.isChecked():
            extensoes.append('.css')
        if self.check_js.isChecked():
            extensoes.append('.js')
        if self.check_outros.isChecked():
            outros = self.entrada_outros.text()
            if outros:
                outros_ext = [ext.strip().lower() if ext.strip().startswith('.') else '.' + ext.strip().lower() for ext in outros.split(',')]
                extensoes.extend(outros_ext)
        return extensoes

    def gerar_estrutura(self):
        diretorio = self.entrada_diretorio.text().strip()
        extensoes = self.obter_extensoes_selecionadas()
        estrutura, erros = self.processador.processar_projeto(diretorio, extensoes)
        return estrutura, erros

    def processar_e_salvar(self):
        diretorio = self.entrada_diretorio.text().strip()
        arquivo_saida = self.entrada_saida.text().strip()

        # Validações
        if not diretorio:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione o diretório do projeto.")
            return
        if not arquivo_saida:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione o local e o nome do arquivo de saída.")
            return
        extensoes = self.obter_extensoes_selecionadas()
        if not extensoes:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione pelo menos um tipo de arquivo.")
            return

        self.log("Iniciando o processo de geração e salvamento...")

        estrutura, erros = self.gerar_estrutura()
        if estrutura is None:
            self.log("Processamento interrompido devido a um erro crítico.")
            return

        try:
            self.processador.salvar_estrutura(arquivo_saida, estrutura)
            QMessageBox.information(self, "Sucesso", f"Arquivo gerado em: {arquivo_saida}")
            self.log(f"Arquivo salvo em: {arquivo_saida}")
            if erros:
                self.log("Erros encontrados durante o processamento:")
                for erro in erros:
                    self.log(erro)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível salvar o arquivo: {str(e)}")
            self.log(f"Erro ao salvar o arquivo: {str(e)}")

    def processar_e_copiar(self):
        mostrar_mensagem = not self.checkbox_sem_mensagem.isChecked()

        diretorio = self.entrada_diretorio.text().strip()
        extensoes = self.obter_extensoes_selecionadas()

        # Validações
        if not diretorio:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione o diretório do projeto.")
            return
        if not extensoes:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione pelo menos um tipo de arquivo.")
            return

        self.log("Iniciando o processo de cópia para o clipboard...")

        estrutura, erros = self.gerar_estrutura()
        if estrutura is None:
            self.log("Processamento interrompido devido a um erro crítico.")
            return

        try:
            self.processador.copiar_para_clipboard(estrutura)
            if mostrar_mensagem:
                QMessageBox.information(self, "Sucesso", "A estrutura do projeto foi copiada para a área de transferência.")
            self.log("Estrutura copiada para o clipboard.")
            if erros:
                self.log("Erros encontrados durante o processamento:")
                for erro in erros:
                    self.log(erro)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível copiar para o clipboard: {str(e)}")
            self.log(f"Erro ao copiar para o clipboard: {str(e)}")

    def log(self, mensagem):
        self.area_log.append(mensagem)
        self.area_log.moveCursor(QtGui.QTextCursor.End)
