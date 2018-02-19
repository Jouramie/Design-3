import socket


class NetworkController:

    def __init__(self, port, encoding='ascii'):
        self.port = port
        self.encoding = encoding

    def host_network(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', self.port))

        while True:
            server.listen(5)
            client, address = server.accept()
            print("{} connected".format(address))

            msg = "ThAnKs YoU fOr CoNnEcTiNg !!!!1\n"
            client.send(msg.encode(self.encoding))
            client.close()

    def pair_with_host(self, host_ip):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host_ip, self.port))
        msg = client.recv(1024)

        client.close()
        print(msg.decode(self.encoding))
