from os.path import isfile



def create_request_handler(client_app_directory: str):
    def handle_request(request: list[str, str]) -> str | None:
        if '.' in request:
            try:
                with open(f'{client_app_directory}{request}') as file:
                    return file.read()
            except:
                return None
        else:
            with open (f"{client_app_directory}/app.html") as file:
                return file.read()

    return handle_request