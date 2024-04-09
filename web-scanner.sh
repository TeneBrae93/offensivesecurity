  #!/bin/bash
  # Bash script that will use nmap to find web servers and then eye-witness to get screenshots of all the web servers 

  # Check if the input file is provided
  if [ -z "$1" ]; then
    echo "Please provide a .txt file as input."
    exit 1
  fi

  # Read each line from the input file
  while IFS= read -r line; do
    # Use nmap to scan common web ports on each line (IP address or hostname)
    nmap -p 80,443,8080 -iL "$1" | grep -E '^(80|443|8080)/open' | awk '{print $2}' >> web-servers.txt
  done < "$1"

  # Run eyewitness on the web servers
  eyewitness --web -f web-servers.txt
  done < "$1"