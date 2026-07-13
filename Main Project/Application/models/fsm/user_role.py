"""
    Usuário Administrador:
        * Criar Dataset
        * Adicionar, Renomear e Excluir Classes
        * Abrir Vídeos
        * Selecionar e Salvar ROIs

    Usuário Classificador:
        * Abrir um dataset
        * Visualizar imagens
        * Classificar imagens
        * Salvar suas classificações
"""
from enum import Enum, auto


class UserRole(Enum):

    # Estados relacionados ao usuário
    ADMIN = auto()
    ANNOTATOR = auto()
