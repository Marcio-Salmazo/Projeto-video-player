from ..models.fsm.video_fsm import VideoFSM
from ..models.fsm.app_fsm import ApplicationFSM


# Controlador principal da aplicação, responsável por delegar as responsabilidades aos
# modulos específicos. Quem usa a aplicação (por exemplo, a GUI) conversa apenas com ApplicationController.
class UserController:

    # DEFINIR ESTADOS

    def __init__(self):
        self.app_fsm = ApplicationFSM()
        self.video_fsm = VideoFSM()
