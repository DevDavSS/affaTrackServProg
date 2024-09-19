from pyngrok import ngrok
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from shared import printCoordenatesInterface
import threading

#clases de servidores http y tcp

class server():
    def __init__(self, host, port):
        self.host = host
        self.port = port


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, widget, *args, **kwargs):
        self.widget = widget
        super().__init__(*args, **kwargs)


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

        def printCordInterFunc(post_data):
            printCoordenatesInterface(post_data, self.widget)
        
        if self.path.startswith('/coordenadas'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            print(f"Coordenadas recibidas: {post_data}")

            printCordsMangerThread = threading.Thread(target=printCordInterFunc, args=(post_data,))
            printCordsMangerThread.start()

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
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

        self.httpd = None  

    def run(self, widget):
        server_address = (self.host, self.port)
        self.httpd = HTTPServer(server_address, lambda *args, **kwargs: RequestHandler(widget, *args, **kwargs))
        print(f"Servidor HTTP corriendo en {self.host}:{self.port}")
        
        try:
            self.httpd.serve_forever()  # Start the server
        except Exception as e:
            print(f"Error while running the server: {e}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()  # shutdown the serverr
            self.httpd.server_close()  # close the server
            print("Servidor HTTP cerrado")
        else:
            print("No existe httpd")


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
