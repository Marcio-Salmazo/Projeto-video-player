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
from ..models.Display_Info import DisplayInfo


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

    # =================================================================
    #       EVENTOS RELACIONADOS AO MONITORAMENTO DO MOUSE
    # =================================================================
    def mousePressEvent(self, event):

        if not self.point_inside_image(
                event.position().x(),
                event.position().y()
        ):
            return

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
        fx1, fy1 = self.widget_to_frame_coords(self.start_x, self.start_y)
        fx2, fy2 = self.widget_to_frame_coords(self.end_x, self.end_y)
        self.roi = ROI_Model(fx1,fy1,fx2,fy2)

        self.update()

    # =================================================================
    #                     DESENHO DA ROI NA IMAGEM
    # =================================================================
    def paintEvent(self, event):
        super().paintEvent(event)

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

    # =================================================================
    #                      CONVERSÃO DE COORDENADAS
    #                          Posição do mouse
    #                                 ↓
    #                      Posição na imagem escalada
    #                                 ↓
    #                       Posição no frame original
    # =================================================================
    def widget_to_frame_coords(self, x, y):

        info = self.display_info

        x -= info.offset_x
        y -= info.offset_y

        frame_x = int(x * info.scale_x)
        frame_y = int(y * info.scale_y)

        return frame_x, frame_y

    # =================================================================
    #         GARANTE QUE A SELEÇÃO ESTÁ DENTRO DA IMAGEM
    # =================================================================
    def point_inside_image(self, x, y):

        return (
                self.display_info.offset_x <= x <= self.display_info.offset_x + self.display_info.display_width
                and
                self.display_info.offset_y <= y <= self.display_info.offset_y + self.display_info.display_height
        )