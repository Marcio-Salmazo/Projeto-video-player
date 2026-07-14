from Main_Project.Application.models.fsm.app_fsm import ApplicationFSM
from Main_Project.Application.services.user_manager import UserManager


class UserController:

    def __init__(self):

        self.user_manager = UserManager()
        self.app_fsm = ApplicationFSM()
        self.current_user = None

    def login(self, username, password):
        user = self.user_manager.authenticate(username, password)

        if user:
            self.current_user = user
            return True
        return False

    @property
    def role(self):
        return self.current_user.role

    @property
    def username(self):
        return self.current_user.username
