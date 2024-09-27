import subprocess
import shutil
import os

nmap_path = os.path.join(os.path.dirname(__file__), "config", "nmap.exe")


class portScanning():

    def scan_open_ports(self, host = "localhost"):
        try:
            result = subprocess.run([nmap_path, "-p-", host], capture_output=True, text=True)
            open_ports = []
            for line in result.stdout.splitlines():
                if "open" in line:
                    port = line.split("/")[0]
                    open_ports.append(int(port))
            print("Error:", result.stderr)
            return open_ports
        except Exception as e:
            print("error: ", e)


