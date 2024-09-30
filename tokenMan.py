
import socket
import uuid
import hashlib
from cryptography.fernet import Fernet
from scapy.all import conf 


class collec_mac_ipv4():

    @staticmethod
    def get_mac():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                        for ele in range(0, 8*6, 8)][::-1])
        return mac_address
        
    @staticmethod                         
    def get_ipv4():
        hostname = socket.gethostname()
        ipv4_adress =socket.gethostbyname(hostname)
        return ipv4_adress
    
    @staticmethod
    def get_gateway():

        gateway = conf.route.route("0.0.0.0")[2]
        return gateway



class Token():
    def __init__(self, macAdress, ipv4):
        self.macAdress = macAdress
        self.ipv4 = ipv4


    def generate_token(self):
        mac_ipv4_concat = "passwrd:es2360f"+collec_mac_ipv4.get_ipv4() +collec_mac_ipv4.get_mac()
        hash_object = hashlib.sha256(mac_ipv4_concat.encode())

        hexadecimal_hash = hash_object.hexdigest()


        return hexadecimal_hash


class codeEncrypted():

    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        with open("init.key","wb") as key_file:
            key_file.write(key)
        return key
    
    @staticmethod
    def encrypt_state_code(state_code, key):
        fernet = Fernet(key)
        encrypted = fernet.encrypt(state_code.encode())
        with open("init.txt","wb") as encrypted_state_file:
            encrypted_state_file.write(encrypted)

    @staticmethod
    def decrypt_state_code(key):
        
        fernet = Fernet(key)
        with open("init.txt","rb") as encrypted_state_file:
            encypted_state_code_founded = encrypted_state_file.read()
        decrypted_code = fernet.decrypt(encypted_state_code_founded).decode()
        return decrypted_code



class stateCode():
    @staticmethod
    def generate_activated_state_code():
        from state import encrypted_state_code_key
        state_code =collec_mac_ipv4.get_gateway() +collec_mac_ipv4.get_mac() + "ActivatedStatusPassword328874k*/-"
        new_encrypted_state_code = codeEncrypted()
        key = new_encrypted_state_code.generate_key()
        encrypted_state_code_key.key = key
        new_encrypted_state_code.encrypt_state_code(state_code, key)

    @staticmethod
    def generate_blocked_state_code():
        from state import encrypted_state_code_key
        state_code =collec_mac_ipv4.get_gateway() +collec_mac_ipv4.get_mac() + "blockedlStatusPasswordtjg78//-+"
        new_encrypted_state_code = codeEncrypted()
        key = new_encrypted_state_code.generate_key()
        encrypted_state_code_key.key = key
        new_encrypted_state_code.encrypt_state_code(state_code, key)

    @staticmethod
    def generate_neutral_state_code():
        from state import encrypted_state_code_key
        state_code =collec_mac_ipv4.get_gateway() + collec_mac_ipv4.get_mac() + "neutralStatusPasswordtyubg24ll*-"
        new_encrypted_state_code = codeEncrypted()
        key = new_encrypted_state_code.generate_key()
        encrypted_state_code_key.key = key
        new_encrypted_state_code.encrypt_state_code(state_code, key)
        
