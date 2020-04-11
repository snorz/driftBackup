#!/usr/bin/python
import subprocess
import argparse
import json
import urllib2
import requests

VERBOSE = 0

COMPANY = "none"

INCREASE_STEP = 100
DECREASE_STEP = 100
DOWNLOAD_LIMIT = 1.5
BUFFER = 0

parser = argparse.ArgumentParser(prog='dscale.py')
parser.add_argument('-v','--verbose',dest="verbose",help='Turn verbosity on',default=False,action="store_true")
parser.add_argument('-c','--company',dest="company",help='Company name',default=COMPANY)
parser.add_argument('-i','--increase-step',dest="increase",help="How much to increase the frontpage_limit every step",default=INCREASE_STEP)
parser.add_argument('-d','--decrease-step',dest="decrease",help="How much to decrease the frontpage_limit every step",default=DECREASE_STEP)
parser.add_argument('-l','--download-limit',dest="limit",help="The download time limit to act on",default=DOWNLOAD_LIMIT)
parser.add_argument('-b','--buffer',dest="buffer",help="A buffer to allow more robust limits",default=BUFFER)
arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
COMPANY = arguments.company
INCREASE_STEP = arguments.increase
DECREASE_STEP = arguments.decrease
DOWNLOAD_LIMIT = arguments.limit
BUFFER = arguments.limit

def verbose(text):
    if VERBOSE:
        print text


def get_download_time(company):
    url = 'http://192.168.128.5:9090/api/v1/query'
    params = {'query': 'last_download_time{name="' + company + '"}'}

    req = requests.get(url, params=params, auth=('admin', 'admin'))
    webContent = json.loads(req.text)
    return float(webContent["data"]["result"][0]["value"][1])

def get_frontpage_limit():
        output = json.loads(subprocess.check_output(["docker service inspect bf_web"],shell=True))
        for env in (output[0]["Spec"]["TaskTemplate"]["ContainerSpec"]["Env"]):
            if "BF_FRONTPAGE" in str(env):
                print "Found flag: " + str(env)
                count=str(env).split("=")[1]
                return float(count)

# Program flow:

# 1. get download time
current_time = get_download_time()
verbose("Current dowload time: " + str(current_time))

# 2. get number of workers
current_frontpage_limit = get_frontpage_limit()
verbose("Current frontpage_limit: " + str(current_frontpage_limit))

# 3. Deside on the need to scale up or down

# if download time is below the treshold, increase by increase step
if current_time < ( DOWNLOAD_LIMIT - BUFFER ):
    verbose("There is room to scale up")
    new_frontpage_limit = current_frontpage_limit + INCREASE_STEP
    # run docker update service command
    # docker service update --env-add BF_FRONTPAGE_LIMIT=XXX --with-registry-auth bf_web

elif current_time < DOWNLOAD_LIMIT:
    verbose("We are below the limit, but within the buffer of " + BUFFER + "s")

# if download time is above the treshold, decrease by decrease step
elif current_time > DOWNLOAD_LIMIT:
    verbose("We cannot sustain the current load, decreasing the frontpage limit")
    new_frontpage_limit = current_frontpage_limit - DECREASE_STEP
    if new_frontpage_limit < 0:
        verbose("Oh no!, we can't shrink any further")
    else
        # run docker update service command
        verbose("Scaling down to " + new_frontpage_limit)
