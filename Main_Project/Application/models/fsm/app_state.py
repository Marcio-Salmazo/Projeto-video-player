from enum import Enum, auto


# Ao herdar de Enum, cada atributo da classe se torna um valor constante da enumeração.
# O auto() faz com que o Python atribua automaticamente um valor inteiro ao membro.
class AppState(Enum):

    # Estado Inicial, com nada carregado (Dataset, Video)
    INITIAL = auto()

    # Existe um dataset aberto (Permitido gerenciar classes e abrir vídeo)
    DATASET_READY = auto()

    # Vídeo carregado. (Controles de Reprodução)
    VIDEO_READY = auto()

    # Usuário está criando uma ROI. (Entra em mousePressEvent e sai em mouseReleaseEvent)
    ROI_SELECTION = auto()

    # Existe uma ROI válida. (Permite seu armazenamento)
    ROI_SELECTED = auto()

    # Espaço fixo da roi. (Permite movimentar da ROI)
    ROI_LOCKED = auto()

    # Quando um usuário comum abrir um dataset.
    CLASSIFICATION = auto()
