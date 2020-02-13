# version 0.1
FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update 
RUN apt-get -y install apache2
RUN apt-get install libapache2-mod-php php-pgsql -y

RUN rm /var/www/html/index.html

#ADD code/* /var/www/html/ 
#ADD config.php /var/www/html/

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

EXPOSE 80

