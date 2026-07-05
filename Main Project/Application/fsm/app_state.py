from enum import Enum, auto


# Ao herdar de Enum, cada atributo da classe se torna um valor constante da enumeração.
# O auto() faz com que o Python atribua automaticamente um valor inteiro ao membro.
class AppState(Enum):

    INITIAL = auto()
    READY = auto()
