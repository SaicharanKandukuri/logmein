################################################################
# keep_alive.py
#
# Copyright (C) 2021 SaicharanKandukrui <saicharankandukuri1x1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
###################################################################

import copy
import logging
import sys
import urllib
import urllib.request as urllib2
from signal import signal, SIGINT
from sys import exit
from time import sleep
from urllib.error import HTTPError

from rich.logging import RichHandler

import modules.loginpu as loginpu

"""
Accept user input and pass it to the loginpu module
    script <username> <password>
        url is set to deafault value http://10.0.0.11:8090/login.xml        
"""
x = 0

# logger with rich logging format
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")


def basic_login_nosys(username, password):
    """
    Accept user input and pass it to the loginpu module
        main.py <username> <password>
            url is set to deafault value http://10.0.0.11:8090/login.xml        
    """
    url = "http://10.0.0.11:8090/login.xml"

    response = copy.deepcopy(loginpu.login(url, username, password))
    return [{'logedin': response[0], 'response': response[1], 'server_status': response[2]}]


# min 2 is suggested for intervel
def keep_alive(username=sys.argv[1], password=sys.argv[2], interval=2):
    """
    Runs script forever to keep Wi-Fi logged in
    """
    try:
        req = urllib2.Request("http://10.0.0.11:8090/",
                              headers={'User-Agent': 'Mozilla/5.0'})
        urllib2.urlopen(req)
        log.info("Check: \"Parul_WIFI\" connected")
    except urllib.error.URLError:
        log.warning("Could not see \"PARUL_WIFI\"")
        log.warning("Try Connecting to wifi?")
        log.warning('connection timed out, low bandwidth?')


    try:
        req2 = urllib2.Request("https://www.google.com",
                               headers={'User-Agent': 'Mozilla/5.0'})
        urllib2.urlopen(req2)
        log.info("Internet Connection Avalible")
    except urllib.error.URLError:
        log.warning("Internet access Failed ?")
        log.info("Attempting To Sign In " + username)
        log.info("looged in as " + username)
        log.info(basic_login_nosys(username, password))
        log.warning('connection timed out, low bandwidth?')

    sleep(interval)


def handler(signal_received, frame):
    # Handle any cleanup here
    log.warning('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    log.info('Running ' + sys.argv[0] + '. Press CTRL-C to exit.')
    while True:
        keep_alive(sys.argv[1], sys.argv[2])
