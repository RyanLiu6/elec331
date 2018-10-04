import socket

# Defining UDP server variables
UDP_PORT = 12000
UDP_PACKET_SIZE = 2048
UDP_SERVER = "localhost"
UDP_ADDRESS = (UDP_SERVER, UDP_PORT)

def server():
    # Creates the socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binds the socket to the defined port
    serverAddress = (UDP_SERVER, UDP_PORT)
    serverSocket.bind(serverAddress)

    print("Starting up on {} port {}".format(*serverAddress))

    while True:
        data, address = serverSocket.recvfrom(UDP_PACKET_SIZE)

        print(data)
        retData = data[::-1]

        if data:
            serverSocket.sendto(retData, address)
        else:
            print("Waiting for message")

if __name__ == "__main__":
    server()
