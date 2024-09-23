import  os
import tkinter as tk
import tokenMan
from tokenMan import collec_mac_ipv4, codeEncrypted, stateCode
from tkinter import *
from interfaces import mainInterface
import sys
from tkinter import Entry, Button
import threading
from main import defined_state_codes

class encrypted_state_code_key():
    @staticmethod
    def load_key():
        return open("init.key","rb").read()


def decrypt_state_code_validation(key):
    new_decrypted_state_code = codeEncrypted.decrypt_state_code(key)
    return new_decrypted_state_code



class activation_interface():
    def __init__(self):
        self.chances = 0  

    def run_activation_interface(self):
        mac_collector = collec_mac_ipv4()  
        ipv4_collector = collec_mac_ipv4()

            
        def get_identifiers(newMAc=mac_collector, newIpv4=ipv4_collector):
            identifiers = {'Mac': newMAc, 'ipv4': newIpv4}
            return identifiers

        def compare_tokens(token):
            userToken = self.tokenEntry.get()  

           
            if userToken == token:

                activP = programState()
                activationThread = threading.Thread(target=activP.activatedProgram)
                activationThread.start()
                print("validado con exito")
                activWind.destroy()
                new_main_interface = mainInterface()
                new_main_interface.run_main_interface()
            else:
                self.chances += 1
                print(f"Token no válido. Intento {self.chances}/5")
      
                self.errorLabel.config(text=f"Token no válido. Intentos restantes: {5 - self.chances}")
                self.tokenEntry.delete(0, tk.END)  

          
                if self.chances >= 3:
                    blockP = programState()
                    blockP.blockProgram()
                    sys.exit()

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
                         font=("Helvetica", 40, "bold"),
                         anchor="center"
                         ).pack(side="top", fill="both", anchor="n", pady=10)

        instructionsLabel1 = tk.Label(activWind,
                                      text="Enter the provided activation Token to start",
                                      bg="black",
                                      fg="white",
                                      font=20,
                                      anchor="center",
                                      ).pack(fill="both", anchor="n", pady=20)

        self.tokenEntry = Entry(activWind, width=40)  
        self.tokenEntry.pack(anchor="n", pady=20)

        activateButton = Button(activWind,
                                text="Activate",
                                width=20,
                                bg="#999595", fg="black",
                                command=lambda: compare_tokens(token)
                                ).pack(pady=50)

        exitButton = Button(activWind, text="Exit", width=20, bg="#999595", fg="black", command=closeProgram).pack(pady=20)


        self.errorLabel = tk.Label(activWind, text="", bg="black", fg="red", font=16) 
        self.errorLabel.pack(anchor="n", pady=10)
        self.ipv4Widget = Label(activWind, 
            text=ipv4_collector.get_ipv4(),
             bg="black", fg="green", font=10
            ).pack()
        self.macWidget = Label(activWind, 
            text=mac_collector.get_mac(),
            bg="black", fg="green", font=10
            ).pack()
        activWind.mainloop()


class programState():

    def checkProgramStateExists(self):
        with open("init.txt", "r") as f:
            code = f.read().split()
        return code

    def blockProgram(self):
        print("The program is blocked")
        new_encrypted_state_code_file = stateCode.generate_blocked_state_code()

    def activatedProgram(self):
        print("program activated")
        new_encrypted_state_code_file = stateCode.generate_activated_state_code()

    def neutralProgram(self):
        new_encrypted_state_code_file = stateCode.generate_neutral_state_code()
    

    def verifyState(self):
        
        if not os.path.exists("init.txt"):
      
            return False
        elif os.path.exists("init.txt") and not self.checkProgramStateExists():
            stateCode.generate_neutral_state_code()
            self.verifyState()

        else:
        
            state = decrypt_state_code_validation(encrypted_state_code_key.load_key())
            return state

            

