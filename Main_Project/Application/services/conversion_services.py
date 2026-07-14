# A classe se responsabiliza pelas conversões entre formatos de imagem e redimensionamento de frames
import cv2
from PySide6.QtGui import QImage, QPixmap


class ConversionServices:

    # ------------------------------------------------------------------------------------------------------------------
    #         Função de conversão entre as coordenadas apresentadas na janela e as dimensões reais do frame
    #               Considera: Posição do mouse - Posição na imagem escalada - Posição no frame original
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def widget_to_frame(x, y, display_info):

        info = display_info
        x -= info.offset_x
        y -= info.offset_y

        # As coordenadas do widget são multiplicadas pelo fator de escala
        frame_x = int(x * info.scale_x)
        frame_y = int(y * info.scale_y)
        return frame_x, frame_y

    # ..................................................................................................................

    @staticmethod
    def point_inside_image(x, y, display_info):
        # Garantia de que as coordenadas selecionadas estão dentro da janela do vídeo
        return (display_info.offset_x <= x <= display_info.offset_x + display_info.display_width and
                display_info.offset_y <= y <= display_info.offset_y + display_info.display_height)

    # ------------------------------------------------------------------------------------------------------------------
    #                Função de conversão entre os formatos de imagem do OpenCV para Pixmap (PyQt)
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def convert_cv_to_qt(frame):
        # Conversão do frame de BGR para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Obtenção dos dado de altura, largura e canais do frame
        h, w, ch = rgb_frame.shape
        # Obtenção da quantidade de bytes por linha
        bytes_per_line = ch * w
        # Conversão efetiva para QImage
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Conversão e retorno do formato para QPixmap
        return QPixmap.fromImage(qt_image)
