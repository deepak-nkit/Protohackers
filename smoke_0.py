import socket
import sys

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8000
BUFFER_SIZE = 8192

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print("Binding with server is completed..")
    s.listen(5)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
    while True:
        c, addr = s.accept()
        print("Connection address from", addr)
        data = b""
        print("Receiving Data from client side \n")
        while True:
            temp  = c.recv(BUFFER_SIZE)
            if temp == b'':
                print("connectionn closed")
                break
            data += temp
            print(data)
        print("The Message:" ,data)

        c.sendall(data)
        c.shutdown(socket.SHUT_RDWR)
        c.close()
        print("connection closed waiting for new ")