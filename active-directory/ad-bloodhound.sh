#!/bin/bash 

# I always messed up the bloodhound-python syntax. This simplifies the process and asks the users for each parameter and fires off the bloodhound-python
# bloodhound-python -d <domain> -u <username> -p <password> -gc <domain> -c all -ns <ip of domain> 

echo "Domain: "
read domain 

echo "Username: "
read username

echo "Password: "
read password

echo "IP of Domain: " 
read ip_address

bloodhound-python -d $domain -u $username -p $password -gc $domain -c all -ns $ip_address
