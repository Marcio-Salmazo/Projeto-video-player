from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)


class LoginDialog(QDialog):

    def __init__(self, controller):

        super().__init__()

        self.controller = controller

        self.setWindowTitle("Login")
        self.setFixedSize(300, 180)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username"))

        self.username = QLineEdit()

        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password"))

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.password)

        login_button = QPushButton("Login")

        login_button.clicked.connect(self.login)

        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):

        success = self.controller.login(
            self.username.text(),
            self.password.text()
        )

        if success:

            self.accept()

        else:

            QMessageBox.warning(
                self,
                "Login",
                "Invalid username or password."
            )