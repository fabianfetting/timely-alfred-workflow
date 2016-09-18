import subprocess
import sys
import json

def print_time(t):
    output = {
    	'items': [
    		{
    			'uid': 'result',
    			'type': 'file',
    			'title': t,
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

try:
    result = subprocess.check_output(['./timely.py'] + sys.argv[1:])
except subprocess.CalledProcessError as e:
    print_invalid()
    exit(0)

print_time(result[:-2])
