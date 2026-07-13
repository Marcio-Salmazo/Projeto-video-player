from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QRect, Signal
from ..models.dataClasses.roi_model import ROI_Model
from ..models.dataClasses.display_model import DisplayInfo
from ..models.services.conversion_services import ConversionServices


# Classe de criação da Janela
class VideoWidget(QLabel):
    # Sinal de pause (Para o caso do clique na janela (Ao selecionar a ROI))
    pause_requested = Signal()

    def __init__(self, app_fsm):
        super().__init__()

        # Configurações base do Widget
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(800, 600)

        # Coordenadas da ROI no widget
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        # Coordenadas da ROI na área de exibição do widget
        self.visualROI = None
        # Flag para avaliar se a seleção está sendo desenhada
        self.drawing = False
        # Região selecionada como ROI
        self.real_roi = None

        # Dataclass para informações de Display
        self.display_info = DisplayInfo()

        # Flag do estado do checkbox
        self.lock_roi = False
        # Flag para definir se a roi está ou não sendo movimentada
        self.dragging_roi = False
        # Pontos de referência para saber onde foi feito o clique do Mouse dentro da roi
        # Isso evita que a roi dê um pulo para ficar centralizada com o mouse
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Estados relacionados à Aplicação
        self.app_fsm = app_fsm

    # ------------------------------------------------------------------------------------------------------------------
    #                   Conjunto de funções referentes ao controle de eventos do Mouse
    # ------------------------------------------------------------------------------------------------------------------
    def mousePressEvent(self, event):

        # Emissão do sinal de pausa de vídeo
        self.pause_requested.emit()
        # Valida se o ponto está dentro da área delimitada do Widget
        if not ConversionServices.point_inside_image(event.position().x(), event.position().y(), self.display_info):
            return

        # Valida se o checkbox de travar a roi está marcado e se existe uma seleção
        if self.lock_roi:
            # Valida se o clique foi feito dentro da seleção
            if self.point_inside_roi(event.position().x(), event.position().y()):

                # Define os offsets para manter a janela na posição do clique
                self.drag_offset_x = (event.position().x() - self.visualROI.left())
                self.drag_offset_y = (event.position().y() - self.visualROI.top())

                # Atualiza a flag
                self.dragging_roi = True
                self.drawing = False

        if not self.lock_roi:

            # Estado de seleção
            self.app_fsm.roi_selection()

            # Armazenamento das coordenadas iniciais no momento do clique
            self.start_x = event.position().x()
            self.start_y = event.position().y()
            self.end_x = self.start_x
            self.end_y = self.start_y
            # Atualização da Flag e atualizar elemento
            self.drawing = True

    def mouseMoveEvent(self, event):

        if self.dragging_roi and not self.drawing:
            # Novos valores para a roi, considerando os
            # offsets e a posição do Mouse
            x = event.position().x() - self.drag_offset_x
            y = event.position().y() - self.drag_offset_y
            self.visualROI.moveTo(x, y)
            self.update()

        if self.drawing:
            # Atualiza consistentemente as coordenadas finais
            self.end_x = event.position().x()
            self.end_y = event.position().y()

            # Desenha a roi de acordo com as coordenadas atualizadas
            self.visualROI = QRect(
                int(self.start_x),
                int(self.start_y),
                int(self.end_x - self.start_x),
                int(self.end_y - self.start_y)
            )
            self.update()

    def mouseReleaseEvent(self, event):

        if self.dragging_roi:
            self.dragging_roi = False

        else:
            # Atualiza a Flag de desenho
            self.drawing = False

        self.app_fsm.roi_locked()
        self.update_roi_model()

    # ------------------------------------------------------------------------------------------------------------------
    #                          Função referentes ao desenho efetivo da ROI na janela
    # ------------------------------------------------------------------------------------------------------------------
    def paintEvent(self, event):
        super().paintEvent(event)

        if not (self.real_roi or self.drawing):
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

        # painter.drawRect(self.visualROI)

        # Coordenadas da ROI na área de exibição do widget
        # Serve para a função de travar a ROI
        if self.visualROI is None:
            self.visualROI = rect
        painter.drawRect(self.visualROI)

    # ------------------------------------------------------------------------------------------------------------------
    #                                   Função referentes à movimentação da roi
    # ------------------------------------------------------------------------------------------------------------------

    def update_roi_model(self):
        # Atualiza as coordenadas reais da roi de acordo com a área desenhada no widget
        fx1, fy1 = ConversionServices.widget_to_frame(
            self.visualROI.left(),
            self.visualROI.top(),
            self.display_info
        )

        fx2, fy2 = ConversionServices.widget_to_frame(
            self.visualROI.right(),
            self.visualROI.bottom(),
            self.display_info
        )

        self.real_roi = ROI_Model(fx1, fy1, fx2, fy2)

    def point_inside_roi(self, x, y):
        if self.visualROI is None:
            return False
        return self.visualROI.contains(int(x), int(y))
