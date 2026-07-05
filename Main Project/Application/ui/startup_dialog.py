import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from enum import Enum, auto


# ----------------------------------------------------------------------------------------------------------------------
# Enumeração (Enum) é uma estrutura usada para agrupar um conjunto de constantes
# com nomes simbólicos e valores exclusivos.
# ----------------------------------------------------------------------------------------------------------------------
# A função auto() do módulo enum atribui automaticamente um valor numérico sequencial único a esta constante.
# Em Python, ele geralmente começa em 1 .
# ----------------------------------------------------------------------------------------------------------------------
class StartupChoice(Enum):
    OPEN = auto()
    NEW = auto()


# QDialog modal que será apresentada antes da execução da janela principal
class StartupDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.choice = None
        self.setFixedWidth(400)
        self.setFixedHeight(250)
        self.setWindowTitle("Inicialização")

        # Criação de um Layout básico para alocar os botões
        layout = QVBoxLayout()

        # Definição dos botões
        btn_open = QPushButton("Open pre-existing Database")
        btn_open.setMinimumWidth(150)
        btn_open.setMinimumHeight(50)
        btn_new = QPushButton("Startup with new Database")
        btn_new.setMinimumWidth(150)
        btn_new.setMinimumHeight(50)
        btn_exit = QPushButton("Exit")
        btn_exit.setMinimumWidth(150)
        btn_exit.setMinimumHeight(50)

        # Conexão dos botões às suas respectivas funções
        btn_open.clicked.connect(self.open_existing)
        btn_new.clicked.connect(self.create_new)
        btn_exit.clicked.connect(sys.exit)

        # Adição dos botões ao layout criado para esta Janela
        layout.addWidget(btn_open)
        layout.addWidget(btn_new)
        layout.addSpacing(50)
        layout.addWidget(btn_exit)
        self.setLayout(layout)

    # Define a escolha de acordo com o botão selecionado
    # A função accept() retorna a resposta da escolha para Main.py
    def open_existing(self):
        self.choice = StartupChoice.OPEN
        self.accept()

    def create_new(self):
        self.choice = StartupChoice.NEW
        self.accept()
