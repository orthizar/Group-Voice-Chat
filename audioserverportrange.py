import socket, threading, sys
servers = []
users = []
clients = []
count = []
CHUNK = 4096
if len(sys.argv) > 1:
    IP = sys.argv[1]
    portmin = sys.argv[2]
    portmax = sys.argv[3]
else:
    IP = '0.0.0.0'
    portmin = 65000
    portmax = 65535
actport = portmin
class clientforwarding(threading.Thread):
    def __init__(self, server, port, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        print("OK")
        global count
        global clients
        self.port = port
        self.server = server
        self.num = count[self.server]
        count[self.server] += 1
        clients[self.server].append(clientsocket)
        self.csocket = clientsocket
        self.addr = clientAddress
    def run(self):
        global count
        global users
        global CHUNK
        print('Client at ' + str(self.addr) + ' connected to ' + str(self.port))
        users[self.server] += 1
        try:
            while True:
                try:
                    data = self.csocket.recv(CHUNK)
                except:
                    print('Client at ' + str(self.addr) + ' disconnected...')
                    clients[self.server].remove(clients[self.server][self.num])
                    count[self.server] -= 1
                    users[self.server] -= 1
                    break
                finally:
                    for i in range(len(clients)):
                        if not i == self.num:
                            try:
                                clients[self.server][i].send(data)
                            except:
                                pass
        except:
            pass
class server(threading.Thread):
    def __init__(self, port, servernum):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((IP, port))
        self.servernum = servernum
        self.ip = IP
        self.port = port
        print(str(self.ip) + ':' + str(self.port) + ' started...')
    def run(self):
        while True:
            self.server.listen(1)
            clientsock, clientAddress = self.server.accept()
            newthread = clientforwarding(self.servernum, self.port, clientAddress, clientsock)
            newthread.start()
        
for i in range(portmax - portmin + 1):
    count.append(0)
    users.append(0)
    clients.append([])
    try:
        servers.append(server(int(actport), i))
        servers[i].start()
    except:
        pass
    actport += 1
