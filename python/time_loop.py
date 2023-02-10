#! /usr/bin/env python3

import time
from datetime import datetime

def time_lopp():
    #somecode 
    while True:
        start_time = time.time()
        now = datetime.now().strftime("")
        for i in range(12):
            print(i)
        print("Time to sleep: ", 300 - ((time.time() - start_time) % 300))            
        time.sleep(300 - ((time.time() - start_time) % 300))
    return

if __name__ == "__main__":
    time_lopp()
