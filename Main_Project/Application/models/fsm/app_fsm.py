from .app_state import AppState


# Classe responsável por gerenciar o estado da aplicação
class ApplicationFSM:

    def __init__(self):
        # Inicialização do estado da aplicação
        self._state = AppState.INITIAL

    # ..................................................................................................................
    # Obtém o estado da aplicação
    # OBSERVAÇÃO: @property trata métodos como atributos e é utilizado quando o objetivo é para obter informações
    @property
    def state(self):
        return self._state

    # ------------------------------------------------------------------------------------------------------------------
    #                            Funções que definem o estado atual da aplicação
    # ------------------------------------------------------------------------------------------------------------------

    def dataset_ready(self):
        self._state = AppState.DATASET_READY

    def video_ready(self):
        self._state = AppState.VIDEO_READY

    def roi_selection(self):
        self._state = AppState.ROI_SELECTION

    def roi_selected(self):
        self._state = AppState.ROI_SELECTED

    def roi_locked(self):
        self._state = AppState.ROI_LOCKED

    def classification(self):
        self._state = AppState.CLASSIFICATION

    # ------------------------------------------------------------------------------------------------------------------
    #                            Funções que conferem o estado atual da aplicação
    # ------------------------------------------------------------------------------------------------------------------

    def is_dataset_ready(self):
        return self._state == AppState.DATASET_READY

    def is_video_ready(self):
        return self._state == AppState.VIDEO_READY

    def is_roi_selection(self):
        return self._state == AppState.ROI_SELECTION

    def is_roi_selected(self):
        return self._state == AppState.ROI_SELECTED

    def is_roi_locked(self):
        return self._state == AppState.ROI_LOCKED

    def is_classification(self):
        return self._state == AppState.CLASSIFICATION
