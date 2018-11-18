import socket

ip_address = '127.0.0.1'
port_number = 7000
BUFFER_SIZE = 1024

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((ip_address, port_number))
ss.listen(1)

while True:
    print('server starts...')
    cs, addr = ss.accept()
    print('connected to {}'.format(addr))

    while True:
        try:
            buffer = cs.recv(BUFFER_SIZE)
            if buffer:
                print('received data : {}'.format(buffer))
                cs.send(bytearray('ACK !', 'utf-8'))
            else:
                print('disconnected to {}'.format(addr))
                break
        except:
            print('disconnected to {}'.format(addr))
            break

    print('server shuts down...')
    cs.close()
