"""
    Script responsável por definir os métodos e funcionalidades
    referentes à reprodução e manipulação básica do Vídeo.
"""

import cv2


class VideoManager:

    def __init__(self):

        # Valores padrões para os elementos do vídeo
        self.cap = None
        self.total_frames = 0
        self.current_frame = 0
        self.fps = 30

    def load_video(self, path):

        # Carregamento efetivo do vídeo pelo OpenCV
        self.cap = cv2.VideoCapture(path)

        # Validação do arquivo carregado
        if not self.cap.isOpened():
            raise Exception("Erro ao abrir vídeo")

        # Obtenção das informações principais obtidos pelo carregamento do vídeo
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.current_frame = 0

    def get_frame(self):
        if self.cap is None:
            return None

        # Capta e armazena o frame do vídeo referente ao frame
        # atual, no momento da chamada da função.
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        success, frame = self.cap.read()

        if not success:
            return None
        return frame

    def next_frame(self):

        # Avalia se o proximo frame não extrapola o total
        # e define o frame atual como o proximo da sequência
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1

    def previous_frame(self):

        # Avalia se o frame anterior não extrapola o início
        # e define o frame atual como o anterior da sequência
        if self.current_frame > 0:
            self.current_frame -= 1

    def seek(self, frame_number):

        # Define diretamente o valor do frame em exibição
        # de acordo com o parâmetro passado
        self.current_frame = frame_number

    def get_current_frame_number(self):

        # Obtém o valor do frame atual em reprodução
        return self.current_frame
