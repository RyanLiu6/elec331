import time
import socket

# Defining UDP server variables
UDP_PORT = 12000
UDP_PACKET_SIZE = 4096
UDP_SERVER = "127.0.0.1"
UDP_ADDRESS = (UDP_SERVER, UDP_PORT)

# Message information
NUM_MESSAGES = 10
BASE_MESSAGE = "PING"
SENT_TIME = 0
RECV_TIME = 0

def client():
    # Creates the socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Client Started")

    for i in range(NUM_MESSAGES):
        currMsg = str.encode(BASE_MESSAGE + " " + str(i))

        clientSocket.sendto(currMsg, UDP_ADDRESS)
        SENT_TIME = time.time()

        retMessage, serverAddress = clientSocket.recvfrom(UDP_PACKET_SIZE)
        RECV_TIME = time.time()

        print("Return Message: " + retMessage.decode())

        print("This took %.2f ms" % (RECV_TIME*1000 - SENT_TIME*1000))

    clientSocket.close()
    print("Client Terminated")


if __name__ == "__main__":
    client()
