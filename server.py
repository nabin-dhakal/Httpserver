import socket
from routes import routes
from middlewares import logging_middleware, timing_middleware

class Request:
    def __init__(self,method,path,version,headers):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers

def applymiddleware(request,handler, middlewares):
    next_fun = handler
    
    for middleware in reversed(middlewares):
        next_fun = lambda req, n = next_fun: middleware(req, n)

    return next_fun(request)    


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind(("0.0.0.0",8080))

server_socket.listen(1)


while True:
    client_socket , client_address = server_socket.accept()
    print(f"connection from {client_address}")

    headers = {}
    data = client_socket.recv(1024)


    request_text = data.decode()

    lines = request_text.split("\r\n")

    request_line = lines[0]

    parts = request_line.split(" ")

    for i in range(1, len(lines)):
        line = lines[i]

        if line == "":
            break

        part = line.split(": ")

        headers[part[0]] = part[1]


    request = Request(parts[0],parts[1], parts[2], headers)

    if request.path in routes:
        handler_function = routes[request.path]
        middlewares = [logging_middleware, timing_middleware]
        body = applymiddleware(request, handler_function, middlewares)
        response = f"HTTP/1.1 200 OK \r\n\r\n{body}"
    else:
        response = "HTTP/1.1 404 NOT FOUND \r\n\r\n 404 - Page Not Found"

    client_socket.send(response.encode())

    client_socket.close()
