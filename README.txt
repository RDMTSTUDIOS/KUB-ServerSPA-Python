SERVER Documentation

1. server

function that handles routing:
-> request;
-> get path from request;
-> look, if path is defined in routes directories
    
    - if True:
        take the whole contents from directory -> send it to client

    - if False:
        return something 404-like (page, text or etc.)

    - If we get requests from src attr:
        look up in the same directories
     


@Section(Server sys utils)
@list:
    - def prepare_server()
        - def load_config()