import sys
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QInputDialog
)

from Application.controllers.application_controller import ApplicationController
from Application.ui.main_window import MainWindow
from Application.ui.startup_dialog import StartupDialog, StartupChoice


def main():

    # Cria a instância principal do aplicativo em PyQt
    classes = []
    app = QApplication(sys.argv)

    # Cria a instância principal do controlador
    controller = ApplicationController()

    # Loop que apresenta a tela inicial até que seja feita
    # um escolha entre um dataset novo ou pré-existente para iniciar
    while True:

        # Executa a Janela
        dialog = StartupDialog()
        if not dialog.exec():
            sys.exit()

        # Operação para iniciar um dataset existente
        if dialog.choice == StartupChoice.OPEN:

            # Obtém o caminho e as classes presentes na base selecionada
            dataset_path = QFileDialog.getExistingDirectory(None, "Selecionar Dataset")
            if not dataset_path:
                continue

            classes = controller.dataset.open_dataset(dataset_path)
            break

        # Operação para iniciar um novo dataset
        elif dialog.choice == StartupChoice.NEW:

            # Pede ao usuário um nome para a base a ser contruída
            base_name, ok = QInputDialog.getText(
                None,
                "Novo Dataset",
                "Nome da base:"
            )

            if not ok or not base_name:
                continue

            # Cria o diretório de trabalho e inicializa sem classes
            controller.dataset.create_dataset(base_name)
            classes = []
            break

    # Apresenta a tela inicial
    window = MainWindow(controller, classes)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
