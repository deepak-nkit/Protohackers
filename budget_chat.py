import socket, threading , re



MEMBERS = {}

def set_Member(username:str):
    if len(username) < 1:
        if not re.Match(r"^[a-z A-Z0-9]+$",username):

        


def handle_client(conn: socket.socket , addr):
    data = ""
    print("************")
    while True:
        print("************")
        msg = conn.recv(1024)
        if not msg:
            exit()
        print("Data Accept from client")
        data += msg.decode("UTF-8")
        print(f"Data: {data}")
        while '\n' in data:
            print("In while loop")
            end = data.index('\n')
            req_data = data[:end]
            data = data[end+1:]
            set_Member(data)





    
def start_server(SERVER_IP = "0.0.0.0", SERVER_PORT = 1672):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP , SERVER_PORT))
        s.listen(10)
        print(f"Listening at: {SERVER_IP}:{SERVER_PORT}")
        try:
            while True:
               conn , addr =  s.accept()
               print(f"connected by {addr}")
               conn.sendall(b"Welcome to budgetchat! What shall I call you?\n")
               thread = threading.Thread(target=handle_client , args=(conn , addr))
               thread.start()

        except KeyboardInterrupt:
            print("ShutDown the Server ")


if __name__ == "__main__":
    start_server()
    
            

