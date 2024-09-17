
import socket
import uuid
import hashlib


class collec_mac_ipv4():

    def get_mac(self):
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                        for ele in range(0, 8*6, 8)][::-1])
        return mac_address
        
                        
    def get_ipv4(self):
        hostname = socket.gethostname()
        ipv4_adress =socket.gethostbyname(hostname)
        return ipv4_adress
    



class Token():
    def __init__(self, macAdress, ipv4):
        self.macAdress = macAdress
        self.ipv4 = ipv4


    def generate_token(self):
        mac_ipv4_concat = "passwrd:es2360f"+self.macAdress + self.ipv4
        hash_object = hashlib.sha256(mac_ipv4_concat.encode())
        hexadecimal_hash = hash_object.hexdigest()
        print(hexadecimal_hash)

        return hexadecimal_hash
