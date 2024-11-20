import math
import socket
import json
import threading

def is_prime(num):
    if not isinstance(num , int) or num < 2:
        return False
    for i in range(2 , int(math.sqrt(num) + 1)):
        if num % i == 0:
            return False
    return True


def handle_client(conn , addr):
        wrong_data = False
        print(f"connected by {addr}")
        data = ""
        while not wrong_data:
            msg = conn.recv(1024)
            if not msg:
                break
            data+= msg.decode('utf-8')

            # req_data  = data.decode("UTF-8").strip()
            print("---------Whole data: ", data)
            while '\n' in data:
                end = data.index('\n')
                req_data = data[:end]
                data = data[end + 1:]
                print("---------Remaining data: ", data)

                try:
                    # requests = req_data.split("\n")
                    # for request in requests:
                    req = json.loads(req_data.strip())
                    print("~~~~~~~req: ", req)
                    if req.get('method') != 'isPrime' or 'number' not in req:
                        raise ValueError ("Malformed request")
                    num = req.get("number")
                    if not (type(num) == int or type(num) == float):
                        print("**************************")
                        raise ValueError ("malformed request")
                    response = {
                        "method": "isPrime",
                        "prime": is_prime(num) 
                        }

                    sending_data = (json.dumps(response) + "\n").encode('utf-8')
                    print("********* Sending data: ", sending_data)
                    conn.sendall(sending_data)
                    print("*****completed sending data ")

                except (ValueError):
                    malformed_response = {
                        "method": "isPrime",
                        "prime": "malformed request"
                    }
                    print("********* Sending  malformed data: " , malformed_response)
                    conn.sendall(("{}lkjsadkfjsajf"+ "\n").encode('utf-8'))
                    print("****completed sending data ")
                    wrong_data = True
                    break
        conn.shutdown(socket.SHUT_RDWR)                
        conn.close()
    
def start_server(SERVER_IP = "0.0.0.0",SERVER_PORT = 1672):
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        
        print(f"Trying to listen on {SERVER_IP}:{SERVER_PORT}")
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(5)
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
        try:
            while True:
                conn , addr = s.accept()
                print("Connection address from", addr)
                thread = threading.Thread(target = handle_client, args = (conn , addr)).start() 
        except KeyboardInterrupt:
            print("Shutdown the server")        
        finally:
            s.close()

if __name__ == "__main__":
    start_server() 











# import socket
# import json
# import threading

# def is_prime(num):
#     if not isinstance(num , int) or num < 2:
#         return False
#     for i in range(2 , (num//2) + 1):
#         if num % i == 0:
#             return False
#     return True

# def handle_client(conn , addr):
#         print(f"connected by {addr}")
#         data = b''
#         while True:
#             while True:
#                 msg = conn.recv(1024)
#                 print("^^^^^^^receives part of msg: ",msg)
#                 if not msg:
#                     break
#                 data += msg
#                 if b'}' in msg:
#                     break
#             req_data  = data.decode("UTF-8").strip()
#             print("---------Whole data: ", req_data)
#             try:
#                 requests = req_data.split("\n")
#                 for request in requests:
#                     req = json.loads(request)
#                     print("~~~~~~~req: ", req)
#                     if req.get('method') != 'isPrime' or 'number' not in req:
#                         raise ValueError ("Malformed request")
#                     num = req.get("number")
#                     if not isinstance(num , (int , float)):
#                         raise ValueError ("malformed request")

#                     response = {
#                         "method": "isPrime",
#                         "prime": is_prime(num) 
#                         }
#                     sending_data = (json.dumps(response) + "\n").encode('utf-8')
#                     print("********* Sending data: ", sending_data)
#                     conn.sendall(sending_data)

#             except (ValueError):
#                 malformed_response = {
#                     "method": "isPrime",
#                     "number": "malformed request"
#                 }
#                 print("********* Sending  malformed data: " , malformed_response)
#                 conn.sendall((json.dumps(malformed_response)+ "\n").encode('utf-8'))
#                 break
#         # conn.shutdown(socket.SHUT_RDWR)                
#         conn.close()

# def handle_client(conn , addr):
#         print(f"connected by {addr}")
#         data = ""
#         while True:
#             msg = conn.recv(1024)
#             if not msg:
#                 break
#             print("^^^^^^^receives part of msg: ",msg)
#             data += msg.decode('utf-8')
#             while '\n' in data:
#                 # req_data  = data.decode("UTF-8").strip()
#                 s, buffer = data.split('\n',1)
#                 request = s.strip()
#                 if not request:
#                     continue
#                 print("---------Whole data: ", request)
#                 try:
#                     # requests = req_data.split("\n")
#                     # for request in requests:
#                     req = json.loads(request)
#                     print("~~~~~~~req: ", req)
#                     if req.get('method') != 'isPrime' or 'number' not in req:
#                         raise ValueError ("Malformed request")
#                     num = req.get("number")
#                     if not isinstance(num , (int , float)):
#                         raise ValueError ("malformed request")

#                     response = {
#                         "method": "isPrime",
#                         "prime": is_prime(num) 
#                         }
#                     sending_data = (json.dumps(response) + "\n").encode('utf-8')
#                     print("********* Sending data: ", sending_data)
#                     conn.sendall(sending_data)

#                 except (ValueError):
#                     malformed_response = {
#                         "method": "isPrime",
#                         "number": "malformed request"
#                     }
#                     print("********* Sending  malformed data: " , malformed_response)
#                     conn.sendall((json.dumps(malformed_response)+ "\n").encode('utf-8'))
#                     break
#             # conn.shutdown(socket.SHUT_RDWR)                
#             conn.close()
    
# def start_server(SERVER_IP = "0.0.0.0",SERVER_PORT = 8003):
#     with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
#         s.bind((SERVER_IP, SERVER_PORT))
#         s.listen(5)
#         print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
#         try:
#             while True:
#                 conn , addr = s.accept()
#                 print("Connection address from", addr)
#                 thread = threading.Thread(target = handle_client, args = (conn , addr)).start() 
#         except KeyboardInterrupt:
#             print("Shutdown the server")        
#         finally:
#             s.close()

# if __name__ == "__main__":
#     start_server() 

