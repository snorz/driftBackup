#!/bin/bash

# script for å kunne gå ut eller inn av produksjon. 
#

		#for å kunne gjøre openstack kommandoer
source /home/ubuntu/IMT3003_V20_group08-openrc.sh

		# Output muligheter
echo "tast inn '1' for aa gaa ut av produksjon"
echo "tast inn '2' for aa gaa inn i produksjon"

		
read inp	#leser valg

#---------------UT AV PROD------------------------------
		# hvis vi skal gaa ut av prod:
if [ $inp == 1 ] 
then
	echo "Gaar ut av produksjon naa"
	openstack server start Docker #start en midlertidig vm
	openstack server add floating ip Docker 10.212.143.56  #flytt floating ip ^

#---------------INN I PROD------------------------------
		# for å gå inn i prod
elif [ $inp == 2 ] 
then
	echo "gaar inn i produksjon igjen!! (:"
	openstack server add floating ip varnish 10.212.143.56 #flytt floating ip til bf
	openstack server stop Docker #slå av vm med midlertidig side

else
	echo "Ikke er valid valg.! "
	echo "exiting"	
fi

