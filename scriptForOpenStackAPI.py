##
##Stjålet fra Aksel & Erik
##

import openstack # openstacksdk
from getpass import getpass #password input
import argparse # arguments from CLI
import sys  # arguments from CLI



# HOW TO DOCUMENT FUNCTIONS:
# PARAMS:
# RETURNS:
# USAGE: 
# OPTIONAL TODO

# clouds.yaml: 
# Go to skyhigh -> API access -> Download OpenStack cloud.yaml File
# Place cloud.yaml in same folder as oppeScript.py

# Dependencies:
# pip3 install openstacksdk


#######################################################


# PARAMS: NONE
# RETURNS: connection to the server
# USAGE: 
# Connects to the API using 'clouds.yaml'
# 'Clouds.yaml' must be in the same folder
def connect():
    inputPass = getpass()
    conn = openstack.connect(cloud='openstack', region_name='SkyHiGh',password=inputPass)
    return conn


# PARAMS: connection returned from func connect()
# RETURNS: boolean of servers active or not
# USAGE: 
#   Checks if all servers are active.
#   if not warning is printed to screen
# TODO: Auto launch a new instance or try to get the server up    
def active(connection):
    allServersActive = True
    servers = connection.compute.servers() # get list of servers
    for server in servers:
        if server.status != "ACTIVE": # checks status of server
            print("********* WARNING: Server Down: " + server.name + "\t********")
            allServersActive = False
    return allServersActive


# PARAMS: connection returned from func connect()
# RETURNS: NONE
# USAGE:
#   Prints information of all servers both active and not
def getAllServers(connection):
    servers = connection.compute.servers()
    flavors = connection.compute.flavors()
    for server, flavor in zip(servers,flavors):
        print("Name: " + server.name)
        print("\tSize: " + flavor.name)
        print("\tRAM: " + str(flavor.ram))
        print("\tVCPUs: " + str(flavor.vcpus))
        print("\tStatus: " + server.status)


# PARAMS: connection returned from func connect()
# RETURNS: NONE
# USAGE: 
#   Create server 
# TODO: https://docs.openstack.org/openstacksdk/latest/user/guides/compute.html#id6
# See 'create server'
#def createServer(connection):



def main(argv):

    if len(sys.argv) < 2: # no arguments supplied
        print("\nNo arguments supplied.. \nFlags: ")
        print("\t-g  => \tGet all servers")
        print("\t-a  => \tCheck if servers are active")
        exit()
    conn = connect()
    parser = argparse.ArgumentParser()
    parser.add_argument('-g',action='store_true', help = 'Get all servers')
    parser.add_argument('-a',action='store_true', help = 'Check if servers are active')
    args = parser.parse_args()

    if args.g:
        getAllServers(conn)
    elif args.a:
        if active(conn):
            print("All servers are active!")


if __name__ == '__main__':
    main(sys.argv[1:])

