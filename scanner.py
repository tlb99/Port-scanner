#!/bin/python

import sys
import socket
from datetime import datetime

# Define our target
if len(sys.argv) == 2:
    try:
        target = socket.gethostbyname(sys.argv[1]) # Translate hostname to IPv4
    except socket.error:
        print("Invalid IP address.")
        sys.exit()
else:
    print("Invalid amount of arguments.")
    print("Syntax: python3 scanner.py <ip>")
    sys.exit()

# Print banner 
print("-" * 50)
print("Scanning target " + target)
print("Time started: " + str(datetime.now()))
print("-" * 50)

try:
    for port in range(1, 65535): # TODO add threading support
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port)) # returns an error indicator if connection was unsuccessful
        if result == 0:
            print("Port {} is open".format(port)) 
        s.close() # close connection

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()

except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()

except socket.error:
    print("Couldn't connect to server.")
    sys.exit()
