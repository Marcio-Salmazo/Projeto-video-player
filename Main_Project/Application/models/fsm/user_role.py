"""
    Script responsável por definir os papeis de cada usuário

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
from enum import Enum


class UserRole(Enum):

    # Estados relacionados ao usuário
    ADMIN = 'ADMIN'
    ANNOTATOR = 'ANNOTATOR'
