from .video_state import VideoState


class VideoFSM:

    def __init__(self):
        # Inicialização do estado da aplicação
        self._state = VideoState.STOPPED

    # Obtém o estado do video
    @property
    def state(self):
        return self._state

    # ------------------------------------------------------------------------------------------------------------------
    #                            Funções que definem o estado atual da video
    # ------------------------------------------------------------------------------------------------------------------

    def playing(self):
        self._state = VideoState.PLAYING

    def paused(self):
        self._state = VideoState.PAUSED

    def stopped(self):
        self._state = VideoState.STOPPED

    def seeking(self):
        self._state = VideoState.SEEKING

    # ------------------------------------------------------------------------------------------------------------------
    #                            Funções que conferem o estado atual do vídeo
    # ------------------------------------------------------------------------------------------------------------------

    def is_playing(self):
        return self._state == VideoState.PLAYING

    def is_paused(self):
        return self._state == VideoState.PAUSED

    def is_stopped(self):
        return self._state == VideoState.STOPPED

    def is_seeking(self):
        return self._state == VideoState.SEEKING
