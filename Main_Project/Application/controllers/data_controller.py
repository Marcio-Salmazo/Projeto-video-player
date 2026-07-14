from Main_Project.Application.models.fsm.app_fsm import ApplicationFSM
from Main_Project.Application.services.dataset_services import DatasetServices


# Controlador principal da aplicação, responsável por delegar as responsabilidades aos
# modulos específicos. Quem usa a aplicação (por exemplo, a GUI) conversa apenas com ApplicationController.
class DataController:

    # DEFINIR ESTADOS

    def __init__(self):
        self.app_fsm = ApplicationFSM()
        self.dataset = DatasetServices()

    def create_dataset(self, dataset_name):
        self.dataset.create_dataset(dataset_name)
        self.app_fsm.dataset_ready()

    def open_dataset(self, path):
        self.app_fsm.dataset_ready()
        return self.dataset.open_dataset(path)

    def add_class(self, name):
        if self.app_fsm.is_dataset_ready():
            self.dataset.add_class(name)

    def rename_class(self, old_name, new_name):
        if self.app_fsm.is_dataset_ready():
            self.dataset.rename_class(old_name, new_name)

    def delete_class(self, class_name):
        if self.app_fsm.is_dataset_ready():
            self.dataset.delete_class(class_name)

    def save_roi(self, frame, roi, class_name):
        if self.app_fsm.roi_selected():
            self.dataset.save_roi(frame, roi, class_name)

    # .........................................
    # Properties

    @property
    def dataset_path(self):
        return self.dataset.base_path
