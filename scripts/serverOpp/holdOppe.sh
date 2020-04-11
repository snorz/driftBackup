#!/bin/bash

source /home/ubuntu/IMT3003_V20_group08-openrc.sh

for server in db1 ManagerDock DockWork1 DockWork2 Balancer backup ; do
	if [ "$(openstack server list | awk '{print $4, $6}' | grep -w "$server" | awk '{print $2}')" != "ACTIVE" ] ; then
		echo "starter server $server : $(date)"
		$(openstack server start $server)
		
	fi
done
