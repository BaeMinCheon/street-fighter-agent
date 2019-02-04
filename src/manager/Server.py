
import socket

class Server:

    def __init__(self, _ip, _port):
        self.ip_server = _ip
        self.port_server = _port
        self.BUFSIZ = 1024
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.ip_server, self.port_server))
        self.socket_server.listen(1)
        print('===== server initialized =====')

    def Accept(self):
        print('===== server waiting client =====')
        self.socket_client, self.ip_client = self.socket_server.accept()
        print('===== server accepted client : {} ====='.format(self.ip_client))

    def Receive(self):
        try:
            self.buffer = self.socket_client.recv(self.BUFSIZ)
            self.list = []
            if self.buffer:
                self.list = self.buffer.decode('utf8').split('.')
                return True
            else:
                self.Close()
                return False
        except socket.error:
            self.Close()
            return False

    def GetList(self):
        return self.list

    def PrintList(self):
        print('p1_isLeft : {} \t gap_X : {} \t gap_Y : {} \t gap_HP_for_p1 : {} \t p1_canInputMove : {} \t p1_canInputAction : {}'.format(
               self.list[0], self.list[1], self.list[2], self.list[3], self.list[4], self.list[5]))

    def Send(self, _action):
        msg = str(_action[0]) + '.' + str(_action[1])
        self.socket_client.send(bytearray(msg, 'utf8'))

    def Close(self):
        self.socket_client.close()
        print('===== server lost client : {} ====='.format(self.ip_client))