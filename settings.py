class config():
    defaultTunnelSettingsFlag = True
    defaultServerSettingsFlag = True
    serverRunning = False
    def __init__(self):
        self.defaultTunnelSettings = {
        'host' : "0.0.0.0",
        'port' : 1945,
        'protocol' : "http"
        }
        self.defaultServerSettings = {
            'host' : '0.0.0.0',
            'port' : 1945
        }
        self.customedTunnelSettings = {
            'host' : "0.0.0.0",
            'port' : 0,
            'protocol' : "http"
        }
        self.customedServerSettings = {
            'host' : '0.0.0.0',
            'port' : 0
        }