
def create_request_handler(client_app_directory: str, doc_name: str):

    def create_responce_OK(data: str) -> bytes:
        return f'HTTP/1.1 200 OK\n\n{data}'.encode()
    
    def create_responce_NOT_FOUND() -> bytes:
        return f'HTTP/1.1 403 RESOURCE NOT FOUND\n\n'.encode()
    
    def create_responce_EXCEPTION() -> bytes:
        return f'HTTP/1.1 403\n\n'.encode()

    # Handle client raw request.
    # @responsibilities(
    #   Handle raw-client-request
    #   Return client-responce back to server socket to send back
    # )
    # @description(
    #   Recognizes client request and reads all possible valuable data from it.
    #   returns a responce to send
    # )
    #
    def handle_request(request: list[bytes]) -> bytes:

        # Client request converted to a readable form as a string.
        client_data: str = b''.join(request).decode().split('\r\n')[:-2]
        # Request method
        method: str = client_data[0].split(' ', 2)
        # Request body(data)
        body: dict[str, str] = dict()
        for line in client_data[1:]:
            key, value = line.split(': ', 1)
            body[key] = value
        
        to_send: str | None = None

        # # Send document
        if (body.get('Sec-Fetch-Dest', '') == 'document') and (body.get('Sec-Fetch-Site', '') == 'none'):
            to_send = f'{client_app_directory}/{doc_name}'
        
        # # Send resource
        elif (not not body.get('Referer', '')) and (not not body.get('Sec-Fetch-Site', None)):
            to_send = f'{client_app_directory}{method[1]}'

        print(to_send)

        if not to_send:
            return create_responce_NOT_FOUND()
        
        try:
            with open(to_send) as file:
                return create_responce_OK(file.read())
        except:
            return create_responce_EXCEPTION()



    return handle_request