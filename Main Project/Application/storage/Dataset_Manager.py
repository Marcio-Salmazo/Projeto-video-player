"""
    Script responsável por definir os métodos e funcionalidades
    referentes ao armazenamento dos dados coletados e à
    organização estrutural do Dataset
"""

import os
import cv2
import shutil


class DatasetManager:
    def __init__(self, dataset_name="mydataset"):
        self.base_path = os.path.join("Datasets", dataset_name)

    # =================================================================
    #             CARREGAMENTO DE DATASET PRÉ-EXISTENTE
    # =================================================================
    def load_dataset(self, dataset_path):

        # Recebe o caminho da base a ser carregada
        self.base_path = dataset_path
        # Incialização vazia da lista de classes encontradas
        classes = []

        # Percorre cada um dos diretórios presentes no caminho indicado
        for item in os.listdir(dataset_path):

            # Valida se o item lido é um diretório ou um arquivo
            # Inclui na lista de classe APENAS o itens que são diretórios
            full_path = os.path.join(dataset_path, item)
            if os.path.isdir(full_path):
                classes.append(item)

        # Retorna a lista, de maneira ordenada
        return sorted(classes)

    # =================================================================
    #            CRIAÇÃO DE NOVA CLASSE DENTRO DO DATASET
    # =================================================================
    def create_class(self, class_name):
        # Cria um novo diretório com o nome definido por 'class_name'
        # no caminho do dataset gerado
        class_path = os.path.join(self.base_path, class_name)
        os.makedirs(class_path, exist_ok=True)

    # =================================================================
    #               RENOMEAR CLASSE DENTRO DO DATASET
    # =================================================================
    def rename_class(self, old_name, new_name):
        old_path = os.path.join(self.base_path, old_name)
        new_path = os.path.join(self.base_path, new_name)
        os.rename(old_path,new_path)

    # =================================================================
    #            EXCLUSÃO DE CLASSE DENTRO DO DATASET
    # =================================================================
    def delete_class(self, class_name):

        # Define o caminho da classe a ser removida
        class_path = os.path.join(self.base_path, class_name)
        # Remove recursivamente o diretório e todos os itens internos
        shutil.rmtree(class_path)

    # =================================================================
    #               CRIAÇÃO DA ESTRUTURA DO DATASET
    # =================================================================
    def create_dataset_structure(self, classes):

        # Criação da estrutura principal do Dataset
        # Dentro do caminho estipulado em self.base_path, são
        # criados sub-diretórios para cada uma das classes definidas
        os.makedirs(self.base_path, exist_ok=True)
        for cls in classes:
            os.makedirs(os.path.join(self.base_path, cls), exist_ok=True)

    # =================================================================
    #               ARMAZENAMENTO EFETIVO DA ROI
    # =================================================================
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
