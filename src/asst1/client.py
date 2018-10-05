import socket

# Defining UDP server variables
UDP_PORT = 12000
UDP_SERVER = "localhost"
UDP_ADDRESS = (UDP_SERVER, UDP_PORT)

def client():
    # Creates the socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = input("PING 1")

    print("Started")

    clientSocket.sendto(message, (serverName, serverPort))
    retMessage, serverAddress = clientSocket.recvfrom(2048)

    print(retMessage.decode())
    clientSocket.close()
    print("Finished")


if __name__ == "__main__":
    client()
