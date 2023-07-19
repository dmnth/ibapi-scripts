#! /usr/bin/env python3

import socket
import threading
import sys
import struct
from ibapiTest.connection import Connection
from ibapiTest.server_versions import MIN_CLIENT_VER, MAX_CLIENT_VER

host = "192.168.43.222"
port = 7497

v100prefix = "API\0"
v100version = "v%d..%d" % (MIN_CLIENT_VER, MAX_CLIENT_VER) + " " + " " 

msg = struct.pack("!I%ds" % len(v100version), len(v100version), str.encode(v100version))
print(msg)
msg2 = str.encode(v100prefix, 'ascii') + msg

skt = socket.socket()
skt.connect((host, port))

if skt is not None:
    skt.send(msg2)
    print(f"{msg2} sent")

allbuf = b""
while True:
    buf = skt.recv(4096)
    allbuf += buf
    print("len %d raw:%s| " % (len(buf), buf))
    if len(buf) < 4096:
        break

print(allbuf)


class twsTestSocket():

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def sendMessage(self, message):
        self.sock.send(message)

    def receiveMessage(self)
        allbuf = b""
        while True:
            buf = skt.recv(4096)
            allbuf += buf
            print("len %d raw:%s| " % (len(buf), buf))
            if len(buf) < 4096:
                break
        























