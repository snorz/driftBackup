#!/usr/bin/python

import os
import shutil
import argparse

###########################################
# Extra stuff
parser = argparse.ArgumentParser(prog='pull_backup.py')
parser.add_argument('-v', '--verbose', dest="verbose", help='Turn verbosity on', default=False, action="store_true")
parser.add_argument('-d', '--debug', dest="debug", help='Turn debug_messages on', default=False, action="store_true")
parser.add_argument('-c', '--config', dest="config", help='What config file to use', metavar="FILE", default="/etc/backup.conf")
parser.add_argument('-i', '--iterations', dest="iterations", type=int, help='How many backup iterations to do', metavar="N", default=7)
parser.add_argument('-b', '--backup-directory', dest="backup_folder", help="Where to keep the backup files", metavar="FOLDER", default="/backups/")
arguments = parser.parse_args()

VERBOSE = arguments.verbose
DEBUG = arguments.debug
ITERATIONS = arguments.iterations
BACKUP_FOLDER = arguments.backup_folder
SCP_USER = "ubuntu@"
##########################################


def verbose(text):
    if VERBOSE:
        print(text)


def debug(text):
    if DEBUG:
        print(text)


verbose(f"Opening config file: {CONFIG}")
with open(CONFIG) as config:
    for line in config:
        verbose(f"Read line: {line}")
        config_list = line.split(":")
        host = config_list[0]
        path_list = config_list[1].split(",")
        verbose(f"host: {host}")

        # step 0: Check there is a backup folder
        host_backup_path = BACKUP_FOLDER + host
        if not os.path.isdir(host_backup_path):
            verbose(f"Creating backup folder {host_backup_path}")
            os.makedirs(host_backup_path)
        
        # Step 1: remove the oldest folder
        if os.path.isdir(f"{host_backup_path}.{ITERATIONS}"):
            verbose("Deleting oldest version of backup directories")
            shutil.rmtree(f"{host_backup_path}.{ITERATIONS}")
            
        # step 2: move the other folders up
        for i in range(ITERATIONS - 1, 0, -1):
            debug(f"Checking if {i}th folder exists")
            if os.path.isdir(f"{host_backup_path}.{i}"):
                verbose(f"Moving {host_backup_path} from {i} to {i + 1}")
                shutil.move(f"{host_backup_path}.{i}", f"{host_backup_path}.{i + 1}")

        # step 3: cp -al the current folder
        # shutil.copytree(host_backup_path, host_backup_path + ".1", copy_function=os.link)
        verbose("Copying main folder with hard links")
        os.system(f"cp -al {host_backup_path} {host_backup_path}.1")

        # step 4: sync the current folder
        verbose("Synchronizing folders")
        for folder in pathlist:
            folder = folder.rstrip()
            verbose(f"-> {folder}")
            if not os.path.isdir(host_backup_path + folder):
                os.makedirs(host_backup_path + folder)

            os.system(f"rsync -a{'v' if VERBOSE else ''} --delete {SCP_USER}{host}:{folder} {host_backup_path}{folder}")
