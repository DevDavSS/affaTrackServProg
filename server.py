from pyngrok import ngrok
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse


#clases de servidores http y tcp

class server():
    def __init__(self, host, port):
        self.host = host
        self.port = port


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Servidor en funcionamiento")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")

    def do_POST(self):
        if self.path.startswith('/coordenadas'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            print(f"Coordenadas recibidas: {post_data}")

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Mensaje recibido")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")
    

class HTTPServerWrapper:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        server_address = (self.host, self.port)
        httpd = HTTPServer(server_address, RequestHandler)
        print(f"Servidor HTTP corriendo en {self.host}:{self.port}")
        httpd.serve_forever()
    

class HTTPServerWrapper:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        server_address = (self.host, self.port)
        httpd = HTTPServer(server_address, RequestHandler)
        print(f"Servidor HTTP corriendo en {self.host}:{self.port}")
        httpd.serve_forever()

        


class tcp_server(server):
    def __init__(self, protocol):
        self.protocol = protocol



#creacion y ejecucion de tuneles usando ngrok

class tunnel():
    def __init__(self, host, port):
        self.host = host
        self.port = port


class http_tunnel(tunnel):

    def __init__(self,host,port, protocol):
        super().__init__(host, port)
        self.protocol = protocol



    def start_http_tunnel(self):

        http_tunel = ngrok.connect(self.port, self.protocol)
        url = http_tunel.public_url
        return url, http_tunel

    def stop_http_tunnel(self, http_tunel):
        ngrok.disconnect(http_tunel.public_url)

        """
        input("enter para cerrar el tunel...")
        ngrok.disconnect(http_tunel.public_url)"""




#no valido hasta obtener protocolos TCP incluido en token de ngrok
"""
class tcp_tunnel(tunnel):

    def __init__(self, protocol):
        self.protocol

    def __init__(self,host,port, protocol):
        super().__init__(host, port)
        self.protocol = protocol



    def start_tcp_tunnel(self):
        tcp_tunel = ngrok.connect(self.port, self.protocol)
        print("URL generada", http_tunel.public_url)
        input("enter para cerrar el tunel...")
        ngrok.disconnect(http_tunel.public_url)

"""
