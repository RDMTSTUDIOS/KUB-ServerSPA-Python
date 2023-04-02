from sys import stdout, exit

# @description(KUB server exception base class)
# @exception


class ExceptionBaseModel(Exception):
    def __init__(self, message: str, *args: object) -> None:
        stdout.write(
            '\n \033[38;5;197m\033[48;5;237m|----------------------------|\033[0m')
        stdout.write(
            '\n \033[38;5;197m\033[48;5;237m|    KUB-Server exception    |\033[0m')
        stdout.write(
            '\n \033[38;5;197m\033[48;5;237m|----------------------------|\033[0m')
        stdout.write(
            f'\n\n Execution stop due to exception: \033[38;5;96m{type(self).__name__}\033[0m')
        stdout.write(
            f'\n Exception caused by:\n\n \033[38;5;183m\033[48;5;237m ->  {message}  \033[0m\n\n\n')
        exit(1)
