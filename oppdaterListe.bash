#!/bin/bash

source /home/ubuntu/IMT3003_V20_group08-openrc.sh

		# henter listen over alle ACTIVE servere
servLi=$(openstack server list | grep ACTIVE | awk '{print $4 ":" $8}')

for serv in $servLi
do
	###########################################################
		
		# henter ut navn og ip fra stringen
	nvn=$(echo $serv | cut -d ':' -f1)
	ip=$(echo $serv | cut -d ':' -f2 | cut -c 9- )
		
		# sjekker om det er ',' på slutten som det er på de med to ip-adresser
	if [[ $ip == *","  ]]; then   		ip=$(echo $ip | tr -d ,)
	fi
	
	###########################################################
			#Naa er alt paa et riktig format
		# så her må det bli en switch case for å sjekke alle mulige
		#	muligheter og evt hva som skal gjøres. 
		# lagre resultatene til en fil.
	case "$nvn" in 
		*Dock*)
			echo "hipp"
		;;
		#########################
		*ManagerV2*)
			echo "	HURRA"
				
		;;
		#########################
	esac
		

	#### må flytte filen til backup-server for at den har riktig liste
	# funka dårlig å kjøre dette på backup siden output blir rar...

done

