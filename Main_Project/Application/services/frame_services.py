"""
    Responsável pelo acesso das imagens registradas na base
    e demaois serviços associados ao processo de classificação das
    ROIs extraídas, por usuários não-administradores.
"""

from pathlib import Path
import cv2


class FrameServices:

    def __init__(self):

        # Lista de caminhos das imagens existentes na base de dados
        self.images = []
        self.current_index = 0
        self.valid_formats = {".jpg", ".jpeg", ".png"}

    # COMO EVITAR O CARREGAMENTO DE UMA PASTA QUALQUER E INFLAR DEMAIS A LISTA?
    def load_samples(self, dataset_path):

        # Reset a lista ao chamar a função
        self.images.clear()

        if dataset_path is None:
            return

        # A profundidade da busca é limitada a apenas 2 niveis: 'diretorio_pai/classe/'
        for classes in dataset_path.iterdir():

            # Valida inicialmente se o item percorrido atual (classes) é um diretório
            if not classes.is_dir():
                continue

            # Percorre cada um dos itens em determinada classe
            for item in classes.iterdir():

                # Valida se o item do loop é uma imagem e se está no formato esperado
                if item.is_file() and item.suffix.lower() in self.valid_formats:

                    # Armazena na lista o caminho Dataset/Classe/Amostra
                    self.images.append(item.relative_to(dataset_path.parent))

        # organiza os objetos Path em ordem alfabética
        self.images.sort(key=str)
        # Define o index incial
        self.current_index = 0

    def current_image(self):

        if not self.images:
            return None

        # Retorna a leitura da imagem pelo OpenCV referente ao caminho definido na lista
        return cv2.imread(str(self.images[self.current_index]))

    def next_image(self):

        # Valida se é possível avançar o frame e atualiza o índice
        if self.current_index < len(self.images) - 1:
            self.current_index += 1

        # Retorna a leitura da imagem no próximo índice
        return self.current_image()

    def previous_image(self):

        # Valida se é possível avançar o frame e atualiza o índice
        if self.current_index > 0:
            self.current_index -= 1

        # Retorna a leitura da imagem no índice anterior
        return self.current_image()


