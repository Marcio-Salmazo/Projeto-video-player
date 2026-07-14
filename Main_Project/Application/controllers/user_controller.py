from Main_Project.Application.models.fsm.app_fsm import ApplicationFSM
from Main_Project.Application.services.user_services import UserServices


class UserController:

    def __init__(self):

        self.user_services = UserServices()
        self.app_fsm = ApplicationFSM()
        self.current_user = None

    def login(self, username, password):

        # Chamada da função responsável por autenticar os dados
        # passados pelo usuário, ao realizar o login
        user = self.user_services.authenticate(username, password)

        # Caso exista uma correspondência, a função authenticate retorna
        # o objeto do usuário, de modo que seja possível obter suas atribuições
        if user:
            self.current_user = user
            return True
        return False

    # Getters das atribuições do usuário
    @property
    def role(self):
        return self.current_user.role

    @property
    def username(self):
        return self.current_user.username
