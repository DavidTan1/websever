import socketserver


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
            self.request.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 12\r\n\r\nHello World!".encode())
        elif request == "GET" and path == "/hi":
            self.request.send("HTTP/1.1 301 Moved Permanently\r\nLocation: /hello".encode())
        else:
            self.request.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 36\r\n\r\nThe requested content does not exist".encode())


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 8000), tcp)
    server.serve_forever()
