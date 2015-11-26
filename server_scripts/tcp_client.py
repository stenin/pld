#!/usr/bin/env python

from socket import *

HOST = 'localhost'
PORT = 21567
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

def main():

    tcp_client_socket = socket(AF_INET, SOCK_STREAM)
    tcp_client_socket.connect(ADDRESS)

    while True:
        data = raw_input('>')
        if not data:
            break
        tcp_client_socket.send(data)
        data = tcp_client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        print data

    tcp_client_socket.close()


if __name__ == "__main__":
    main()
