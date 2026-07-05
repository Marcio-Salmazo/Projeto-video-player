from enum import Enum, auto


# Ao herdar de Enum, cada atributo da classe se torna um valor constante da enumeração.
# O auto() faz com que o Python atribua automaticamente um valor inteiro ao membro.
class VideoState(Enum):

    STOPPED = auto()
    PLAYING = auto()
    PAUSED = auto()
    SEEKING = auto()
