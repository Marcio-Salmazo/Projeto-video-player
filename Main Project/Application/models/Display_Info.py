"""O decorador @dataclass, é usado para criar classes estruturadas
focadas principalmente no armazenamento de dados. Ele elimina a
necessidade de escrever código repetitivo ao gerar automaticamente
métodos essenciais, como __init__, __repr__ e __eq__."""
from dataclasses import dataclass

@dataclass
class DisplayInfo:

    frame_width: int = 0
    frame_height: int = 0

    display_width: int = 0
    display_height: int = 0

    offset_x: float = 0.0
    offset_y: float = 0.0

    @property
    def scale_x(self):

        if self.display_width == 0:
            return 1

        return self.frame_width / self.display_width

    @property
    def scale_y(self):

        if self.display_height == 0:
            return 1

        return self.frame_height / self.display_height