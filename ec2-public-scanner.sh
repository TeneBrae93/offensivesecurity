# This tool will scan an AWS account for public EC2s. It will save these IPs to target.txt and then run an nmap scan against them for more information. 
#!/bin/bash

print_help() {
    echo "This is a tool that finds public EC2 instances in an AWS account and returns their public IP addresses. The public ones will be stored to target.txt"
    echo "Usage: $0 <AWS_PROFILE_NAME> <AWS_REGION>"
}

if [ $# -ne 2 ]; then
    print_help
    exit 1
fi

AWS_PROFILE=$1
AWS_REGION=$2

echo "EC2 Public IP Finder is a tool that finds public EC2 instances in an AWS account and returns their public IP addresses. If they are public, it will be echoed to the screen in green writing as well as saved to 'targets.txt' for manual enumeration. Enjoy!"
echo "By Tyler Ramsbey"

for instance in $(aws ec2 describe-instances --profile "$AWS_PROFILE" --region "$AWS_REGION" --filters "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].InstanceId" --output text); do
    public_ip=$(aws ec2 describe-instances --profile "$AWS_PROFILE" --region "$AWS_REGION" --instance-ids "$instance" --query "Reservations[].Instances[].PublicIpAddress" --output text)
    if [[ -n "$public_ip" ]]; then
        echo -e "\033[32mInstance $instance has public IP $public_ip\033[0m"
        echo "$public_ip" >> targets.txt
    else
        echo -e "\033[31mInstance $instance does not have a public IP\033[0m"
    fi
done

if [ -s targets.txt ]; then
    echo "Running nmap scan on public IPs found in targets.txt"
    nmap -sS -T4 -Pn -n -iL targets.txt -oN nmap_scan_results.txt
else
    echo "No public IPs found, skipping nmap scan."
fi
