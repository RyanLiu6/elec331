import sys
import time
import socket

# Defining some traceroute base variables
STAR = "*"
SPACE = "  "
TIMEOUT = 4
SENT_TIME = 0
RECV_TIME = 0
NUM_TRIES = 3
MAX_HOPS = 30
SOCKET_PORT = 33434
TERM_MSG = "max number of hops reached ... terminating"

class myTraceRoute:
    def __init__(self, des_hostname):
        # Initializing the traceroute class
        self.hop = 1
        self.tries = NUM_TRIES
        self.port = SOCKET_PORT
        self.des_hostname = des_hostname
        self.des_address = socket.gethostbyname(des_hostname)
        self.sendAddr = (self.des_address, self.port)
        self.rttArr = []

    def trace(self):
        info = "traceroute to {} ({}), {} hops max".format(self.des_hostname, self.des_address, MAX_HOPS)

        print(info)

        while True:
            # Print which hop this is
            print(self.hop, end=SPACE)

            # initialize certain variables every hop
            address = None
            self.rttArr.clear()
            self.tries = NUM_TRIES

            # Perform 3 attempts each time
            while self.tries > 0:
                SENT_TIME = time.time()
                sender = self.createSender()
                receiver = self.createReceiver()

                sender.sendto(b"", self.sendAddr)

                # Attempt to receive data
                # As we set the timeout previously, timeouts will go to exception
                try:
                    data, address = receiver.recvfrom(512)
                    RECV_TIME = time.time()
                    RTT = round((RECV_TIME - SENT_TIME) * 1000, 2)

                    self.tries -= 1
                    self.rttArr.append(RTT)
                except socket.error:
                    # Error (timeout) occured, so we need a *
                    self.tries -= 1

                    self.rttArr.append(STAR)
                finally:
                    sender.close()
                    receiver.close()

            # Printing for each hop
            # If address is not None, we print the address
            if address:
                currAddr = str(address[0])
                currName = self.lookup(currAddr)

                replyAddress = "{} ({})".format(currName, currAddr)

                print(replyAddress, end=SPACE)

            for rtt in self.rttArr:
                currMsg = str(rtt)
                if currMsg != STAR:
                    currMsg += " ms"

                print(currMsg, end=SPACE)

            print()

            # Increment hops
            self.hop += 1

            # Check if we have arrived at our destination
            if address and address[0] == self.des_address:
                break

            # Check if we have not reached our destination after MAX_HOPS hops
            if self.hop > MAX_HOPS:
                print(TERM_MSG)
                break

    def createSender(self):
        # Create sending socket using UDP as underlying protocol and set the TTL
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, self.hop)

        return sender

    def createReceiver(self):
        # Create receiving socket using ICMP as underlying protocol and set timeout
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        receiver.settimeout(TIMEOUT)
        receiver.bind(("", self.port))

        return receiver

    def lookup(self, addr):
        try:
            name, alias, addresslist = socket.gethostbyaddr(addr)
            return name
        except socket.herror:
            return addr

if __name__ == "__main__":
    # Assuming only one destination
    # Must run using sudo because of socket.SOCK_RAW
    des_hostname = sys.argv[1]

    tracer = myTraceRoute(des_hostname)
    tracer.trace()
