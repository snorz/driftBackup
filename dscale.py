#!/usr/bin/python
import subprocess
import argparse
import json
import urllib2
import requests

parser = argparse.ArgumentParser(prog='dscale.py')
parser.add_argument('-v', '--verbose', dest="verbose", help='Turn verbosity on', default=False, action="store_true")
parser.add_argument('-c', '--company', dest="company", help='Company name', required=True)
parser.add_argument('-s', '--service', dest="service", help="The bf service name", default="bf_web")
parser.add_argument('-i', '--increase-step', dest="increase", help="How much to increase the frontpage_limit every step", default=100)
parser.add_argument('-d', '--decrease-step', dest="decrease", help="How much to decrease the frontpage_limit every step", default=100)
parser.add_argument('-l', '--download-limit', dest="limit", help="The download time limit to act on", default=1.5)
parser.add_argument('-b', '--buffer', dest="buffer", help="A buffer to allow more robust limits", default=0)
arguments = parser.parse_args()

VERBOSE = arguments.verbose
COMPANY = arguments.company
SERVICE = arguments.service
INCREASE_STEP = arguments.increase
DECREASE_STEP = arguments.decrease
DOWNLOAD_LIMIT = arguments.limit
BUFFER = arguments.limit


def verbose(text):
    if VERBOSE:
        print(text)


def get_download_time(company):
    try:
        url = f"http://imt3003.skyhigh.iik.ntnu.no:9001/imt3003_report_last_100_{company}.json"
        req = requests.get(url)
        web_content = json.loads(req.text)
        for entry in web_content["reports"]:
            if entry["type"] == "webcheck":
                return float(entry["time_to_download"])
        print("Could not find download time.")
        exit(1)
    except (ConnectionError, JSONDecodeError):
        print("Failed to query data endpoint.")
        exit(1)


def get_frontpage_limit():
    output = json.loads(subprocess.check_output([f"docker service inspect {SERVICE}"], shell=True))
    for line in str(output[0]["Spec"]["TaskTemplate"]["ContainerSpec"]["Env"]):
        if "BF_FRONTPAGE" in line:
            print(f"Found flag: {line}")
            count = line.split("=")[1]
            return float(count)


# Program flow:
# 1. get download time
current_time = get_download_time(COMPANY)
verbose(f"Current download time: {current_time}")

# 2. get number of workers
current_frontpage_limit = get_frontpage_limit()
verbose(f"Current frontpage_limit: {current_frontpage_limit}")

# 3. Decide on the need to scale up or down
# if download time is below the threshold, increase by increase step
if current_time < DOWNLOAD_LIMIT - BUFFER:
    verbose("There is room to scale up")
    new_frontpage_limit = current_frontpage_limit + INCREASE_STEP
    # run docker update service command
    # docker service update --env-add BF_FRONTPAGE_LIMIT=XXX --with-registry-auth bf_web

elif current_time < DOWNLOAD_LIMIT:
    verbose(f"We are below the limit, but within the buffer of {BUFFER}s")

# if download time is above the threshold, decrease by decrease step
elif current_time > DOWNLOAD_LIMIT:
    verbose("We cannot sustain the current load, decreasing the frontpage limit")
    new_frontpage_limit = current_frontpage_limit - DECREASE_STEP
    if new_frontpage_limit < 0:
        verbose("Oh no!, we can't shrink any further")
    else:
        # run docker update service command
<<<<<<< HEAD
        verbose("Scaling down to " + new_frontpage_limit)
=======
        verbose(f"Scaling down to {new_frontpage_limit}")
>>>>>>> 474d5597f8126c82eaf577ef780e2acaaa1a1b7b
