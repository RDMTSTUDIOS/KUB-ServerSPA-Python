from inspect import currentframe

# Jadegreen - \033[38;5;36
# Burgundy - \033[48;2;128;0;32m
# Light green - [48;5;49
# 

class klog:

    def __init__(self) -> None:
        raise Exception('Can not create instance of KUBMessage object class.')

    def status(message: str) -> None:
        print('(KUBServer) status: ' + message)

    def warning(message: str) -> None:
        print('(KUBServer) Warning: ' + message)

    def devprint(message: str) -> None:
        print(
            f'\033[1;36m(KUB :: {currentframe().f_back.f_code.co_name}\033[0m) msg: \033[38;5;36m {message} \033[0m')

    def statuslog(message: str) -> None:
        print(f'\033[2;38;5;36m{message}\033[0m')

    def alert(message: str) -> None:
        print(f'\x1b[5m WARN \x1b[25m')

    def event(message: str) -> None:
        print(
            f'\033[38;5;36mKUBEvent:\033[0m |\033[48;5;55m\033[38;5;153m {message} \033[0m|')
