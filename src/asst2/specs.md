# Assignment 2 Specs
Write a program in Python 3, called myTraceRoute.
The program should implement the basic traceroute program functionality as follows:

1. It displays the routers' info along the way (one per line).
2. It calculates and displays 3 RTT values (ms) for each router (on the same line as the router info, similar to traceroute). If an RTT cannot be calculated within 4 seconds (a timeout), it should display a * (asterisk) instead for the RTT value.
3. The maximum number of hopes in the path to search for the destination is 30 hops, after which (if reached) the program terminates with a message "max number of hops reached ... terminating".
You can decide on the details of implementation within the requirements.
