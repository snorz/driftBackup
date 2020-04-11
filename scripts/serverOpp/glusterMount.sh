#!/bin/bash

#script called from serverStartUp to mount gluster if 
#	one of docker servers are shut down
#
#----------------- PROG -----------------

read -r server


#wait 3 min? for server to start up
sleep 3m
#henter ip-adressen til server
ip=$(openstack server list | grep $server | awk '{print $8}' | cut -c 9-)


# mount glusterfs on server that is shut down /parameter sendt from other script
ssh ubuntu@$ip mount -t glusterfs 192.168.128.80:bf_config /bf_config

ssh ubuntu@$ip mount -t glusterfs server1:bf_images /bf_images


