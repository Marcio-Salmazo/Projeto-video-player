"""
    Script responsável pelo modelo dos dados referêntes à
    zona de interesse selecionada pelo usuário. Aqui são
    feitas as padronizações da ROI para futuro armazenamento

    OBS: O decorador '@dataclass' simplifica a criação de classes
         cujo principal objetivo é armazenar dados.
    OBS: A classe apenas define e normaliza as coordenadas recebidas
         que constituem a ROI de um determinado frame
"""
from dataclasses import dataclass


@dataclass
class ROI_Model:
    x1: int
    y1: int
    x2: int
    y2: int

    def width(self):
        return abs(self.x2 - self.x1)

    def height(self):
        return abs(self.y2 - self.y1)

    def normalized(self):
        return (
            min(self.x1, self.x2),
            min(self.y1, self.y2),
            max(self.x1, self.x2),
            max(self.y1, self.y2)
        )
