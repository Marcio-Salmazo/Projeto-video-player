from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QRect, Signal
from ..models.roi_model import ROI_Model
from ..models.display_info import DisplayInfo
from .conversion_services import ConversionServices


# Criação do Widget (herdando as propriedade de um QLabel) para a exibição do vídeo selecionado.
class VideoWidget(QLabel):
    # Sinal de pause (Para o caso do clique na janela (Ao selecionar a ROI))
    pause_requested = Signal()

    def __init__(self):
        super().__init__()

        # Coordenadas da ROI na área de exibição do widget
        self.visualROI = None
        # Configurações base do Widget
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(800, 600)

        # Coordenadas da ROI
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        # Flag para avaliar se a seleção está sendo desenhada
        self.drawing = False
        # Região selecionada como ROI
        self.roi = None
        # Dataclass para informações de Display
        self.display_info = DisplayInfo()

    # ------------------------------------------------------------------------------------------------------------------
    #                   Conjunto de funções referentes ao controle de eventos do Mouse
    # ------------------------------------------------------------------------------------------------------------------
    def mousePressEvent(self, event):

        if not ConversionServices.point_inside_image(event.position().x(), event.position().y(), self.display_info):
            return

        # Emissão do sinal de pausa de vídeo
        self.pause_requested.emit()

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

        # Define a zona de interesse
        # O ROI armazenado corresponde à coordenadas reais do vídeo
        fx1, fy1 = ConversionServices.widget_to_frame(self.start_x, self.start_y, self.display_info)
        fx2, fy2 = ConversionServices.widget_to_frame(self.end_x, self.end_y, self.display_info)
        self.roi = ROI_Model(fx1, fy1, fx2, fy2)

        self.update()

    # ------------------------------------------------------------------------------------------------------------------
    #                          Função referentes ao desenho efetivo da ROI na janela
    # ------------------------------------------------------------------------------------------------------------------
    def paintEvent(self, event):
        super().paintEvent(event)

        if not (self.roi or self.drawing):
            return

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
        # Coordenadas da ROI na área de exibição do widget
        # Serve para a função de travar a ROI
        self.visualROI = rect
        painter.drawRect(rect)
