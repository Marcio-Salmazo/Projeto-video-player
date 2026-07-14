"""
    Script da View
    * Responsável apenas por montar a janela principal
      Obter os comandos do usuário e devolver informações
      processadas pelos demais módulos do sistema.

"""

import os

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QFileDialog,
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
from PySide6.QtCore import Qt, QTimer
from Main_Project.Application.services.conversion_services import ConversionServices


# QMainWindow é a classe base do framework Qt para criar a janela principal do aplicativo.
# Neste caso, MainWindow herda diretamente os parâmetros de QMainWindow
class MainWindow(QMainWindow):
    def __init__(self, user_controller, video_controller, data_controller, classes):
        super().__init__()

        # Inicialização dos elementos da janela
        self.lock_roi_checkbox = None
        self.manage_dataset_button = None
        self.open_dataset_button = None
        self.add_class_button = None
        self.save_button = None
        self.dataset_label = None
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

        # Recebe a referência da instância do controller da aplicação (ApplicationController)
        # e as classes à serem exibidas na aba lateral (Caso uma base pré-existente tenha sido selecionada)
        self.video_controller = video_controller
        self.data_controller = data_controller
        self.classes = classes

        # Parâmetros PADRÕES para criação da janela principal
        self.setWindowTitle("Dataset Annotation Tool")
        self.resize(1200, 800)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_playback_frame)
        self.setup_ui()

    # ------------------------------------------------------------------------------------------------------------------
    #               Função responsável por definir e organizar os elementos da interface gráfica
    # ------------------------------------------------------------------------------------------------------------------
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

        # Criação de uma Label para indicar a área das classes
        class_label = QLabel("Classes")
        # Criação de uma Label para indicar os controles de vídeo
        controls_label = QLabel("Controles de vídeo")
        # Criação de uma Label para indicar os controles especiais
        functions_label = QLabel("Funcionalidade especiais")
        # Criação de uma Label para preencher inicialmente a área das classes
        self.dataset_label = QLabel("No Dataset Loaded")

        # Criação de um Widget de lista responsável
        # por exibir as classes descritas no construtor
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
        self.manage_dataset_button = QPushButton("Manage Dataset")
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
        left_layout.addWidget(self.dataset_label)

        # Inserção dos botões criados no left_layout
        left_layout.addWidget(self.add_class_button)
        left_layout.addWidget(self.open_dataset_button)
        left_layout.addWidget(self.manage_dataset_button)

        # ....................................................................

        # Criação do Widget responsável pela reprodução do Vídeo
        self.video_widget = self.video_controller.create_video_widget()
        # Inserção do widget de vídeo no video_layout
        video_layout.addWidget(self.video_widget)
        # Inserção do widget de slider no video_layout
        video_layout.addLayout(self.timeline_layout)

        # ....................................................................

        # Inserção do controls_layout e sua respectiva label no video_layout
        video_layout.addWidget(controls_label)
        video_layout.addLayout(controls_layout)
        # Inserção do functions_layout e sua respectiva label no video_layout
        video_layout.addWidget(functions_label)
        video_layout.addLayout(functions_layout)

        # --------------------------------------------------------------------------------------------------------------
        #   OBS: 'video_layout' contém tanto o widget de vídeo quanto os componentes definidos em 'controls_layout'
        # --------------------------------------------------------------------------------------------------------------

        # Inserção dos layouts secundários left_layout e video_layout
        # no main_layout (Gera uma estrutura hierárquica de layouts)
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(video_layout, 4)

        # Define o main_layout como Layout do Widget central da aplicaçao
        central_widget.setLayout(main_layout)
        # Chama a função responsável por conectar cada botão à uma função do script
        self.connect_signals()

    # ------------------------------------------------------------------------------------------------------------------
    #             Função responsável por conectar os elementos de controle da UI aos respectivos métodos
    # ------------------------------------------------------------------------------------------------------------------
    def connect_signals(self):

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
        self.timeline_slider.sliderReleased.connect(self.slider_released)

        # Conexão de sinal emitido ao iniciar a seleção da ROI
        self.video_widget.pause_requested.connect(self.pause_video)
        # Conexão do checkbox para travar a ROI
        self.lock_roi_checkbox.toggled.connect(self.video_controller.set_lock_roi)

    # ------------------------------------------------------------------------------------------------------------------
    #                   Conjunto de funções referentes ao controle e execução do Vídeo
    # ------------------------------------------------------------------------------------------------------------------

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
            self.video_controller.load_video(path)
            # Obtém apenas o nome do arquivo base para exibição
            file_basename = os.path.basename(self.data_controller.dataset_path)
            self.dataset_label.setText(file_basename)
            # Ao abrir o vídeo, o slider atualiza seu valor máximo com base no total de frames
            self.timeline_slider.setMaximum(self.video_controller.total_frames - 1)

        # Atualiza a exibição
        self.update_frame()
        self.start_video()

    # ..................................................................................................................

    # Função responsável por renderizar o frame do vídeo na janela
    def display_frame(self, frame):
        if frame is None:
            return

        # Converte o frame para um formato compatível com Qt, no caso, um pixmap
        pixmap = ConversionServices.convert_cv_to_qt(frame)

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

    # ..................................................................................................................

    def start_video(self):
        # Controle de reprodução do vídeo seguido pelo controle do temporizador
        self.video_controller.play()
        frame_interval = self.video_controller.frame_interval
        self.timer.start(frame_interval)

    # ..................................................................................................................

    def pause_video(self):
        # Controle de pausa do vídeo seguido pelo controle do temporizador
        self.video_controller.pause()
        self.timer.stop()

    # ..................................................................................................................

    def next_frame(self):
        self.pause_video()
        # Controle do avanço de frame do vídeo
        self.video_controller.next_frame()
        self.update_frame()

    # ..................................................................................................................

    def previous_frame(self):
        self.pause_video()
        # Controle do retrocesso de frame do vídeo
        self.video_controller.previous_frame()
        self.update_frame()

    # ..................................................................................................................

    def update_frame(self, frame=None):
        # Obtenção e exibição do frame atual
        if frame is None:
            frame = self.video_controller.get_frame()

        self.display_frame(frame)

    # ..................................................................................................................

    def update_playback_frame(self):
        # Obtenção do frame subsequente e atualização do temporizador
        frame = self.video_controller.get_next_frame()
        if frame is None:
            self.timer.stop()
            return

        self.display_frame(frame)
        self.update_timeline()

    # ..................................................................................................................

    def slider_released(self):
        # Define o frame com base na posição do slider e atualiza a reprodução
        frame_number = self.timeline_slider.value()
        frame = self.video_controller.seek(frame_number)

        self.update_frame(frame)
        self.start_video()

    # ------------------------------------------------------------------------------------------------------------------
    #                     Função referente ao controle e atualização do temporizador
    # ------------------------------------------------------------------------------------------------------------------

    def update_timeline(self):

        # 'blockSignals' impede termporariamente que um Widget emita sinais.
        # Esse comando evita que a atualização de valores ocorra de forma
        # segura, sem gerar loops inconsistentes
        self.timeline_slider.blockSignals(True)
        self.timeline_slider.setValue(self.video_controller.current_frame)
        self.timeline_slider.blockSignals(False)

        # Atualiza a Label do slider sempre que um novo frame for exibido

        # Tempo atual do vídeo
        current_time = (self.video_controller.current_frame / self.video_controller.fps)
        # Tempo total do vídeo
        total_time = (self.video_controller.total_frames / self.video_controller.fps)
        # Formatação do tempo atual de vídeo (mm:ss)
        current_video_time = self.video_controller.format_time(current_time)
        # Formatação do tempo total de vídeo (mm:ss)
        total_video_time = self.video_controller.format_time(total_time)
        self.frame_label.setText(f"{current_video_time} / {total_video_time}")

    # ------------------------------------------------------------------------------------------------------------------
    #                   Conjunto de funções referentes ao gerenciamento do dataset e classes
    # ------------------------------------------------------------------------------------------------------------------

    def open_dataset(self):

        # Obtenção do caminho da base selecionada
        path = QFileDialog.getExistingDirectory(self, "Selecionar Dataset")
        if not path:
            return

        # Obtenção das classes pré-existentes base e subsequente exibição na janela
        classes = self.data_controller.open_dataset(path)
        self.class_list.clear()
        self.class_list.addItems(classes)
        self.classes = classes
        self.dataset_label.setText(path)

    # ..................................................................................................................

    def add_class(self):

        # Solicita ao usuário pelo nome da nova classe à ser adicionada
        class_name, ok = QInputDialog.getText(self, "Nova Classe", "Nome da classe:")
        if not ok:
            return

        # Remoção de espaços em branco nas extremidades do nome inserido
        class_name = class_name.strip()
        if not class_name:
            return

        # Atualização da lista de classes
        self.data_controller.add_class(class_name)
        self.class_list.addItem(class_name)

    # ..................................................................................................................

    def rename_class(self, item):

        # Obtém o nome original da classe e solicita ao usuário um novo nome para a classe
        old_name = item.text()
        new_name, ok = QInputDialog.getText(self, "Renomear Classe", "Novo nome:", text=old_name)
        if not ok:
            return

        # Remoção de espaços em branco nas extremidades do nome inserido
        new_name = new_name.strip()
        if not new_name:
            return

        # Atualização da lista de classes
        self.data_controller.rename_class(old_name, new_name)
        item.setText(new_name)

    # ..................................................................................................................

    def delete_class(self, item):

        # Obtém o nome da classe e questiona o usuário sobre a exclusão da classe e seu conteúdo
        class_name = item.text()
        response = QMessageBox.question(self, "Excluir Classe", f"Excluir '{class_name}' e seu conteúdo?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response != QMessageBox.Yes:
            return

        # Deleta a classe selecionada e atualiza a lista de classes
        self.data_controller.delete_class(class_name)
        row = self.class_list.row(item)
        self.class_list.takeItem(row)

    # ..................................................................................................................

    def show_class_menu(self, position):

        item = self.class_list.itemAt(position)
        if item is None:
            return

        # Definição dos itens do menu de opções referente à classe selecionada
        menu = QMenu()
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")

        # Abre e posiciona um menu de contexto (clique com o botão direito)
        # exatamente onde o usuário clicou
        action = menu.exec(self.class_list.mapToGlobal(position))

        # Chama as funções relativas ao item selecionado
        if action == rename_action:
            self.rename_class(item)
        elif action == delete_action:
            self.delete_class(item)

    # ..................................................................................................................

    def save_roi(self):

        # Valida se há uma ROI definida
        if self.video_widget.real_roi is None:
            QMessageBox.warning(self, "Erro", "Nenhuma ROI selecionada")
            return

        # Obtém a classe que foi selecionada para o armazenamento da ROI
        selected_item = self.class_list.currentItem()

        # Valida se alguma classe foi selecionada para o armazenamento da ROI
        if selected_item is None:
            QMessageBox.warning(self, "Erro", "Nenhuma classe selecionada")
            return

        # Chama a função no controller (AppController) responsável pelo armazenamento da ROI
        # na classe selecionada pelo usuário
        self.data_controller.save_roi(
            self.video_controller.current_frame_image,
            self.video_widget.real_roi,
            selected_item.text()
        )

        # Informa o sucesso do armazenamento ao usuário
        QMessageBox.information(self, "Sucesso", "ROI salva com sucesso")
