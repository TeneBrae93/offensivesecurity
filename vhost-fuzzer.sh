#!/bin/bash

# Function to display script usage
show_help() {
    echo "Usage: $0 <DOMAIN> <WORDLIST> <URL> <FS Filter>"
    echo "   -h, --help     Display this help and exit"
    echo
    echo "This script is a vhost fuzzer using ffuf for people who may forget the syntax."
}

# Check if the help option is provided
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Check if the required arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Error: Missing or incorrect arguments."
    show_help
    exit 1
fi

# Assign arguments to variables
DOMAIN="$1"
WORDLIST="$2"
URL="$3"
FS="$4"

# Run ffuf command
ffuf -H "Host: FUZZ.$DOMAIN" -H "User-Agent: PENTEST" -c -w "$WORDLIST" -u "$URL" -fs "$FS"
