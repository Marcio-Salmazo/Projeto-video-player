import os
import cv2
import shutil


class DatasetServices:

    def __init__(self):

        # Estrutura padrão da base criada - root/Datasets/'nome da base'
        self.base_path = None

    # ------------------------------------------------------------------------------------------------------------------
    #             Definição dos estados associados à reprodução do vídeo e chamada de funções associadas
    # ------------------------------------------------------------------------------------------------------------------

    def create_dataset(self, dataset_name):

        # Estrutura padrão da base - root/Datasets/'nome da base'
        self.base_path = os.path.join("Datasets", dataset_name)
        if self.base_path is None:
            return

        # Criação da estrutura principal do Dataset
        # Dentro do caminho estipulado em self.base_path, são
        # criados sub-diretórios para cada uma das classes definidas
        os.makedirs(self.base_path, exist_ok=True)

    # ..................................................................................................................

    def open_dataset(self, dataset_path):
        # Incialização vazia da lista de classes encontradas
        classes = []

        # Percorre cada um dos diretórios presentes no caminho indicado
        for item in os.listdir(dataset_path):

            # Valida se o item lido é um diretório ou um arquivo
            # Inclui na lista de classe APENAS o itens que são diretórios
            full_path = os.path.join(dataset_path, item)
            if os.path.isdir(full_path):
                classes.append(item)

        # Define o caminho da base global
        self.base_path = dataset_path

        # Retorna a lista, de maneira ordenada
        return sorted(classes)

    # ..................................................................................................................

    def add_class(self, class_name):
        if self.base_path is None:
            return

        # Cria um novo diretório com o nome definido por 'class_name'
        # no caminho do dataset gerado
        class_path = os.path.join(self.base_path, class_name)
        os.makedirs(class_path, exist_ok=True)

    # ..................................................................................................................

    def rename_class(self, old_name, new_name):
        if self.base_path is None:
            return

        old_path = os.path.join(self.base_path, old_name)
        new_path = os.path.join(self.base_path, new_name)
        os.rename(old_path, new_path)

    # ..................................................................................................................

    def delete_class(self, class_name):
        if self.base_path is None:
            return

        # Define o caminho da classe a ser removida
        class_path = os.path.join(self.base_path, class_name)
        # Remove recursivamente o diretório e todos os itens internos
        shutil.rmtree(class_path)

    # ..................................................................................................................

    def save_roi(self, frame, roi, class_name):

        # Recebe as coordenadas definidos para o ROI
        x1, y1, x2, y2 = roi.normalized()
        # Aplica o corte no frame selecionado, em conformidade com as coordenadas
        cropped = frame[y1:y2, x1:x2]

        if cropped.size == 0:
            print("ROI inválida")
            return

        # Caminho da Classe que deve conter o ROI e Casting do path para String
        class_path = os.path.join(str(self.base_path), str(class_name))
        file_count = len(os.listdir(class_path))  # Contagem de itens no diretório da classe
        filename = f"{class_name}_{file_count + 1:06d}.png"  # Construção do nome do frame salvo
        full_path = os.path.join(class_path, filename)  # Caminho completo do frame
        cv2.imwrite(full_path, cropped)  # Armazenamento efetivo do frame
        print(f"Imagem salva: {full_path}")  # Mensagem de LOG
