# Very basic script which cats out all the files and searches for a specific string - specified in the script below
#!/bin/bash

# Set the directory where the .txt files are located
dir=/home/test/secret-files # Update this to the folder containing the files you are searching

# Set the password to search for
password="password" # Update this to the string you're searching for

# Loop through each .txt file in the directory
for file in "$dir"/*.txt
do
  # Search for the password in the file
  if grep -q "$password" "$file"; then
    echo "Password found in file: $file"
  else
    echo "Password not found in file: $file"
  fi
done
