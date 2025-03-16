import socket

DATABASE = {}

def insert_message (message: str):
    indx = message.index('=')
    key = message[:indx]
    val = message[indx+1:]
    DATABASE[key] = val

def retrieve_message (key: str) -> str:
    for k in DATABASE.keys():
        if k == key and len(DATABASE[key]) > 0:
            msg = f"{key}={DATABASE[key]}"
            print(msg)
            return msg
    print("key=")
    return ("key=")



def start_server(UDP_IP= '127.0.0.1' , UDP_PORT= 1672): 
    with socket.socket(socket.AF_INET , socket.SOCK_DGRAM) as s:
        # s.setsockopt(socket.IPPROTO_IPV6 , socket.IPV6_V6ONLY , 0)
        s.bind((UDP_IP , UDP_PORT))
        print(f"Listening at: {UDP_IP}:{UDP_PORT}")

        while True:
            print("Herer")
            msg , client_addr = s.recvfrom(1024)
            print(f"Received Message from Client: {msg.decode()} ")

            #Send to Client Address
            s.sendto(msg , client_addr)




            # print(f"messsssage {decode_msg}")
            # s.sendto(msg , addr)
            # if "=" in decode_msg:
            #     insert_message(decode_msg)
            # else:
            #     res = retrieve_message(decode_msg)
            #     s.sendto((res.encode('utf-8')) , addr)

if __name__ == '__main__':
    start_server()