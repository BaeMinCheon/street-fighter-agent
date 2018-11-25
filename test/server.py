import socket


class Server:

    def __init__(self, _ip, _port):
        self.ip_address = _ip
        self.port_number = _port
        self.BUFSIZ = 1024
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, self.port_number))
        self.server_socket.listen(1)
        print('=====')
        print('server initialized')
        print('=====')

    def Accept(self):
        self.client_socket, self.client_address = self.server_socket.accept()
        print('=====')
        print('server accepted client : {}'.format(self.client_address))
        print('=====')

    def Receive(self):
        try:
            self.buffer = self.client_socket.recv(self.BUFSIZ)
            self.list_feature = []
            if self.buffer:
                self.list_feature = self.buffer.decode('utf8').split('.')
                return True
            else:
                raise socket.error()
        except socket.error:
            self.Close()
            return False

    def GetFeatures(self):
        return self.list_feature

    def Print(self):
        print('p1_isLeft : {} \t gap_X : {} \t gap_Y : {} \t gap_HP_for_p1 : {} \t p1_canInputMove : {} \t p1_canInputAction : {}'.format(
               self.list_feature[0], self.list_feature[1], self.list_feature[2], self.list_feature[3], self.list_feature[4], self.list_feature[5]))

    def Send(self, _action):
        msg = str(_action[0]) + '.' + str(_action[1])
        self.client_socket.send(bytearray(msg, 'utf8'))

    def Close(self):
        self.client_socket.close()
        print('=====')
        print('server lost client : {}'.format(self.client_address))
        print('=====')