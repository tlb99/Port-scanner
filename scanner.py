#!/bin/python
import sys
import socket
from multiprocessing import Pool
from datetime import datetime

def scan_port(args:tuple):
    target, port = args
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((target, port)) # returns an error indicator if connection was unsuccessful
        s.close() # close connection
        return port, True

    except:
        return port, False

if __name__ == '__main__':
    # check for valid input
    if len(sys.argv) == 3:
        try:
            target = socket.gethostbyname(sys.argv[1]) # translate hostname to IPv4
        except socket.error:
            print("Invalid IP address.")
            sys.exit()
    else:
        print("Invalid amount of arguments.")
        print("Syntax: python3 scanner.py <ip> <processes>")
        sys.exit()

    # print banner and info
    print("-" * 50)
    print("Scanning target " + target)
    print("Time started: " + str(datetime.now()))
    print("-" * 50)

    ports = range(1, 65535)

    pool = Pool(processes=int(sys.argv[2]))

    for port, status in pool.imap_unordered(scan_port, [(sys.argv[1], port) for port in ports]):
        if status: print("Port " + str(port) + " is open") 