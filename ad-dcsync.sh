#!/bin/bash 

# secretsdump.py <domain>/<username>:<password>@<ip_address> 

echo "Yay! We no longer screw up the syntax for 15 minutes!" 

echo "Domain: "
read domain

echo "Username: "
read username

echo "Password: "
read password

echo "IP Address: "
read ip_address

secretsdump.py $domain/$username:$password@$ip_address
