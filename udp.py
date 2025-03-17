import socket

DATABASE = {'version': "Ken's version 1.0"}

def insert_message (message: str):

    indx = message.index('=')
    key = message[:indx]
    val = message[indx+1:]
    if key != 'version':
        DATABASE[key] = val

def retrieve_message (key: str) -> str:
    for k in DATABASE.keys():
        if key == 'version':
            return (f"{key}={DATABASE[key]}")
        if key == k and (len(DATABASE[key]) > 0):
            msg = f"{key}={DATABASE[key]}"
            return msg
    return ("key=")

def start_server(UDP_IP= '0.0.0.0' , UDP_PORT= 1672): 
    with socket.socket(socket.AF_INET , socket.SOCK_DGRAM) as s:
        # s.setsockopt(socket.IPPROTO_IPV6 , socket.IPV6_V6ONLY , 0)
        s.bind((UDP_IP , UDP_PORT))
        print(f"Listening at: {UDP_IP}:{UDP_PORT}")

        while True:
            msg , client_addr = s.recvfrom(1024)
            decode_msg = msg.decode()
            print(f"Received Message from Client: {decode_msg} ")
            decode_msg = decode_msg.strip('\n')

            #Send to Client Address
            # s.sendto(msg , client_addr)

            if "=" in decode_msg:
                insert_message(decode_msg)
            else:
                res = retrieve_message(decode_msg)
                res = res+'\n'
                print(f"retrive data : {res}")
                s.sendto((res.encode()) , client_addr)

if __name__ == '__main__':
    start_server()