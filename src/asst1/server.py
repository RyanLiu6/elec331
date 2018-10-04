import time
import socket
import random

# Defining UDP server variables
UDP_PORT = 12000
UDP_PACKET_SIZE = 4096
UDP_SERVER = "localhost"
UDP_ADDRESS = (UDP_SERVER, UDP_PORT)

def server():
    # Sets the random seed for pseudo-random behaviour
    random.seed(time.time())

    # Creates the socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binds the socket to the defined server address
    serverSocket.bind(UDP_ADDRESS)

    print("Starting up on {} port {}".format(*UDP_ADDRESS))

    while True:
        # Close the serverSocket if we terminate the server via ctrl-c
        try:
            # Receive data from the socket
            data, address = serverSocket.recvfrom(UDP_PACKET_SIZE)
        except KeyboardInterrupt:
            serverSocket.close()
            print("Server Terminated")
            break

        print('received {} bytes from {}'.format(
            len(data), address))
        print(data.decode())

        # Randomly wait for 5 to 50ms
        randomWait()

        # Check if we should ignore this packet, with a 10% chance
        if randomIgnore():
            continue
        else:
            serverSocket.sendto(data, address)

def randomWait():
    # Chooses a number between 5 and 50 inclusive
    delay = random.randint(5, 50)
    print("Delay is: ", end = "")
    print(delay)

    # Sleep for 5 - 50ms
    time.sleep(delay / 1000)

def randomIgnore():
    # Chooses a number between 1 and 10 inclusive
    chance = random.randint(1, 10)

    # Ignores the message (True) if it equals 1 (10%)
    if chance == 1:
        return True
    else:
        return False

if __name__ == "__main__":
    server()
