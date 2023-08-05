import os
import socket
import sys

max_port = 65535
min_port = 1023


# waits for OK message from server to know if to send the next message
def receive_ack(message, s, i, ip, port):
    try:
        data, addr = s.recvfrom(101)
        if data.decode() != message:
            s.sendto((str(i) + ',' + message).encode(), (ip, port))
            receive_ack(message, s, i, ip, port)
        return

    except socket.timeout:
        s.sendto((str(i) + ',' + message).encode(), (ip, port))
        receive_ack(message, s, i, ip, port)


# create client's socket and send message by message to the server
def send_messages(ip, port, string_list):

    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5.0)

    # for every message in the data (message is 100 bytes)
    for i in range(len(string_list)):

        # send the message
        s.sendto((str(i) + ',' + string_list[i]).encode(), (ip, port))
        receive_ack(string_list[i], s, i, ip, port)

    # close the socket
    s.close()


# split file to smaller packages
def split_file(ip, port, file_name):
    if not os.path.isfile(file_name):
        sys.exit()

    file = open(file_name, "r").read()

    # max number of bytes in a message
    num_of_bytes = 90
    send_messages(ip, port, [file[i:i + num_of_bytes] for i in range(0, len(file), num_of_bytes)])


# check if ip is valid
def check_ip(ip_address):
    points = ip_address.split(".")
    if not len(points) == 4:
        sys.exit()
    for point in points:
        if not 0 <= int(point) <= 255:
            sys.exit()


# check if port is valid
def check_port(port):
    if not min_port <= port <= max_port:
        sys.exit()


# main method - send args to split_files method
if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit()
    try:
        DEST_IP = sys.argv[1]
        check_ip(DEST_IP)
        DEST_PORT = int(sys.argv[2])
        check_port(DEST_PORT)
        FILE_NAME = sys.argv[3]
        split_file(DEST_IP, DEST_PORT, FILE_NAME)
    except ValueError:
        sys.exit()

