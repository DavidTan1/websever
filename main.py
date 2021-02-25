import socketserver
import codecs


def requestFor200(pathname):
    string = "HTTP/1.1 200 OK\r\nContent-Type:"
    if pathname == "/hello":
        string = string + " text/plain\r\nContent-Length: 12\r\n\r\nHello World!"
        return string
    if pathname == "/":
        html = codecs.open("index.html", 'r')
        htmlcontent = html.read()
        count = 0
        for x in htmlcontent:
            print(x.encode())
            count+=1
        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: "+str(count)+"\r\nX-Content-Type-Options: nosniff\r\n\r\n"+htmlcontent

    if pathname == "/style.css":

        css = codecs.open("style.css", 'r')
        csscontent = css.read()
        count = 0
        for x in csscontent:
            print(x.encode())
            count+=1

        return "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: "+str(count)+"\r\nX-Content-Type-Options: nosniff\r\n\r\n"+csscontent

    if pathname == "/functions.js":
        js = codecs.open("functions.js", 'r')
        jscontent = js.read()
        count = 0
        for x in jscontent:
            print(x.encode())
            count += 1
        return "HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\nContent-Length: "+str(count)+"\r\nX-Content-Type-Options: nosniff\r\n\r\n"+jscontent

    if pathname == "/utf.txt":
        utf = codecs.open("utf.txt", 'r', encoding="utf-8")
        utfcontent = utf.read()
        count = 0
        for x in utfcontent:
            btyearr = str(x.encode()).split("\\")

            for y in btyearr:
                if y != "b'":
                    count += 1
        print(count)
        return "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: "+str(count)+"\r\nX-Content-Type-Options: nosniff\r\n\r\n"+utfcontent


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
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and path == "/utf.txt":
            self.request.send(requestFor200(path).encode())
        else:
            self.request.send(requestFor404(path).encode())


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 8000), tcp)
    server.serve_forever()
