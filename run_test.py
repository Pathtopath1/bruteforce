
import os
import sys
import json
import base64

# Generate config for bruteforce.py and convert to json
config = {}
config["ip"] = "127.0.0.1"
config["port"] = "20"
config["service"] = sys.argv[2]
config["tool"] = sys.argv[1]
config["bruteforce_threads"] = "20"
config["login"] = True
config["password"] = True
json_str = json.dumps(config)

# Encode to base64
message_bytes = json_str.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

# Run bruteforce.py
os.system("python3 bruteforce.py %s %s" % (base64_message, "/root/upload"))
