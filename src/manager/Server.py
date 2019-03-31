
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
        log = ''
        for i in self.data:
            log += i + ' : ' + str(self.data[i]) + ', '
        print(log)

    def Send(self, _move, _action, _control = 0):
        data = {'key_move': _move, 'key_action': _action, 'key_control': _control}
        self.socket_client.send(json.dumps(data).encode('utf-8'))

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