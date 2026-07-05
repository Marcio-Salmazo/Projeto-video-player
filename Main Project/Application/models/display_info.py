"""
    Script responsável por armazenar informações sobre as dimensões de um frame (imagem original)
    e de sua exibição na tela, além de calcular automaticamente fatores de escala.

    OBS: O decorador @dataclass, é usado para criar classes estruturadas
         focadas principalmente no armazenamento de dados. Ele elimina a
         necessidade de escrever código repetitivo ao gerar automaticamente
         métodos essenciais, como __init__ (construtor), __repr__ e __eq__.'''
"""

from dataclasses import dataclass


@dataclass
class DisplayInfo:

    # Frame original
    frame_width: int = 0
    frame_height: int = 0

    # Frame exibido na janela (Redimensionado)
    display_width: int = 0
    display_height: int = 0

    # Valores de deslocamentos da imagem na tela
    # Utilizados para converter coordenadas do mouse.
    offset_x: float = 0.0
    offset_y: float = 0.0

    '''
        O @property é um recurso que transforma um método de classe em um atributo gerenciado. 
        Isso permite o acesso ou modificação da lógica por trás de um dado usando a sintaxe de um atributo 
        (ex: objeto.valor), sem precisar chamá-lo como função (ex: objeto.valor())
    '''

    @property
    def scale_x(self):

        if self.display_width == 0:
            return 1
        # Retorna a escala de redimensionamento em X
        return self.frame_width / self.display_width

    @property
    def scale_y(self):

        if self.display_height == 0:
            return 1
        # Retorna a escala de redimensionamento em Y
        return self.frame_height / self.display_height
