"""
    Script da Janela de Login
    * Responsável apenas por receber os dados
      do usuário e validar seu papel na ferramenta
"""
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)


class LoginDialog(QDialog):

    def __init__(self, user_controller):
        super().__init__()

        # Recebe o user_controller como parâmetro
        self.controller = user_controller

        # Definição das dimensões e nome da Janela
        self.setWindowTitle("Login")
        self.setFixedSize(300, 180)

        # Definição do Layout principal (Vertical)
        layout = QVBoxLayout()

        # Adição da label de Username e área de inserção de texto
        layout.addWidget(QLabel("Username"))
        self.username = QLineEdit()
        layout.addWidget(self.username)

        # Adição da label de Password e área de inserção de texto
        # setEchoMode(QLineEdit.Password) esconde os caracteres digitados
        layout.addWidget(QLabel("Password"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        # Criação e conexão do botão de Login à respectiva função
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        self.setLayout(layout)

    def login(self):

        # Retorno verdadeiro, caso a função de Login no controller consiga validar os dados
        # Os dados de entrada são passados como parâmetro para o controller
        success = self.controller.login(self.username.text(), self.password.text())

        if success:
            self.accept()

        else:
            QMessageBox.warning(self, "Login", "Invalid username or password.")
