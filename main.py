import socketserver
import codecs


def setUpTemplate(map, html):
    if "{{loop}}" in html:
        newhtml = html.replace("{{loop}}", "arandomStringUseToSPLIT{{loop}}")
        updatehtml = newhtml.replace("{{end_loop}}", "{{end_loop}}arandomStringUseToSPLIT")
        htmlarr = updatehtml.split("arandomStringUseToSPLIT")
        for x in htmlarr:
            if "{{loop}}" in x:
                x1 = x.replace("{{loop}}", "")
                x2 = x1.replace("{{end_loop}}", "")
                x3 = x2.replace("{{", "")
                x4 = x3.replace("}}", "")

                for y in map.keys():
                    if y in x4:
                        arr = x4.split("=")
                        imagearr = map[y].split('+')  # get all the content
                        img = ""
                        for z in imagearr:

                            stry = str(y)
                            newy = stry.replace('s','')
                            img = img + arr[0] + '="/' + newy + '/' + z + '.jpg"'+"/>"+'\r\n'
                            print(img)
                        html = html.replace(x, img)

    for key in map.keys():
        html = html.replace("{{" + key + "}}", map[key])  # replace placeholder with key value
    #print(html)
    return html


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
            count += 1
        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + str(
            count) + "\r\nX-Content-Type-Options: nosniff\r\n\r\n" + htmlcontent

    if pathname == "/style.css":
        css = codecs.open("style.css", 'r')
        csscontent = css.read()
        count = 0
        for x in csscontent:
            print(x.encode())
            count += 1
        return "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: " + str(
            count) + "\r\nX-Content-Type-Options: nosniff\r\n\r\n" + csscontent

    if pathname == "/functions.js":
        js = codecs.open("functions.js", 'r')
        jscontent = js.read()
        count = 0
        for x in jscontent:
            print(x.encode())
            count += 1
        return "HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\nContent-Length: " + str(
            count) + "\r\nX-Content-Type-Options: nosniff\r\n\r\n" + jscontent

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
        return "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: " + str(
            count) + "\r\nX-Content-Type-Options: nosniff\r\n\r\n" + utfcontent

    if "/image/" in pathname:
        patharr = pathname.split('/')
        imgcontent = open('image/' + patharr[2], 'rb').read()
        count = 0
        for x in imgcontent:
            print(x)
            count += 1
        return ("HTTP/1.1 200 OK\r\nContent-Type: image/jpeg; charset=utf-8\r\nContent-Length: " + str(
            count) + "\r\nX-Content-Type-Options: nosniff\r\n\r\n").encode() + imgcontent

    if "/images" in pathname:
        map = {}
        patharr = pathname.split('?')
        html = codecs.open("HTMLtemplate.html", 'r').read()
        brokenupqueryString = patharr[1].split('&')
        print(brokenupqueryString)
        for x in brokenupqueryString:
            keyandvalue = x.split('=')
            map.update({keyandvalue[0]: keyandvalue[1]})

        updatedhtml = setUpTemplate(map, html)
        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + str(
            len(updatedhtml)) + "\r\nX-Content-Type-Options: nosniff\r\n\r\n" + updatedhtml


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
        header = parseData[0]  # the header
        headerLine = header.split(" ")

        request = headerLine[0]  # GET or POST request

        path = headerLine[1]  # the path

        paths = path.split("?")  # split the path to check for query string
        # path is the first index
        # the query string is the 2nd index

        if request == "GET" and paths[0] == "/hello":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and paths[0] == "/hi":
            self.request.send(requestFor301(path).encode())
        elif request == "GET" and paths[0] == "/":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and paths[0] == "/style.css":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and paths[0] == "/functions.js":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and paths[0] == "/utf.txt":
            self.request.send(requestFor200(path).encode())
        elif request == "GET" and "/image/" in paths[0]:
            self.request.send(requestFor200(path))
        elif request == "GET" and "/images" == paths[0]:
            self.request.send(requestFor200(path).encode())
        else:
            self.request.send(requestFor404(path).encode())


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 8000), tcp)
    server.serve_forever()
