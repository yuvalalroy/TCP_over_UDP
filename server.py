import socket
import sys

WANTED_MESSAGE = 0
max_port = 65535
min_port = 1023


# create server's socket and wait to get a message from client and print the messages.
def receive_message():

    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PORT))
    while True:

        # receive data from the client
        data, addr = s.recvfrom(101)

        # split the header from the message
        number_message, message = data.decode().split(",", 1)
        global WANTED_MESSAGE

        # if this is the wanted message - print it and send a message back to client
        if int(number_message) == WANTED_MESSAGE:
            WANTED_MESSAGE += 1
            print(message, end='')
        s.sendto(message.encode(), addr)


# check if port is valid
def check_port(port):
    if not min_port <= port <= max_port:
        sys.exit()


# main method
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    try:
        PORT = int(sys.argv[1])
        check_port(PORT)
        receive_message()

    except ValueError:
        sys.exit()
