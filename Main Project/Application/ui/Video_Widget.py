"""
    Script responsável por definir o Widget especializado para a exibição
    do vídeo, detectar o Mouse para seleção do ROI e Desenho da seleção.

    As funcionalidades deste Script são separados da Janela principal pois
    o gerencialmento do ROI é uma funcionalidade independente. Aqui é definido
    o 'Canva Inteligente' da ferramenta
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRect
from ..models.ROI_Model import ROI_Model


# Criação do Widget (herdando as propriedade de um QLabel)
# para a exibição do vídeo selecionado. Essa classe é instânciada
# na tela principal em Main_Window.
class VideoWidget(QLabel):

    # Construtor padrão do Widget de Vídeo
    def __init__(self):
        super().__init__()

        # Configurações base do Widget
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(800, 600)

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        # Flag para avaliar se a seleção está sendo desenhada
        self.drawing = False
        # Região selecionada como ROI
        self.roi = None

    # ==================================================================================================================
    # Funções voltadas para avaliar e monitorar os comandos do Mouse
    #       OBS: self.update() no contexto da GUI é usado para forçar a janela a redesenhar elementos,
    #            processar eventos pendentes ou atualizar uma barra de progresso em tempo real.

    def mousePressEvent(self, event):

        # Armazenamento das coordenadas iniciais no momento do clique
        self.start_x = event.position().x()
        self.start_y = event.position().y()
        self.end_x = self.start_x
        self.end_y = self.start_y

        # Atualização da Flag e atualizar elemento
        self.drawing = True
        self.update()

    def mouseMoveEvent(self, event):
        if self.drawing:

            # Atualiza consistentemente as coordenadas finais
            self.end_x = event.position().x()
            self.end_y = event.position().y()
            self.update()

    def mouseReleaseEvent(self, event):

        # Define e armazena as coordenadas finais ao soltar o clique
        self.end_x = event.position().x()
        self.end_y = event.position().y()

        # Atualiza a Flag
        self.drawing = False

        # Define a zona de interesse com base no modelo padrão
        self.roi = ROI_Model(
            int(self.start_x),
            int(self.start_y),
            int(self.end_x),
            int(self.end_y)
        )
        self.update()

    # ==================================================================================================================

    def paintEvent(self, event):
        super().paintEvent(event)

        # Função responsável por 'desenhar' a ROI no frame selecionado
        # Inicia o desenhho apenas se houver um ROI definido ou se a Flag
        # de desenho estiver ativa.
        if self.roi or self.drawing:

            # Criação e configuração do elemento de pintura
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

            # Desenho da ROI de acordo com as coordenadas definidas
            rect = QRect(
                int(self.start_x),
                int(self.start_y),
                int(self.end_x - self.start_x),
                int(self.end_y - self.start_y)
            )

            painter.drawRect(rect)
