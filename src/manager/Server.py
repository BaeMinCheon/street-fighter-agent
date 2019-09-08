
import socket
import json
import os

class Server:

    def __init__(self, _ip, _port):
        self.ip_server = _ip
        self.port_server = _port
        self.buffer_size = 1024
        self.InitSocket()
        self.data = {}
        self.count_print = 0

    def InitSocket(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.ip_server, self.port_server))
        self.socket_server.listen(1)

    def Accept(self):
        try:
            self.socket_client, self.ip_client = self.socket_server.accept()
            print('> server accepted client : {}'.format(self.ip_client))
        except OSError as error:
            #print('> server failed to accept client, error:' + str(error))
            pass

    def Receive(self):
        try:
            self.buffer = self.socket_client.recv(self.buffer_size)
            if self.buffer:
                self.data = json.loads(self.buffer.decode('utf-8'))
                return True
            else:
                self.Close()
                return False
        except socket.error as error:
            #print('> server failed to receive data, error:' + str(error))
            self.Close()
            return False

    def PrintData(self):
        self.count_print += 1
        if self.count_print == 30:
            self.count_print = 0
            log = ''
            for i in self.data:
                log += i + ' = ' + str(self.data[i]) + '    /    '
            os.system('cls')
            print(log)

    def Send(self, _action = [0, 0, 0]):
        try:
            data = {'Move': _action[0], 'Action': _action[1], 'Control': _action[2]}
            self.socket_client.send(json.dumps(data).encode('utf-8'))
        except AttributeError as error:
            #print('> server failed to send data, error:' + str(error))
            pass

    def Close(self):
        print('Server.Close()')
        try:
            self.socket_client.close()
            del self.socket_client
            print('> server lost client : {}'.format(self.ip_client))
        except AttributeError as error:
            #print('> server failed to close socket, error:' + str(error))
            self.socket_server.close()
            self.InitSocket()