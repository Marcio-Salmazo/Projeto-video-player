"""
    Script responsável por coordenar comunicação entre módulos,
    buscando intermediar as operações que incluem serviços, interface e conversões.
"""

from PySide6.QtGui import QImage, QPixmap
import cv2


# Função estática responsável apenas
# Pela conversão do formato pelo OpenCV para
# algo que seja compreensível pelo Qt (Pixmap)

def convert_cv_to_qt(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_frame.shape
    bytes_per_line = ch * w

    qt_image = QImage(
        rgb_frame.data,
        w,
        h,
        bytes_per_line,
        QImage.Format_RGB888
    )

    return QPixmap.fromImage(qt_image)


# Classe pré-definida para o controller, caso seja necessário
# na implementação de elementos futuros
'''
class AppController:
    def __init__(self, main_window):
        self.main_window = main_window
'''