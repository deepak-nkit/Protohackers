import sys
import struct
import time
import socket
import threading


PRICE_DATA = {}


def get_bit_val(data: bytearray) -> int:
    if len(data) != 4:
        raise ValueError("The Data Uncomplete < 4 Bytes")

    val = 0
    bits = ""
    for byte in data:
        for b in range(8):
            bit = byte >> (7 - b) & 1
            bits += str(bit)

    ln = len(bits)
    is_neg = bits[0] == "1"
    for i in range(len(bits)):
        if is_neg and i == 0:
            val -= 2 ** 32
        if bits[i] == "1":
            val += 2 ** (ln - 1 - i)

    return val


def mean_Query(minitime: int, maxtime: int) -> int:
    sorted_data = {}
    if minitime > maxtime:
        return 0

    for timestamp, value in PRICE_DATA.items():
        if minitime <= timestamp and maxtime >= timestamp:
            sorted_data[timestamp] = value

    if not sorted_data:
        return 0
    total_sum = sum(sorted_data.values())
    total_count = len(sorted_data)
    with open("query.txt", "a") as f:
        f.write(f"Query range: {minitime} to {maxtime} len of data {len(sorted_data)}\n")
        f.write(str(round(total_sum/total_count)))
        f.write("\n")
    return round(total_sum / total_count)


def handle_client(con: socket.socket, addr):
    data = bytearray()
    try:
        while True:
            msg = con.recv(1024)
            if not msg:
                break
            data += msg

            while len(data) >= 9:
                first_byte = data[0]
                pair1 = data[1:5]
                pair2 = data[5:9]
                data = data[9:]
                # print(f"Remainig Data:--------   {data}")

                msg_type = chr(first_byte)

                if msg_type not in ["I", "Q"]:
                    # print("Invalid message Type .... ")
                    continue


                if msg_type == "I":
                    print("Insert Message Received!")
                    timestamp = get_bit_val(pair1)
                    value = get_bit_val(pair2)
                    # print(f"timestamp: {timestamp} ,  value: {value}")
                    if value < 0:
                        print(
                            "********************************************************************************************************************************************************************"
                        )

                    if timestamp not in PRICE_DATA:
                        PRICE_DATA[timestamp] = value

                    else:
                        print("Duplicate Timestamp Occur , Ignoring Message! ")
                        continue

                elif msg_type == "Q":
                    print("Query Message Received!")
                    mintime = get_bit_val(pair1)
                    maxtime = get_bit_val(pair2)
                    print(f"Mintime: {mintime} ,  Maxtime: {maxtime}")

                    if mintime < 0 or maxtime < 0:
                        print(
                            "********************************************************************************************************************************************************************"
                        )

                    query_val = mean_Query(mintime, maxtime)
                    if query_val == 0:
                        print("NO value find in give Timestamp! ")
                        con.sendall(struct.pack(">I", 0))

                    else:
                        print("############")
                        print("value from qurey : ",bytearray(struct.pack(">i", query_val)))
                        con.sendall(bytearray(struct.pack(">i", query_val)))
                        with open("data.csv", "w") as f:
                            f.write(str(bytearray(struct.pack(">i", query_val))))

                else:
                    print("Invalid Message type!")
                    break

            # if len(data) > 0 and len(data) < 9:
            #     print(f"incomplete data from {addr} , waiting for new data.....")

    except Exception as e:
        print(f"error handling client {addr}: {e}")
    finally:
        con.close()


def start_server(SERVER_IP="0.0.0.0", SERVER_PORT=1672):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(5)
        print(f"Server listening at{SERVER_IP} {SERVER_PORT}")
        while True:
            try:
                con, addr = s.accept()
                # print(f"connecting address {addr}")
                threading.Thread(target=handle_client, args=(con, addr)).start()
            except KeyboardInterrupt:
                # print("Shutdown Server")
                break


if __name__ == "__main__":
    start_server()
