"""
    Script responsável pela criação da janela principal, especificamente:
        * Área do vídeo,
        * Botões básicos,
        * Lista de classes.
    Utilização do framework Qt para a estrturação da UI
"""
import sys

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QFileDialog,
    QDialog,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QLabel,
    QSlider,
    QInputDialog,
    QMenu,
    QCheckBox
)
from PySide6.QtCore import Qt, QTimer, QSize

# Importação dos demais módulos (scripts) do projeto
from ..ui.Video_Widget import VideoWidget
from ..services.Video_Manager import VideoManager
from ..storage.Dataset_Manager import DatasetManager
from ..controllers.App_Controller import convert_cv_to_qt


# QDialog modal logo no início da aplicação.
# Ele aparece antes da janela principal e obriga o usuário a escolher uma opção antes de continuar.
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

    def open_existing(self):
        self.choice = "open"
        self.accept()

    def create_new(self):
        self.choice = "new"
        self.accept()


# QMainWindow é a classe base do framework Qt para criar a janela principal do aplicativo.
# Neste caso, MainWindow herda diretamente os parâmetros de QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicialização dos elementos
        self.lock_roi_checkbox = None
        self.manage_dataset = None
        self.open_dataset_button = None
        self.add_class_button = None
        self.current_frame = None
        self.save_button = None
        self.next_button = None
        self.prev_button = None
        self.pause_button = None
        self.play_button = None
        self.open_button = None
        self.video_widget = None
        self.class_list = None
        self.timeline_slider = None
        self.frame_label = None
        self.timeline_layout = None

        # Parâmetros PADRÕES do constrututor para criação da janela principal
        self.setWindowTitle("Dataset Annotation Tool")
        self.resize(1200, 800)
        self.video_manager = VideoManager()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_playback_frame)
        self.classes = []
        self.setup_ui()

        # Cria janela inicial para seleção de uma base pré-existente ou para criação de uma nova base
        while True:

            dialog = StartupDialog()
            if not dialog.exec():
                sys.exit()

            if dialog.choice == "open":
                # Abre uma nova janela para que o usuário possa selecionar o diretório da base de dados
                self.dataset_manager = DatasetManager()
                self.open_dataset()
                break

            elif dialog.choice == "new":
                # Abre uma nova janela de diálogo, perguntando ao usuário o nome da nova base de dados
                base_name, ok = QInputDialog.getText(
                    self,
                    "Novo Dataset",
                    "Nome da base:"
                )

                # Caso o input seja inválido ou cancelado, retorna para a Janela principal
                if not ok or not base_name:
                    continue

                # cria a base
                self.dataset_manager = DatasetManager(base_name)
                self.dataset_manager.create_dataset_structure(self.classes)
                break

    # =================================================================
    #            DEFINIÇÃO E ORGANIZAÇÃO DOS ELEMENTOS DE U.I
    # =================================================================
    def setup_ui(self):

        # Widget central do UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # main_layout -> Área principal dividida horizontalmente para alocar os widgets principais
        main_layout = QHBoxLayout()
        # left_layout -> Área secundária dividida verticalmente para alocar widgets secundários
        left_layout = QVBoxLayout()
        # video_layout -> Área secundária dividida verticalmente para alocar a exibição do vídeo
        video_layout = QVBoxLayout()
        # controls_layout -> Área secundária dividida horizontalmente para os controles do vídeo
        controls_layout = QHBoxLayout()
        # functions_layout -> Área secundária dividida verticalmente para os controles gerais
        functions_layout = QHBoxLayout()

        # Criação de uma Label para indicar as classes
        class_label = QLabel("Classes")
        # Criação de uma Label para indicar os controles de vídeo
        controls_label = QLabel("Controles de vídeo")
        # Criação de uma Label para indicar os controles especiais
        functions_label = QLabel("Funcionalidade especiais")

        # Criação de um Widget de lista responsável por exibir as classes descritas no construtor
        self.class_list = QListWidget()
        self.class_list.addItems(self.classes)
        self.class_list.setCurrentRow(0)

        # Criação do QSlider para implemetação da barra de rolagem do vídeo
        # Inicialização dos valores iniciais para a rolagem
        self.timeline_slider = QSlider(Qt.Horizontal)
        self.timeline_slider.setMinimum(0)
        self.timeline_slider.setMaximum(0)
        self.frame_label = QLabel("00:00")

        # Layout para agregar os elementos do Slider
        self.timeline_layout = QHBoxLayout()
        self.timeline_layout.addWidget(self.timeline_slider)
        self.timeline_layout.addWidget(self.frame_label)

        # Criação dos botões de controle
        self.manage_dataset = QPushButton("Manage Dataset")
        self.open_button = QPushButton("Open Video")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.prev_button = QPushButton("<<")
        self.next_button = QPushButton(">>")
        self.save_button = QPushButton("Save ROI")
        self.lock_roi_checkbox = QCheckBox("Lock ROI")
        self.add_class_button = QPushButton("Add Class")
        self.open_dataset_button = QPushButton("Open Dataset")

        # Criação de um menu de contexto para as classes da barra lateral esquerda
        # O menu é acessado com o clique direito do mouse sobre a classe
        self.class_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.class_list.customContextMenuRequested.connect(self.show_class_menu)

        # Inserção dos botões no controls_layout
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.next_button)

        # Inserção dos botões no functions_layout
        functions_layout.addWidget(self.open_button)
        functions_layout.addWidget(self.save_button)
        functions_layout.addWidget(self.lock_roi_checkbox)

        # Inserção da Label e Lista de classes no left_layout
        left_layout.addWidget(class_label)
        left_layout.addWidget(self.class_list)

        # Inserção dos botões criados no left_layout
        left_layout.addWidget(self.add_class_button)
        left_layout.addWidget(self.open_dataset_button)
        left_layout.addWidget(self.manage_dataset)

        # Criação do Widget responsável pela reprodução do Vídeo
        self.video_widget = VideoWidget()
        # Entrega de uma referência do CheckBox para o VideoWidget.
        # ALTERAR REFERENCIA NO FUTURO
        self.video_widget.lock_roi_checkbox = self.lock_roi_checkbox

        # Inserção do widget de vídeo no video_layout
        video_layout.addWidget(self.video_widget)
        # Inserção do widget de slider no video_layout
        video_layout.addLayout(self.timeline_layout)

        # Inserção do controls_layout e sua respectiva label no video_layout
        video_layout.addWidget(controls_label)
        video_layout.addLayout(controls_layout)
        # Inserção do functions_layout e sua respectiva label no video_layout
        video_layout.addWidget(functions_label)
        video_layout.addLayout(functions_layout)

        # OBS: video_layout contém tanto o widget de vídeo quanto todos
        # os componentes de controle definidos no controls_layout

        # Inserção dos layouts secundários left_layout e video_layout
        # no main_layout (Gera uma estrutura hierárquica de layouts)
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(video_layout, 4)

        # Define o main_layout como Layout do Widget central da aplicaçao
        central_widget.setLayout(main_layout)
        # Chama a função responsável por conectar cada botão à uma função do script
        self.connect_signals()

    # =================================================================
    #             CONEXÃO DOS ELEMENTOS DE U.I AOS MÉTODOS
    # =================================================================
    def connect_signals(self):

        # Conexão dos botões à suas respectivas funções
        self.open_button.clicked.connect(self.open_video)
        self.play_button.clicked.connect(self.start_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.prev_button.clicked.connect(self.previous_frame)
        self.next_button.clicked.connect(self.next_frame)
        self.save_button.clicked.connect(self.save_roi)
        self.add_class_button.clicked.connect(self.add_class)
        self.open_dataset_button.clicked.connect(self.open_dataset)
        # Pausa o video ao 'pressionar' o slider
        self.timeline_slider.sliderPressed.connect(self.pause_video)
        # Função chamada ao 'soltar' o slider em dada posição
        self.timeline_slider.sliderReleased.connect(self.slider_released)

        # self.manage_dataset.clicked.connect()

    # =================================================================
    #           CARREGAMENTO DE DATASET PRÉ-EXISTENTE
    # =================================================================
    def open_dataset(self):

        # Abre uma nova Janela destinada à seleção do diretório da base de dados
        dataset_path = QFileDialog.getExistingDirectory(self, "Selecionar Dataset")
        if not dataset_path:
            return

        # Obtém a lista de classes existentes no diretório indicado
        classes = (self.dataset_manager.load_dataset(dataset_path))
        # Limpa a 'class_list' na área lateral à esquerda
        if self.class_list is not None:
            self.class_list.clear()
        # Adiciona as classes obtidas no carregamento da base na área lateral
        self.class_list.addItems(classes)
        # Redefine as classes
        self.classes = classes

    # =================================================================
    #           GERENCIAMENTO DAS CLASSES (ÁREA À ESQUERDA)
    # =================================================================

    def add_class(self):  # >>>>>>>>>>>>> ADICIONAR NOVA CLASSE AO DATASET

        # Abre uma nova janela de diálogo, perguntando ao usuário o nome que a nova classe deve ter
        # Em sequência é validado se uma string válida foi digitada
        class_name, ok = QInputDialog.getText(self, "Nova Classe", "Nome da classe:")
        if not ok:
            return
        # Remove potenciais espaços em branco do texto digitado
        # Valida se a String restante permanece válida
        class_name = class_name.strip()
        if not class_name:
            return

        # Chama a função responsável por criar a nova classe no dataset
        self.dataset_manager.create_class(class_name)
        # Incrementa o nome da classe na lista QWidgetList
        self.class_list.addItem(class_name)

    def show_class_menu(self, position):  # >>>>>>>>>>>>> DEFINIÇÃO DO MENU DE CONTEXO PARA CADA CLASSE

        # Exibe o menu para a classe indicada pela posição
        # A posição é extraída automaticamente de class_list,
        # de acordo com o item selecionado ao pressionar o clique direito do mouse
        item = self.class_list.itemAt(position)
        if item is None:
            return

        # Instância de um QMenu e seus itens
        menu = QMenu()
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")

        # Recebe qual dos itens no menu foram selecionados
        # Chamando suas respectivas funções em sequência
        action = menu.exec(self.class_list.mapToGlobal(position))
        if action == rename_action:
            self.rename_class(item)
        elif action == delete_action:
            self.delete_class(item)

    def rename_class(self, item):  # >>>>>>>>>>>>> RENOMEAR CLASSE (DENTRO DO MENU DE CONTEXTO)

        # Obtém o nome original do item, para permitir a edição do nome original
        # Caso contrário, ao chamar a função, o nome original seria apagado diretamente
        old_name = item.text()
        # Abre uma nova janela de diálogo, perguntando ao usuário o novo nome que da classe selecionada
        new_name, ok = (QInputDialog.getText(self, "Renomear Classe", "Novo nome:", text=old_name))
        if not ok:
            return

        # Remove potenciais espaços em branco do texto digitado
        # Valida se a String restante permanece válida
        new_name = new_name.strip()
        if not new_name:
            return

        # Chama a função responsável por alterar o nome no diretório do dataset
        self.dataset_manager.rename_class(
            old_name,
            new_name
        )
        # Altera o valor do nome para o respectivo item da lista
        item.setText(new_name)

    def delete_class(self, item):  # >>>>>>>>>>>>> DELETAR CLASSE (DENTRO DO MENU DE CONTEXTO)

        # Obtém o nome original do item
        class_name = item.text()
        # Abre uma nova Janela solicitando a confirmação de exclusão
        response = QMessageBox.question(self, "Excluir Classe",
                                        f"Excluir '{class_name}' e todos os seus itens internos ?",
                                        QMessageBox.Yes | QMessageBox.No)
        # Valida a resposta da Janela 'response'
        if response != QMessageBox.Yes:
            return
        # Chama a função responsável por deletar a classe no diretório do dataset
        self.dataset_manager.delete_class(class_name)
        # Remove o item da lista de classes
        row = self.class_list.row(item)
        self.class_list.takeItem(row)

    # =================================================================
    #                    CONTROLADORES DO SLIDER
    # =================================================================
    def slider_released(self):
        # Define o frame com base na posição do slider e atualiza a reprodução
        frame_number = self.timeline_slider.value()
        self.video_manager.seek(frame_number)
        self.update_frame()
        self.start_video()

    # =================================================================
    #                ATUALIZAÇÃO DO TEMPO DE VÍDEO
    # =================================================================
    def update_timeline(self):

        # 'blockSignals' impede termporariamente que um Widget emita sinais.
        # Esse comando evita que a atualização de valores ocorra de forma
        # segura, sem gerar loops inconsistentes
        self.timeline_slider.blockSignals(True)
        self.timeline_slider.setValue(self.video_manager.current_frame)
        self.timeline_slider.blockSignals(False)

        # Atualiza a Label do slider sempre que um novo frame for exibido
        current_time = (self.video_manager.current_frame / self.video_manager.fps)
        total_time = (self.video_manager.total_frames / self.video_manager.fps)
        current_video_time = VideoManager.format_time(current_time)
        total_video_time = VideoManager.format_time(total_time)
        self.frame_label.setText(f"{current_video_time} / {total_video_time}")

    # =================================================================
    #              CARREGAMENTO DO ARQUIVO DE VÍDEO
    # =================================================================
    def open_video(self):

        # Função responsável por selecionar o arquivo de vídeo e limitar as extensões aceitas
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            "Videos (*.mp4 *.avi *.mov)"
        )
        # Chama a função para carregamento do arquivo no caminho indicado
        if path:
            self.video_manager.load_video(path)
            # Ao abrir o vídeo, o slider atualiza seu valor máximo com base no total de frames
            self.timeline_slider.setMaximum(self.video_manager.total_frames - 1)
        # Atualiza a exibição
        self.update_frame()
        self.start_video()

    # =================================================================
    #                 RENDERIZAÇÃO DO FRAME NA JANELA
    # =================================================================
    def display_frame(self, frame):
        if frame is None:
            return

        # Define o frame atual como uma cópia do frame carregado
        # A cópia evita corrupções no frame original extraído
        self.current_frame = frame.copy()
        # Converte o frame para um formato compatível com Qt, no caso, um pixmap
        pixmap = convert_cv_to_qt(frame)
        # O frame é redimensionado de acordo com o tamanho de video_widget.
        scaled = pixmap.scaled(
            self.video_widget.size(),
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )

        # Instncia o objeto de informações referentes à coordenadas
        info = self.video_widget.display_info

        # Armazenar o tamanho do frame original
        h, w = frame.shape[:2]
        info.frame_width = w
        info.frame_height = h

        # Armazenar dimensões reais renderizadas
        info.display_width = scaled.width()
        info.display_height = scaled.height()

        # Armazenar valores do offset para identificar onde a imagem está, dentro do widget.
        info.offset_x = (self.video_widget.width() - scaled.width()) / 2
        info.offset_y = (self.video_widget.height() - scaled.height()) / 2

        # Chamada da função para exibir o Pixmap
        self.video_widget.setPixmap(scaled)
        # Chamada da função para atualizar o tempo de vídeo
        self.update_timeline()

    # =================================================================
    #                     CAPTURA MANUAL DO FRAME
    # =================================================================
    def update_frame(self):
        frame = self.video_manager.get_frame_by_position()
        self.display_frame(frame)

    # =================================================================
    #                  REPRODUÇÃO CONTÍNUA DE FRAMES
    # =================================================================
    def update_playback_frame(self):
        frame = self.video_manager.read_next_frame()
        if frame is None:
            self.timer.stop()
            return

        self.display_frame(frame)
        self.update_timeline()

    # =================================================================
    #                  FUNÇÕES DE CONTROLE MANUAL
    #         Utiliza operações definidas no Script Video_Manager,
    #           contida no pacote SERVICES (Lógica operacional)
    # =================================================================
    def start_video(self):
        interval = int(1000 / max(1, self.video_manager.fps))
        self.timer.start(interval)

    def pause_video(self):
        if self.timer.isActive():
            self.timer.stop()

    def next_frame(self):
        self.pause_video()
        self.video_manager.next_frame()
        self.update_frame()
        self.update_timeline()

    def previous_frame(self):
        self.pause_video()
        self.video_manager.previous_frame()
        self.update_frame()
        self.update_timeline()

    # =================================================================
    #                       ARMAZENAMENTO DA ROI
    # =================================================================
    def save_roi(self):
        if self.video_widget.roi is None:
            QMessageBox.warning(self, "Erro", "Nenhuma ROI selecionada")
            return

        selected_item = self.class_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(self, "Erro", "Nenhuma classe selecionada")
            return
        class_name = selected_item.text()
        self.dataset_manager.save_roi(
            self.current_frame,
            self.video_widget.roi,
            class_name
        )
        QMessageBox.information(self, "Sucesso", "ROI salva com sucesso")
