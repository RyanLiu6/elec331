import socket

# Defining UDP server variables
UDP_PORT = 12000
UDP_PACKET_SIZE = 2048
UDP_SERVER = "localhost"
UDP_ADDRESS = (UDP_SERVER, UDP_PORT)

# Message information
NUM_MESSAGES = 10
BASE_MESSAGE = "PING"

def client():
    # Creates the socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Client Started")

    for i in range(NUM_MESSAGES):
        currMsg = input(BASE_MESSAGE + " " + str(i))

        clientSocket.sendto(currMsg, UDP_ADDRESS)
        retMessage, serverAddress = clientSocket.recvfrom(UDP_PACKET_SIZE)

        print(retMessage.decode())

    clientSocket.close()
    print("Client Terminated")


if __name__ == "__main__":
    client()
