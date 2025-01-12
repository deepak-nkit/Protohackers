import struct
import socket
import threading

PRICE_DATA = {}


def get_bit_val(data: bytearray) -> int:
    if len(data) != 4:
        raise ValueError("Not 4 byte ")

    """
    
    data = bytearray([6, 9, 19, 7])
    position = 23

    0 0 0 0 0 1 1 0
        
    """

    # byte_indx = position//8
    # p = position//8
    # print(data[byte_indx])
    # s = (b>>7)%2

    val = 0
    bits = ""
    for byte in data:
        for b in range(8):
            bit = byte >> (7 - b) & 1
            bits += str(bit)
    print(f"bits: {bits}  length: {len(bits)}")

    ln = len(bits)
    for i in range(len(bits)):
        if bits[i] == "1":
            val += 2 ** (ln - 1 - i)
    return val

    # 2nd Option -----------

    # value = 0
    # for byte in range(len(data)):
    #     value += data[byte] * (256 ** (3 - byte))
    # print("Bytes values: ", value)
    # return value

    # Step1: Get the byte containing bit at position
    #        byte = 23
    #        byte_pos = 7

    # Step2: Get bit from byte at byte_pos


def mean_Query(minitime: int, maxtime: int) -> int:
    count = 0
    val = 0
    try:
        for key in PRICE_DATA:
            if key >= minitime and key <= maxtime:
                count += 1
                val += PRICE_DATA[key]
                print(f"coutn{count} val {val}")

    except ZeroDivisionError:
        raise ZeroDivisionError

    num = round(val / count)
    return num


def handle_client(con: socket.socket, addr):
    data = bytearray()
    while True:
        msg = con.recv(1024)
        if not msg:
            break
        data += msg
        print("Received Data ", data)

        while len(data) >= 9:
            first_byte = data[0]
            pair1 = data[1:5]
            pair2 = data[5:9]
            print(f"first_byte: {first_byte}")
            print(f"pair_1: {pair1}")
            print(f"pair_2: {pair2}")
            data = data[9:]

            msg_type = chr(first_byte)
            try:
                if msg_type == "I":
                    print("Insert Message Received!")
                    timestamp = get_bit_val(pair1)
                    value = get_bit_val(pair2)
                    print(f"timestamp: {timestamp} ,  value: {value}")
                    if timestamp not in PRICE_DATA:
                        PRICE_DATA[timestamp] = value

                    else:
                        print("Duplicate Timestamp Occur , Ignoring Message! ")
                    print(f"The Loan price DATA: {PRICE_DATA}")

                elif msg_type == "Q":
                    print("Query Message Received!")
                    print()
                    mintime = get_bit_val(pair1)
                    maxtime = get_bit_val(pair2)
                    print(f"Mintime: {mintime} ,  Maxtime: {maxtime}")
                    if mintime >= maxtime:
                        print(
                            "Invalid query: Mintime is greater than or equal to Maxtime."
                        )
                        con.sendall(struct.pack(">I", 0))
                        continue

                    query_val = mean_Query(mintime, maxtime)

                    if query_val is None:
                        print("NO value find in give Timestamp! ")
                        con.sendall(struct.pack(">I", 0))

                    else:
                        print("****************", query_val)
                        print(f"~~~~~~~    {bytearray(struct.pack('>I',query_val))}")
                        con.sendall(bytearray(struct.pack(">I", query_val)))
                        print("###################################################")


                else:
                    print("Invalid Message type!")
                    break

            except ValueError as e:
                print(f"ValueError {e}")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    con.shutdown(socket.SHUT_RDWR)
    con.close()


def start_server(SERVER_IP="0.0.0.0", SERVER_PORT=1672):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(5)
        print(f"Server listening at{SERVER_IP} {SERVER_PORT}")
        while True:
            try:
                con, addr = s.accept()
                print(f"connecting address {addr}")
                thread = threading.Thread(
                    target=handle_client, args=(con, addr)
                ).start()
            except KeyboardInterrupt:
                print("Shutdown Server")
            finally:
                s.close()


if __name__ == "__main__":
    start_server()
