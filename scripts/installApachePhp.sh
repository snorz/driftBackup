#!/bin/bash

apt-get update -y
apt-get install apache2 -y

apt-get install libapache2-mod-php php-mysql -y

apt-get install mysql-client -y
