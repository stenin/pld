#!/usr/bin/env python

from socket import *
from time import ctime

HOST = ''
PORT = 21567
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

def main():

    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    tcp_server_socket.bind(ADDRESS)
    tcp_server_socket.listen(5)

    while True:
        print 'waiting for connection...'
        tcp_client_socket, address = tcp_server_socket.accept()
        print '...connected from: ', address

        while True:
            data = tcp_client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            tcp_client_socket.send('[%s] %s' % (ctime(), data))
        tcp_client_socket.close()
    tcp_server_socket.close()

if __name__ == "__main__":
    main()
