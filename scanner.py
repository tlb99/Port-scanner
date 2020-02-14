#!/bin/python
import sys
import socket
from multiprocessing import Process, Lock
from datetime import datetime

l = Lock()

def scan_ports(start: int, end: int):
    try:
        for port in range(start,end): 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((target, port)) # returns an error indicator if connection was unsuccessful
            if result == 0:
                with l:
                    print("Port {} is open".format(port)) 
            s.close() # close connection

    # quit if an interrupt is detected
    except KeyboardInterrupt:
        sys.exit()

    # quit if the hostname could not be resolved
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()

    # quit if the server couldn't be reached
    except socket.error:
        print("Couldn't connect to server.")
        sys.exit()

if __name__ == '__main__':
    # check for valid input
    if len(sys.argv) == 2:
        try:
            target = socket.gethostbyname(sys.argv[1]) # translate hostname to IPv4
        except socket.error:
            print("Invalid IP address.")
            sys.exit()
    else:
        print("Invalid amount of arguments.")
        print("Syntax: python3 scanner.py <ip>")
        sys.exit()

    # print banner and info
    print("-" * 50)
    print("Scanning target " + target)
    print("Time started: " + str(datetime.now()))
    print("-" * 50)

    processes = 5
    totalports = 65535

    ports = list(range(1, totalports+3, int(totalports/processes)))

    m = len(ports)-1
    i = 0

    while i < m:
        p = Process(target=scan_ports, args=(ports[i],ports[i+1]))
        i += 1
        p.daemon = True
        p.start()
        
    while processes >= 0:
        p.join()
        processes -= 1

    sys.exit()