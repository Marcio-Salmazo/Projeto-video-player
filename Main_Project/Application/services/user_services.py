import json
from Main_Project.Application.models.dataClasses.user_model import UserModel
from Main_Project.Application.models.fsm.user_role import UserRole


class UserServices:

    def __init__(self):

        # Logo na inicialização, o script faz a leitura dos usuários cadastrados
        # no arquivo JSON padrão localizado em "resources/users.json"
        with open("Main_Project/Application/resources/users.json", "r") as file:
            data = json.load(file)

        # Cria a lista inicial dos usuários (Vazia)
        self.users = []

        # Popula a lista criada préviamente com os dados lidos no arquivo JSON
        # Utiliza o modelo do DataClass para formatar os dados obtidos, formando um objeto padronizado.
        for user in data:
            self.users.append(

                UserModel(
                    username=user["username"],
                    password=user["password"],
                    role=UserRole(user["role"])
                )
            )

    def authenticate(self, username, password):

        # Função responsável por comparar os dados de entrada do login com
        # os usuários cadastrados no arquivo users.json
        for user in self.users:

            # Caso haja uma correspondência, o usuário é retornado
            if user.username == username and user.password == password:
                return user

        return None
