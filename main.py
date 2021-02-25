import socketserver


def requestFor200(pathname):
    string = "HTTP/1.1 200 OK\r\nContent-Type:"
    if pathname == "/hello":
        string = string + " text/plain\r\nContent-Length: 12\r\n\r\nHello World!"
        return string
    if pathname == "/":
        string = string +  " text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nindex.html"
        return "index.html"

    if pathname == "/style.css":
        return pathname
    if pathname == "/functions.js":
        return pathname


def requestFor404(pathname):
    return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 36\r\n\r\nThe requested content does not exist"


def requestFor301(pathname):
    return "HTTP/1.1 301 Moved Permanently\r\nLocation: /hello"


class tcp(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        print(self.client_address[0] + " is sending data:")
        print(data)
        print(data.decode())

        parseData = data.decode().split('\r\n')
        header = parseData[0]

        headerLine = header.split(" ")
        request = headerLine[0]
        path = headerLine[1]
        print(path)
        print(headerLine)
        if request == "GET" and path == "/hello":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and path == "/hi":
            self.request.send(requestFor301(path).encode())
        elif request == "GET" and path == "/":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and path == "/style.css":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and path == "/functions.js":
            self.request.send(requestFor200(path))
        else:
            self.request.send(requestFor404(path).encode())


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 8000), tcp)
    server.serve_forever()
