#!/bin/bash

sudo apt-get update -y

sudo apt-get install apache2 libapache2-mod-php php-pgsql -y

sudo apt-get install git -y


git clone  https://git.cs.hioa.no/kyrre.begnum/bookface.git

cd bookface

rm /var/www/html/index.html

cp code/* /var/www/html/

wget https://raw.githubusercontent.com/snorz/driftBackup/master/config.php 
mv config.php /var/www/html/
