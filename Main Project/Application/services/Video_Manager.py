""" Script responsável por definir os métodos e funcionalidades
referentes à reprodução e manipulação básica do Vídeo. """

import cv2


class VideoManager:

    def __init__(self):

        self.cap = None  # Captura do arquivo Vídeo pelo cv2
        self.total_frames = 0  # Valor total de frames no vídeo
        self.current_frame = 0  # Armazena o valor atual do frame
        self.fps = 30  # Limitação da velocidade de reprodução
        self.current_frame_image = None  # Armazena o frame já carregado

    # =================================================================
    #                 CARREGAMENTO DO ARQUIVO DE VÍDEO
    # =================================================================
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

    # =================================================================
    #            CAPTURA SEQUENCIAL AUTOMÁTICA DOS FRAMES
    # =================================================================
    def read_next_frame(self):
        if self.cap is None:
            return None

        # Realiza a leitura rápida e direta do próximo frame,
        # armazenando um cache do frame atual
        success, frame = self.cap.read()
        if not success:
            return None

        self.current_frame += 1
        self.current_frame_image = frame
        return frame

    # =================================================================
    #              CAPTURA MANUAL DO FRAME EM EXIBIÇÃO
    # =================================================================
    def get_frame_by_position(self):
        if self.cap is None:
            return None

        # Capta e armazena o frame atual
        # no momento da chamada da função.
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        success, frame = self.cap.read()

        if not success:
            return None
        self.current_frame_image = frame
        return frame

    # =================================================================
    #                CAPTURA DOS FRAMES ADJACENTES
    # =================================================================
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

    # =================================================================
    #               GET/SET MANUAL PARA O FRAME ATUAL
    # =================================================================
    def seek(self, frame_number):
        self.current_frame = frame_number
        # Reseta a imagem atual (frame)
        self.current_frame_image = None

    def get_current_frame_number(self):
        return self.current_frame

    # =================================================================
    #                 FORMATAÇÃO DO TEMPO DE VIDEO
    # =================================================================
    @staticmethod
    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"
