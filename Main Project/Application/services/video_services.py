from ..fsm.video_fsm import VideoFSM
import cv2


class VideoServices:

    def __init__(self, app_fsm):

        self.video_fsm = VideoFSM()
        # Definição do application FSM
        self.app_fsm = app_fsm

        self.cap = None  # Captura do arquivo Vídeo pelo cv2
        self.total_frames = 0  # Valor total de frames no vídeo
        self.current_frame_value = 0  # Armazena o valor atual do frame
        self.fps = 30  # Limitação da velocidade de reprodução
        self.current_frame_image = None  # Armazena o frame já carregado

    # ------------------------------------------------------------------------------------------------------------------
    #            Operações relacionadas ao controle e reprodução do vídeo, além da definição dos estados
    # ------------------------------------------------------------------------------------------------------------------

    def load_video(self, path):

        # Carregamento efetivo do vídeo pelo OpenCV
        self.cap = cv2.VideoCapture(path)

        # Validação do arquivo carregado
        if not self.cap.isOpened():
            raise Exception("Erro ao abrir vídeo")

        # Obtenção das informações principais obtidos pelo carregamento do vídeo
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.current_frame_value = 0

        # Define o estado para o vídeo em PLAYING
        self.video_fsm.play()
        # Define o estado para a aplicação em VIDEO_OPEN
        self.app_fsm.dataset_ready()

    # ..................................................................................................................

    def play(self):
        # Define o estado para o vídeo em PLAYING
        self.video_fsm.play()

    # ..................................................................................................................

    def pause(self):
        # Define o estado para o vídeo em PAUSED
        self.video_fsm.pause()

    # ..................................................................................................................

    def stop(self):
        # Define o estado para o vídeo STOPPED
        self.video_fsm.stop()

    # ..................................................................................................................

    def next_frame(self):
        # Avalia se o proximo frame não extrapola o total e define a posição de acordo com o próximo frame da sequência
        if self.current_frame_value < self.total_frames - 1:
            self.current_frame_value += 1

        # Define o estado para o vídeo em PAUSED
        self.video_fsm.pause()

    # ..................................................................................................................

    def previous_frame(self):
        # Avalia se o proximo frame não extrapola o inicío e define a posição de acordo com o frame anterior
        if self.current_frame_value > 0:
            self.current_frame_value -= 1

        # Define o estado para o vídeo em PAUSED
        self.video_fsm.pause()

    # ..................................................................................................................

    def seek(self, frame_number):
        # Define manualmente o valor de posição para o frame 'atual'
        self.current_frame_value = frame_number
        # Reseta a imagem atual (frame)
        self.current_frame_image = None

        # Define o estado para o vídeo em SEEKING
        self.video_fsm.pause()

    # ..................................................................................................................

    def get_frame(self):
        if self.cap is None:
            return None

        # Define a posição de captura do cv2 de acordo com o valor do frame atual
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_value)
        # Lê o frame definido na linha anterior
        success, frame = self.cap.read()

        if not success:
            return None

        # Retorna o frame capturado
        self.current_frame_image = frame
        return frame

    # ..................................................................................................................

    def get_next_frame(self):
        # Realiza a leitura rápida e direta do próximo frame
        if self.cap is None:
            return None

        # Armazena um cache do frame atual
        success, frame = self.cap.read()
        if not success:
            return None

        # Atualiza o valor do frame para o próximo e exibe o atual
        self.current_frame_value += 1
        self.current_frame_image = frame
        return frame

    # ..................................................................................................................

    @property
    def frame_interval(self):
        return int(1000 / max(1, self.fps))

    # ..................................................................................................................

    @staticmethod
    def format_time(seconds):
        # Formatação do tempo - mm:ss
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    # ------------------------------------------------------------------------------------------------------------------
    #                                               Funções de checagem do estado
    # ------------------------------------------------------------------------------------------------------------------

    def is_playing(self):
        return self.video_fsm.is_playing()

    def is_paused(self):
        return self.video_fsm.is_paused()

    def is_stopped(self):
        return self.video_fsm.is_stopped()

    def is_seeking(self):
        return self.video_fsm.is_seeking()
