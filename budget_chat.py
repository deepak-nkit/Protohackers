import socket, threading, re

ACTIVE_MEMBERS = {}


def set_Member(username: str):
    if not username or not re.match(r"^[a-zA-Z0-9]+$", username):
        return False
    elif len(username) < 1 or len(username) > 16:
        return False
    return True


def broadCast_message(message: str, username: str):
    for user, sock in ACTIVE_MEMBERS.items():
        if user != username:
            sock.sendall(message.encode("ASCII"))


def handle_client(conn: socket.socket, addr):
    #  first Receive the username:
    conn.sendall(b"Welcome to budgetchat! What shall I call you?\n")
    username = None

    try:
        msg = conn.recv(1024).decode("ASCII").strip()

        if not set_Member(msg):
            conn.sendall(b"Invalid Usernmae! Use only Characters and numbers")
            conn.close()
            return
        elif msg in ACTIVE_MEMBERS.keys():
            conn.sendall(b"User already exist! use different username")
            conn.close()
            return

        username = msg
        ACTIVE_MEMBERS[username] = conn
        # print(ACTIVE_MEMBERS)
        print(f" {username} has joined from {addr}")

        # Announce member names:
        presented_user = ", ".join(user for user in ACTIVE_MEMBERS.keys() if user != username)
        members_names = f"* The room contains: {presented_user}\n"
        print(f"~~~\t~~: The User {username} -----  the announcement member {presented_user}\n ")
        conn.sendall(members_names.encode("utf-8"))

        # Presence notification:
        join_msg = f"* {username} has entered the room"
        broadCast_message(join_msg, username)


        # Handle message:
        data = ""
        while True:

            msg = conn.recv(1024)
            if not msg:
                break
            data += msg.decode("UTF-8").strip()
            print(f"Data: {data}")
            while "\n" in data:
                end = data.index("\n")
                req_data = data[:end]
                data = data[end + 1 :]
                sender_message = f"[{username}] {req_data}"
                print(sender_message)
                broadCast_message(sender_message, username)

    except Exception as e:
        print(f"{username} has disconnected.")

        # Remove User and Notify others:
    finally:
        print("In Final Block")
        if username in ACTIVE_MEMBERS:
            del ACTIVE_MEMBERS[username]
            broadCast_message(f"* {username} has left the chat", username)

        conn.close()
        print(f"Connection Closed for {username}")


def start_server(SERVER_IP="0.0.0.0", SERVER_PORT=1672):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(10)
        print(f"Listening at: {SERVER_IP}:{SERVER_PORT}")
        try:
            while True:
                conn, addr = s.accept()
                print(f"connected by {addr}")
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()

        except KeyboardInterrupt:
            print("ShutDown the Server ")


if __name__ == "__main__":
    start_server()
