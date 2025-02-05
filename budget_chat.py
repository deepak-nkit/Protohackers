import socket, threading , re

ACTIVE_MEMBERS = {}

def set_Member(username:str):
    if not username or not re.match(r"^[a-z A-Z0-9]+$", username):
       return False
    elif len(username) < 1 or len(username) > 16:
        return False
    return True


def handle_client(conn: socket.socket , addr):
    # print(f"conn {conn} addr {addr}")

    # first check the username 
    conn.sendall(b"Welcome to budgetchat! What shall I call you?\n")
    msg = conn.recv(1024).decode('ASCII')

    if not set_Member(msg):
        conn.sendall(b"Invalid Usernmae! Use only Characters and numbers")
        conn.close()
        return
    elif msg in ACTIVE_MEMBERS.keys():
        conn.sendall(b"User already exist! use different usernae")
        conn.close()
        return

    username = msg
    ACTIVE_MEMBERS[username] = conn
    print(type(ACTIVE_MEMBERS[username]))
    print(ACTIVE_MEMBERS)
    print(f"{username} has joined from {addr}")

    # Presence notification: 
    presented_user = ""
    join_msg = f"*{username} has entered the room"
    for user , sock in ACTIVE_MEMBERS.items():
        if user != username:
            presented_user += user
            presented_user += ','
            sock.senall(join_msg.encode("ASCII"))

    print(f"* The room contains:{presented_user}")

    # Handle message: 
    data = ""
    while True:
        msg = conn.recv(1024)
        if not msg:
            exit()
        data += msg.decode("UTF-8")
        print(f"Data: {data}")
        while '\n' in data:
            end = data.index('\n')
            req_data = data[:end]
            data = data[end+1:]


    #Handle disconnection
    del ACTIVE_MEMBERS[username]
    conn.close()
    

def start_server(SERVER_IP = "0.0.0.0", SERVER_PORT = 1672):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP , SERVER_PORT))
        s.listen(10)
        print(f"Listening at: {SERVER_IP}:{SERVER_PORT}")
        try:
            while True:
               conn , addr =  s.accept()
               print(f"connected by {addr}")
               thread = threading.Thread(target=handle_client , args=(conn , addr))
               thread.start()

        except KeyboardInterrupt:
            print("ShutDown the Server ")


if __name__ == "__main__":
    start_server()
    
            

