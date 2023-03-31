## Creating server

Server - is an object of KUBServer class.

Creating new server starts with creating instance of KUBServer

Then configure_server_socket function is called. It sets server-essential properties from configurational file.

`test_server` function initiates server testing for its proper work.

## Starting server

When object is created, `start_server` function is called. It will start its own function withit to handle proper network data transfer


## Sockets serving

Main server socket is listening new connections. It will delegate message serving for list of other sockets to other *thread server sockets*.


list_of_sockets is searched for ready for reading:

    server socket -> accept new connection
    else :: client socket -> read data
    data is parsed 


### Storing sockets

Sockets stored by their fileno() function call returned value - t's file descriptor.
It 100 percent unique due to socket exitance in client_connections, cause it's their file identifiers assigned by OS. When connection is closed - socket fileno is not used anymore, so it can be assigned to any other socket and it is still quaranteed unique.

sockets list - holds all socket connections to execute different operations within server cycle:

- ease to add
- ease to iterate
- ease to get
- ease to delete


message buffer - holds messages by different sockets by their fileno.

- ease to add
- ease to get
- ease to delete


when socket is now unreadble - procced it's request and send back responce
after that - remove socket from clients and close it

### Client socket serving staging

1. Accept connection
2. Read data
3. When socket is now not readable -> socket also writable -> send data --after all data sended--> close socket
4. This socket now is not a server client, because it received all needed data

### Messages handling

Route is delegated to route handler as a string

Route searches client application directory.

Router considers routes which are type of client app (example: /, /about, /main) as app routes and sends client application back to the client.

If request considered as an app data, like .js .css and etc - sends back request file if it exists.

Server has it's own data structures for different requests, like post and etc

Server also can be managed by creating rule-lists, which can handle specific situations