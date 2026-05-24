"""
    Script responsável por definir os métodos e funcionalidades
    referentes ao armazenamento dos dados coletados e à
    organização estrutural do Dataset
"""

import os
import cv2


class DatasetManager:
    def __init__(self, dataset_name="my_dataset"):
        self.base_path = os.path.join("datasets", dataset_name)

    def create_dataset_structure(self, classes):

        # Criação da estrutura principal do Dataset
        # Dentro do caminho estipulado em self.base_path, são
        # criados sub-diretórios para cada uma das classes definidas
        os.makedirs(self.base_path, exist_ok=True)
        for cls in classes:
            os.makedirs(os.path.join(self.base_path, cls), exist_ok=True)

    def save_roi(self, frame, roi, class_name):

        # Recebe as coordenadas definidos para o ROI
        x1, y1, x2, y2 = roi.normalized()
        # Aplica o corte no frame selecionado, em conformidade com as coordenadas
        cropped = frame[y1:y2, x1:x2]

        if cropped.size == 0:
            print("ROI inválida")
            return

        class_path = os.path.join(self.base_path, class_name)  # Caminho da Classe que deve conter o ROI
        file_count = len(os.listdir(class_path))  # Contagem de itens no diretório da classe
        filename = f"{class_name}_{file_count + 1:06d}.png"  # Construção do nome do frame salvo
        full_path = os.path.join(class_path, filename)  # Caminho completo do frame
        cv2.imwrite(full_path, cropped)  # Armazenamento efetivo do frame
        print(f"Imagem salva: {full_path}")  # Mensagem de LOG
