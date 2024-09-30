import nmap


class portScanning:

    def scan_open_ports(self, host="localhost"):
        try:
            nm = nmap.PortScanner()

            nm.scan('127.0.0.1', '1-65535', arguments="-T4")
            
            open_ports = []

            if '127.0.0.1' in nm.all_hosts():
                for proto in nm['127.0.0.1'].all_protocols():
                    lport = nm['127.0.0.1'][proto].keys()
                    for port in lport:
                        if nm['127.0.0.1'][proto][port]['state'] == 'open':
                            open_ports.append(port)
            else:
                print(f"No hosts found for {host}")
            
            return open_ports
        except Exception as e:
            print("Error: ", e)