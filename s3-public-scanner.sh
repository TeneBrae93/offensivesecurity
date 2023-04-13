#!/bin/bash

print_help() {
    echo "This is a tool that enumerates S3 buckets and returns the ones which are public. The public ones will be stored to buckets.txt"
    echo "Usage: $0 [AWS_PROFILE_NAME]"
}

while getopts "h?:" opt; do
    case "$opt" in
    h|\?)
        print_help
        exit 0
        ;;
    esac
done


echo "-------------------------------"
echo "S3 Public Scanner is a tool that enumerates S3 Buckets in an AWS account to see if any are public." 
echo "If they are public, it will be echoed to the screen in green writing as well as saved to 'buckets.txt' for manual enumeration." 
echo "Enjoy! -Tyler Ramsbey"
echo "-------------------------------"

for BUCKET in $(aws s3api list-buckets --query "Buckets[].Name" --output text); do
  if aws s3api get-bucket-acl --bucket $BUCKET | grep -q "URI=\"http\|URI=\"https";
    then echo -e "\033[32mBucket $BUCKET is public\033[0m";
    echo "$BUCKET" >> buckets.txt;
  else
    echo -e "\033[31mBucket $BUCKET is not public\033[0m";
  fi;
done
