from __future__ import print_function
import sys
import json
import argparse
import datetime
import operator


def print_time(t):
    total_seconds = int(t.total_seconds())
    hours, remainder = divmod(total_seconds, 60*60)
    minutes, seconds = divmod(remainder, 60)
    output = {
    	'items': [
    		{
    			'uid': 'result',
    			'type': 'file',
    			'title': '{}h {}m {}s'.format(hours, minutes, seconds),
    			'subtitle': sys.argv[1],
    			'arg': sys.argv[1],
    			'icon': {
    				'path': 'icon.png'
    			}
    		}
    	]
    }

    output_json = json.dumps(output)
    sys.stdout.write(output_json)


def is_time(string):
    return (
        string.endswith('h') |
        string.endswith('m') |
        string.endswith('s')
    )



def get_args():
    return str.split(sys.argv[1])


def parse_time_strings(time_strings):
    time = {
        'hours': 0,
        'minutes': 0,
        'seconds': 0,
    }

    for time_string in time_strings:
        if time_string.endswith('h'):
            time['hours'] += int(time_string[0:(len(time_string) - 1)])
        if time_string.endswith('m'):
            time['minutes'] += int(time_string[0:(len(time_string) - 1)])
        if time_string.endswith('s'):
            time['seconds'] += int(time_string[0:(len(time_string) - 1)])

    return time


def parse_args(args):
    result = ()
    concatenated_time = []
    i = 0
    for arg in args:
        i += 1
        if is_time(arg):
            concatenated_time += [arg]
        else:
            if len(concatenated_time) > 0:
                time_dict = parse_time_strings(concatenated_time)
                concatenated_time = []
                result += (time_dict,)
            result += (arg,)
        if len(args) == i:
            time_dict = parse_time_strings(concatenated_time)
            concatenated_time = []
            result += (time_dict,)
    return result


def sum_times(times):
    result = times[0]
    return map(lambda t: result + t)


def subtract_times(times):
    result = times[0]
    return map(lambda t: result - t)


def to_timedelta(time):
    return datetime.timedelta(hours=time['hours'], minutes=time['minutes'], seconds=time['seconds'])


def print_invalid():
    output = {
    	'items': [
    		{
    			'uid': 'invalid',
    			'type': 'file',
    			'title': 'Invalid',
    			'subtitle': sys.argv[1],
    			'arg': sys.argv[1],
    			'icon': {
    				'path': 'icon.png'
    			}
    		}
    	]
    }
    output_json = json.dumps(output)
    sys.stdout.write(output_json)

# PARSE
time_result = None
try:
    given_args = get_args()
    times = parse_args(given_args)
    if len(times) <= 0:
        raise Exception('Invalid')

    # CALCULATE
    ops = { '+': operator.add, '-': operator.sub }
    time_result = to_timedelta(times[0])
    i = 2
    while (i < len(times)):
        time = to_timedelta(times[i])
        o = times[i-1]
        time_result = ops[o](time_result, time)
        i += 2
except:
    print_invalid()
    sys.exit()

print_time(time_result)
