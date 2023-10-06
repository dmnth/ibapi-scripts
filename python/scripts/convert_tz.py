#! /usr/bin/env python3

from datetime import datetime

import pytz

def convert_times(local_time, exchange_zone_id):

    user_time = datetime.strptime(local_time, "%Y%m%d-%H:%M:%S")
    exchange_time = \
    user_time.astimezone(pytz.timezone('US/Central')).strftime("%Y%m%d-%H:%M:%S")
    print('US/Central time: ', exchange_time)



convert_times('20230116-15:15:00', "US/Central")
