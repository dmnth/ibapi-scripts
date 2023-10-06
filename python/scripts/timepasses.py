#! /usr/bin/env python3

import datetime

def do_stuff_while_time_goes_by(duration):

    while True:
        time_now = datetime.datetime.now()
        past_5_minutes = time_now + datetime.timedelta(seconds=5.0)
        next_step = past_5_minutes.strftime("%h%m%s")
        print(time_now, next_step) 
#        next_step = past_5_minutes
#        print("time now:", time_now)
#        print("5 seconds: ",next_step)
#        if time_now == next_step: 
#            print('dicks')
#            time_now = past_5_minutes


if __name__ == "__main__":

    do_stuff_while_time_goes_by(4)
