"""
    O script tem a responsabilidade apenas de
    ler os usuários do JSON
"""

import json
from Main_Project.Application.models.dataClasses.user_model import UserModel
from Main_Project.Application.models.fsm.user_role import UserRole


class UserManager:

    def __init__(self):

        with open("Main_Project/Application/resources/users.json", "r") as file:

            data = json.load(file)

        self.users = []

        for user in data:
            self.users.append(

                UserModel(
                    username=user["username"],
                    password=user["password"],
                    role=UserRole(user["role"])
                )
            )

    def authenticate(self, username, password):

        for user in self.users:

            if (
                    user.username == username
                    and
                    user.password == password
            ):
                return user

        return None
