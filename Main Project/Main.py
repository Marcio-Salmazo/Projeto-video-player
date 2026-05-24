"""
    Script orquestrador, responsável pela execução direta da ferramenta,
    unindo e integrando os demais módulos do sistema
"""

import sys
from PySide6.QtWidgets import QApplication
from Application.ui.Main_Window import MainWindow

if __name__ == "__main__":

    # QApplication é a classe que gerencia os recursos da sua aplicação gráfica.
    # sys.argv é uma lista padrão do Python que captura os argumentos passados via terminal.
    app = QApplication(sys.argv)

    # Exibição da Janela principal definida em UI/Main_Window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
