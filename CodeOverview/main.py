# CodeOverview/main.py

import sys
from PyQt5.QtWidgets import QApplication
from CodeOverview.ui.main_window import MainWindow
from PyQt5.QtGui import QIcon
import os

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funciona para desenvolvimento e para PyInstaller."""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def run_app():
    app = QApplication(sys.argv)
    
    # Definir o ícone da aplicação
    icon_path = resource_path(os.path.join('CodeOverview', 'resources', 'icons', 'icon.ico'))
    app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
