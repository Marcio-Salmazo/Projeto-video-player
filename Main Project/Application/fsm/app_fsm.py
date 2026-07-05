from .app_state import AppState


# Classe responsável por gerenciar o estado da aplicação
class ApplicationFSM:

    def __init__(self):
        # Inicialização do estado da aplicação
        self._state = AppState.INITIAL

    # ..................................................................................................................
    # Obtém o estado da aplicação
    # OBSERVAÇÃO: @property trata métodos como atributos e é
    # utilizado quando o objetivo é para obter informações
    @property
    def state(self):
        return self._state

    # ------------------------------------------------------------------------------------------------------------------
    #                            Funções que definem o estado atual da aplicação
    # ------------------------------------------------------------------------------------------------------------------

    def dataset_ready(self):
        self._state = AppState.READY

    # ------------------------------------------------------------------------------------------------------------------
    #                            Funções que conferem o estado atual da aplicação
    # ------------------------------------------------------------------------------------------------------------------

    def is_ready(self):
        return self._state == AppState.READY
