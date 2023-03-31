from os.path import isfile, isdir
from os import listdir

class ClientAppDirectoryNotExist(Exception):
    def __init__(self, dir_path: str) -> None:
        super().__init__(f'Client app directory does not exist: "{dir_path}"')

class ClientAppNotExist(Exception):
    def __init__(self, dir_path: str) -> None:
        super().__init__(f'Client app "app.html" does not exist in directory: "{dir_path}"')



def verify_client_app(client_app_dir: str) -> None:
    if not isdir(client_app_dir): raise ClientAppDirectoryNotExist(client_app_dir)

    contents: list[str] = listdir(client_app_dir)
    if 'app.html' not in contents:  raise ClientAppNotExist(client_app_dir)

    return