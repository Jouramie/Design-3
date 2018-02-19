import socket

port = 7420
encoding = 'ascii'
host_ip = ''


def host_network():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))

    while True:
        server.listen(5)
        client, address = server.accept()
        print("{} connected".format(address))

        msg = "ThAnKs YoU fOr CoNnEcTiNg !!!!1\n"
        client.send(msg.encode(encoding))
        client.close()


def pair_with_host():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host_ip, port))
    msg = client.recv(1024)

    client.close()
    print(msg.decode(encoding))



