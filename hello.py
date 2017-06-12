#!/usr/bin/env python

import os
import time, datetime
import errno
import stat
import sys
import json
import re
import urllib
import socket
import fcntl
import struct

CONFIG_FILE = 'config.json'

def open_and_load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.loads(config_file.read())
    else:
        print "File [%s] doesn't exist, aborting." % (CONFIG_FILE)
        sys.exit(1)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def post2slack(config, txt):
    f = { 'token': config['slack-token'],
          'channel': config['slack-channel'],
          'as_user': 'true',
          'text': txt }
    url = 'https://slack.com/api/chat.postMessage?' + urllib.urlencode(f)
    urllib.urlopen(url)

if __name__ == "__main__":
    config = open_and_load_config()
    data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
    ext_ip = data["ip"]
    interface = str(config['interface'])
    int_ip = get_ip_address(interface)
    res = interface + ": " + int_ip + " => " + ext_ip
    print res
    post2slack(config, res)
