
import socket
import json

class Server:

    def __init__(self, _ip, _port):
        self.ip_server = _ip
        self.port_server = _port
        self.BUFSIZ = 1024
        self.InitSocket()
        self.data = {}

    def InitSocket(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.ip_server, self.port_server))
        self.socket_server.listen(1)

    def Accept(self):
        print('Server.Accept()')
        try:
            self.socket_client, self.ip_client = self.socket_server.accept()
            print('> server accepted client : {}'.format(self.ip_client))
        except OSError:
            pass

    def Receive(self):
        try:
            self.buffer = self.socket_client.recv(self.BUFSIZ)
            if self.buffer:
                self.data = json.loads(self.buffer.decode('utf-8'))
                return True
            else:
                self.Close()
                return False
        except socket.error:
            self.Close()
            return False

    def GetData(self):
        return self.data

    def PrintData(self):
        for i in self.data:
            print(i, ' : ', self.data[i])

    def Send(self, _action):
        msg = str(_action[0]) + '.' + str(_action[1])
        self.socket_client.send(bytearray(msg, 'utf8'))

    def Close(self):
        print('Server.Close()')
        try:
            self.socket_client.close()
            del self.socket_client
            print('> server lost client : {}'.format(self.ip_client))
        except AttributeError:
            self.socket_server.close()
            print('> server cancelled accept')
            self.InitSocket()