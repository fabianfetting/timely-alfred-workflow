#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime, timedelta
import sys
import operator
import re


def print_time(t):
    total_seconds = int(abs(t).total_seconds())
    hours, remainder = divmod(total_seconds, 60*60)
    minutes, seconds = divmod(remainder, 60)
    sign = t.days < 0 and '- ' or ''
    print(sign + '{}h {}m {}s'.format(hours, minutes, seconds))


def to_delta(op, time):
    time_format = ''
    time_format += 'h' in time and '%Hh' or ''
    time_format += 'm' in time and '%Mm' or ''
    time_format += 's' in time and '%Ss' or ''

    try:
        date_time = datetime.strptime(time, time_format)
    except ValueError:
        raise Exception('Invalid input')
        exit(1)
    time_delta = timedelta(hours=date_time.hour, minutes=date_time.minute, seconds=date_time.second)
    return op == '-' and -time_delta or +time_delta


input_string = reduce(operator.concat, sys.argv[1:]).replace(' ', '')
splitted_string = re.split(r'([+,-])', input_string)
time_strings = splitted_string[::2]
time_ops = ['+'] + splitted_string[1::2]
grouped_times = zip(time_ops, time_strings)
deltas = map(lambda t: to_delta(t[0], t[1]), grouped_times)
summed_deltas = reduce(operator.add, deltas)
print_time(summed_deltas)
