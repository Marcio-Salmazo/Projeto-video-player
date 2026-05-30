"""
    Script responsável pela criação da janela principal, especificamente:
        * Área do vídeo,
        * Botões básicos,
        * Lista de classes.
    Utilização do framework Qt para a estrturação da UI
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QFileDialog,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QLabel
)
from PySide6.QtCore import Qt, QTimer

# Importação dos demais módulos (scripts) do projeto
from ..ui.Video_Widget import VideoWidget
from ..services.Video_Manager import VideoManager
from ..storage.Dataset_Manager import DatasetManager
from ..controllers.App_Controller import convert_cv_to_qt


# QMainWindow é a classe base do framework Qt para criar a janela principal do aplicativo.
# Neste caso, MainWindow herda diretamente os parâmetros de QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicialização dos elementos
        self.current_frame = None
        self.save_button = None
        self.next_button = None
        self.prev_button = None
        self.pause_button = None
        self.play_button = None
        self.open_button = None
        self.video_widget = None
        self.class_list = None

        # Parâmetros PADRÕES do constrututor para criação da janela principal
        self.setWindowTitle("Dataset Annotation Tool")
        self.resize(1200, 800)
        self.video_manager = VideoManager()
        self.dataset_manager = DatasetManager()
        # self.controller = AppController(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_playback_frame)
        self.classes = [
            "pain",
            "no_pain",
            "sleeping"
        ]
        self.dataset_manager.create_dataset_structure(self.classes)
        self.setup_ui()

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

        # Criação de uma Label para indicar as classes
        class_label = QLabel("Classes")

        # Criação de um Widget de lista responsável por exibir as classes descritas no construtor
        self.class_list = QListWidget()
        self.class_list.addItems(self.classes)
        self.class_list.setCurrentRow(0)

        # Inserção da Label e Lista de classes no left_layout
        left_layout.addWidget(class_label)
        left_layout.addWidget(self.class_list)

        # Criação dos botões de controle
        self.open_button = QPushButton("Open Video")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.prev_button = QPushButton("<<")
        self.next_button = QPushButton(">>")
        self.save_button = QPushButton("Save ROI")

        # Inserção dos botões criados no controls_layout
        controls_layout.addWidget(self.open_button)
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.save_button)

        # Criação do Widget responsável pela reprodução do Vídeo
        self.video_widget = VideoWidget()

        # Inserção do widget de vídeo no video_layout
        video_layout.addWidget(self.video_widget)
        # Inserção do controls_layout no video_layout
        video_layout.addLayout(controls_layout)
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
        # Atualiza a exibição
        self.update_frame()

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

    # =================================================================
    #                  FUNÇÕES DE CONTROLE MANUAL
    #         Utiliza operações definidas no Script Video_Manager,
    #           contida no pacote SERVICES (Lógica operacional)
    # =================================================================
    def start_video(self):
        interval = int(1000 / max(1, self.video_manager.fps))
        self.timer.start(interval)

    def pause_video(self):
        self.timer.stop()

    def next_frame(self):
        self.video_manager.next_frame()
        self.update_frame()

    def previous_frame(self):
        self.video_manager.previous_frame()
        self.update_frame()

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
