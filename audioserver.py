import socket, threading
clients = []
CHUNK = 4096

class forwarding(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.num = len(clients)
        clients.append(clientsocket)
        self.csocket = clientsocket
        self.addr = clientAddress
        print('New connection added: ' + str(clientAddress))
    def run(self):
        print('Connection from: ' + str(clientAddress))
        while True:
            try:
                data = self.csocket.recv(CHUNK)
            except:
                print('Client at ' + str(clientAddress) + ' disconnected...')
                break
            finally:
                for i in range(len(clients)):
                    if not i == self.num:
                        try:
                            clients[i].send(data)
IP = '0.0.0.0'
PORT = 65535
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
print('Server started on ' + str(IP) + ':' + str(PORT))
print('Waiting for client request..')
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = forwarding(clientAddress, clientsock)
    newthread.start()
