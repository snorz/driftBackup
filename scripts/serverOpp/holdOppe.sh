#!/bin/bash

source /home/ubuntu/IMT3003_V20_group08-openrc.sh

for server in db1 Balancer Docker; do
	if [ "$(openstack server list | grep -w $server | awk '{print $6}')" != "ACTIVE" ] ; then
		echo "starter server $server : $(date)"
		$(openstack server start $server)
		
	fi
done
