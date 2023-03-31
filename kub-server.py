from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from sys import exit

from src.helpers.config_loader import server_config_loader
from src.server_cli.messages import klog
from src.helpers.verify_client_app import verify_client_app
from src.helpers.request_handler import create_request_handler

class KUBServer:

    def __init__(self) -> None:

        server_config = server_config_loader()
        self.__port = server_config.get('PORT')
        self.__host = server_config.get('HOST')
        self.__receive_buffer_size = server_config.get('RECV_BUFFER_SIZE', 2048)
        self.__client_app_directory = server_config.get('CLIENT_APP_DIRECTORY', './client_spa_app')
        self.__verify()

        self.__handler = create_request_handler(self.__client_app_directory)
        
        return


    def __verify(self) -> None:
        verify_client_app(self.__client_app_directory)
        return


    def __setup_server_socket(self, server_socket: socket) -> None:
        
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((self.__host, self.__port))
        server_socket.setblocking(False)
        return

    
    def run_server(self) -> None:

        SERVER_SOCKET: socket = socket()
        self.__setup_server_socket(SERVER_SOCKET)


        bfs = self.__receive_buffer_size
        cldr = self.__client_app_directory


        CLIENT_SOCKETS: dict[socket, socket] = dict()
        CLIENT_SOCKETS[SERVER_SOCKET] = SERVER_SOCKET

        MESSAGE_BUFFER: dict[socket, list[bytes]] = dict()
        WAITING_SOCKETS: dict[socket, socket] = dict()
        STARTED_TRANSFER: dict[socket, True] = dict()


        SERVER_SOCKET.listen(5)
        klog.devprint(f'KUBServer started.\nhttp://{self.__host}:{self.__port}\n')

        while True:
            
            try: READABLE, WRITEABLE, EXCEPTIONAL = select(CLIENT_SOCKETS.keys(), WAITING_SOCKETS.keys(), CLIENT_SOCKETS.keys())
            except KeyboardInterrupt: exit()
            except:
                for client_socket in CLIENT_SOCKETS:
                    if client_socket.fileno() < 0:
                        del CLIENT_SOCKETS[client_socket]
                        break
                continue

            TRANSFERING: dict[socket, True] = dict()

            for opened_socket in READABLE:
                if opened_socket is SERVER_SOCKET:
                    new_client, _ = opened_socket.accept()
                    new_client.setblocking(False)

                    CLIENT_SOCKETS[new_client] = new_client
                    MESSAGE_BUFFER[new_client] = list()
                    WAITING_SOCKETS[new_client] = new_client
                    TRANSFERING[new_client] = True

                    klog.statuslog(f'New user "{new_client.fileno()}" connected')
                    continue


                BUFFER: bytes = opened_socket.recv(bfs)
                STARTED_TRANSFER[opened_socket] = True

                if not BUFFER:
                    del CLIENT_SOCKETS[opened_socket]
                    del MESSAGE_BUFFER[opened_socket]
                    del WAITING_SOCKETS[opened_socket]
                    if STARTED_TRANSFER.get(opened_socket, None):
                        del STARTED_TRANSFER[opened_socket]

                    klog.statuslog(f'User "{opened_socket.fileno()}" disconnected')
                    continue

                TRANSFERING[opened_socket] = True
                MESSAGE_BUFFER[opened_socket].append(BUFFER)

            for waiting_socket in WRITEABLE:

                if not TRANSFERING.get(waiting_socket, None) and STARTED_TRANSFER.get(waiting_socket, None):
                    request_was = b''.join(MESSAGE_BUFFER[waiting_socket]).decode().split(' ', 2)[:2]
                    klog.status(str(request_was))
                    data = self.__handler(request_was[1])
                    responce = b''
                    if not data: responce = b"HTTP/1.1 401 OK\r\n\r\n\rHuiy\n"
                    else: responce = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{data}'.encode()
                    waiting_socket.send(responce)
                
                    del CLIENT_SOCKETS[waiting_socket]
                    del WAITING_SOCKETS[waiting_socket]
                    del MESSAGE_BUFFER[waiting_socket]
                    del STARTED_TRANSFER[waiting_socket]

                    klog.statuslog(f'Message sent to "{waiting_socket.fileno()}" user. User closed')
                    waiting_socket.close()



KUBServer().run_server()