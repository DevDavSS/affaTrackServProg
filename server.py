from pyngrok import ngrok



#clases de servidores http y tcp

class server():
    def __init__(self, host, port):
        self.host = host
        self.port = port

class http_server(server):
    def __init__(self, protocol):
        self.protocol = protocol

class tcp_server():
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
