"""
    OBS: O decorador @dataclass, é usado para criar classes estruturadas
         focadas principalmente no armazenamento de dados. Ele elimina a
         necessidade de escrever código repetitivo ao gerar automaticamente
         métodos essenciais, como __init__ (construtor), __repr__ e __eq__.
"""

from dataclasses import dataclass
from Main_Project.Application.models.fsm.user_role import UserRole


@dataclass
class UserModel:

    # Criação do modelo base de um usuário
    # composto por nome, senha e papel no aplicativo.
    #   OBS: Esse padrão deve ser seguido no arquivo json

    username: str
    password: str

    # O papel do usuário é definido por UserRole
    # estando restrito aos tipos definifos no Script
    role: UserRole
