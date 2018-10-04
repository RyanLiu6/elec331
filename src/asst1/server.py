import time
import socket
import random

# Defining UDP server variables
UDP_PORT = 12000
UDP_PACKET_SIZE = 4096
UDP_SERVER = "127.0.0.1"
UDP_ADDRESS = (UDP_SERVER, UDP_PORT)

def server():
    # Sets the random seed
    random.seed(time.time())

    # Creates the socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binds the socket to the defined port
    serverSocket.bind(UDP_ADDRESS)

    print("Starting up on {} port {}".format(*UDP_ADDRESS))

    while True:
        data, address = serverSocket.recvfrom(UDP_PACKET_SIZE)

        print('received {} bytes from {}'.format(
            len(data), address))
        print(data.decode())

        randomWait()

        if randomIgnore():
            continue
        else:
            serverSocket.sendto(data, address)

def randomWait():
    # Randomly wait for 5 to 50ms
    delay = random.randint(5, 50)
    print("Delay is: ", end = "")
    print(delay)
    time.sleep(delay / 1000)

def randomIgnore():
    # Ignores a message with a 10% chance
    chance = random.randint(1, 10)

    if chance == 1:
        return True
    else:
        return False

if __name__ == "__main__":
    server()
