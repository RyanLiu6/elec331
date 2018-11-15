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

"""
Assumptions made:
1. If first attempt succeeds, simply attempt self.tries - 1 (2) more times
2. If first attempt fails, immediately print 3 stars

Thus, in the worst case scenario, a user must wait 4 seconds to see triple stars.

One modification that was implemented but was commented out was:
a. If first attempt fails, attempt a second time and print based on result of second attempt
b. If second attempt succeeds, print hostname and address with successful RTT,
   star and attempt self.tries - 2 (1) more time
c. If second attempt fails, immediately print 3 stars to indicate failure

Thus, in the worst case scenario, a user must wait 8 seconds to see triple stars.

I was unsure of which design was "correct" so I picked the one with the shortest wait
time. In any case, commenting out the current implementation and uncommenting out the
modified implementation would show that approach as both approaches work perfectly.
"""
class myTraceRoute:
    def __init__(self, des_hostname):
        # Initializing the traceroute class
        self.hop = 1
        self.tries = NUM_TRIES
        self.port = SOCKET_PORT
        self.des_hostname = des_hostname
        self.des_address = socket.gethostbyname(des_hostname)
        self.sendAddr = (self.des_address, self.port)

    def trace(self):
        info = "traceroute to {} ({}), {} hops max".format(self.des_hostname, self.des_address, MAX_HOPS)

        print(info)

        while True:
            # Print which hop this is
            print(self.hop, end=SPACE)

            # Reset tries
            self.tries = NUM_TRIES

            # Initial attempt
            address, RTT = self.sendRequest()

            # If address is not None, we print the hostname and address before quering again
            # Else, we must verify connection via a second try
            # If second try fails, will print out a third * to indicate failure
            if address:
                # First attempt succeeded
                self.printAddress(address, RTT)

                # Attempt self.tries - 1 more times
                for _ in range(self.tries - 1):
                    self.simpleRequest()
            else:
                for _ in range(self.tries):
                    print(RTT, end=SPACE)

            # Alternate else print
            # else:
            #     # First attempt failed
            #     address, RTT = self.sendRequest()
            #
            #     # If second attempt worked, print hostname and address and try self.tries - 2 times
            #     if address:
            #         self.printAddress(address, RTT)
            #         print(STAR, end=SPACE)
            #
            #         for _ in range(self.tries - 2):
            #             self.simpleRequest()
            #     else:
            #         # If second attempt fails, just print all three stars
            #         for _ in range(self.tries):
            #             print(RTT, end=SPACE)

            # Separate each hop
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
        # Provide hostname based on address
        # Returns the address if it could not resolve the hostname
        try:
            name, alias, addresslist = socket.gethostbyaddr(addr)
            return name
        except socket.herror:
            return addr

    def sendRequest(self):
        SENT_TIME = time.time()
        sender = self.createSender()
        receiver = self.createReceiver()

        sender.sendto(b"", self.sendAddr)

        try:
            data, address = receiver.recvfrom(512)
            RECV_TIME = time.time()
            RTT = round((RECV_TIME - SENT_TIME) * 1000, 3)
            RTT = str(RTT)
        except socket.error:
            address = None
            RTT = "*"
        finally:
            sender.close()
            receiver.close()

        return address, RTT

    def simpleRequest(self):
        address, RTT = self.sendRequest()
        if address:
            print(RTT + " ms", end=SPACE)
        else:
            print(RTT, end=SPACE)

    def printAddress(self, address, RTT):
        # First attempte succeeded
        currAddr = str(address[0])
        currName = self.lookup(currAddr)

        replyAddress = "{} ({})".format(currName, currAddr)

        print(replyAddress, end=SPACE)
        print(RTT + " ms", end=SPACE)

if __name__ == "__main__":
    # Assuming only one destination
    # Must run using sudo because of socket.SOCK_RAW
    des_hostname = sys.argv[1]

    tracer = myTraceRoute(des_hostname)
    tracer.trace()
