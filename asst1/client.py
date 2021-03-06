import time
import socket

# Defining UDP server variables
UDP_PORT = 12000
UDP_PACKET_SIZE = 4096
UDP_SERVER = "localhost"
UDP_ADDRESS = (UDP_SERVER, UDP_PORT)

# Message information
RET_MESSAGE = "".encode()
NUM_MESSAGES = 10
BASE_MESSAGE = "PING"
SENT_TIME = 0

def client():
    # Creates the socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the timeout
    clientSocket.settimeout(1)

    print("Client Started")

    for i in range(NUM_MESSAGES):
        # Generate the message
        currMsg = str.encode(BASE_MESSAGE + " " + str(i))

        # Send message to server and set the SENT_TIME for RTT timing
        clientSocket.sendto(currMsg, UDP_ADDRESS)
        SENT_TIME = time.time()

        # Attempt to receive from the socket
        # If more than one second has passed, we print an exception
        try:
            RET_MESSAGE, serverAddress = clientSocket.recvfrom(UDP_PACKET_SIZE)
        except socket.timeout:
            print("Request " + str(i) + " Timed Out")
            continue

        # Printing received message and calculating RTT
        timeDiff = time.time() - SENT_TIME
        print("Return Message: " + RET_MESSAGE.decode())

        print("This took %.2f ms" % (timeDiff * 1000))

    clientSocket.close()
    print("Client Terminated")

if __name__ == "__main__":
    client()
