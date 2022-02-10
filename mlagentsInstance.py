from subprocess import Popen, CREATE_NEW_CONSOLE

class mlagentsInstance():

    def __init__(self, configFilePath, name, port, callback):

        self.configFilePath = configFilePath
        self.name = name
        self.port

    def kill():
        p.kill()

    def start():
        self.p = Popen(f"mlagents-learn {self.configFilePath} --run-id={self.name} --base-port={self.port}",
                           creationflags=CREATE_NEW_CONSOLE)