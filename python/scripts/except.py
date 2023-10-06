#! /usr/bin/env python3

import time

class someClass():

    def __init__(self, arg):
        self.arg = None

try:
    for i in range(2):
        a = someClass(12)
        print(someClass.arg)
    
except:
    print("exception block")
    print(a)

a = someClass(12)
time.sleep(5)
print(a)
