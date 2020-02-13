#!/bin/bash

#how to install docker : 
# 
# sudo apt-get update
# sudo apt-get install \

# apt-transport-https \#!/bin/bash

#how to install docker : 
 
sudo apt-get update -y
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common 

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs)  stable" 

sudo apt-get install docker-ce docker-ce-cli containerd.io -y

