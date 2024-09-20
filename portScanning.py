import subprocess


class portScanning():

    def scan_open_ports(self, host = "localhost"):
        result = subprocess.run(["nmap", "-p-", host], capture_output=True, text=True)
        print(result)
        open_ports = []
        for line in result.stdout.splitlines():
            if "open" in line:
                port = line.split("/")[0]
                open_ports.append(int(port))
        return open_ports


