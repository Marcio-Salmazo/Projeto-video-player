"""
    OBS: O decorador @dataclass, é usado para criar classes estruturadas
         focadas principalmente no armazenamento de dados. Ele elimina a
         necessidade de escrever código repetitivo ao gerar automaticamente
         métodos essenciais, como __init__ (construtor), __repr__ e __eq__.
"""

from dataclasses import dataclass
from ...models.fsm.user_role import UserRole


@dataclass
class UserModel:

    username: str
    password: str
    role: UserRole
