## Fixes SSH Keys so they are properly formatted
import sys
import re
import textwrap

def fix_ssh_key(file_path):
    try:
        with open(file_path, 'r') as file:
            messy_key = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    # Use regex to dynamically find the header, body, and footer
    match = re.search(r"(-----BEGIN .*?-----)(.*?)(-----END .*?-----)", messy_key, re.DOTALL)
    
    if not match:
        print("Error: Could not find valid SSH key boundaries (BEGIN/END headers).")
        sys.exit(1)

    header = match.group(1).strip()
    body = match.group(2)
    footer = match.group(3).strip()

    # Remove all whitespace (spaces, newlines, tabs) from the key body
    clean_body = re.sub(r'\s+', '', body)

    # Wrap the clean base64 string to 70 characters per line (Standard for OpenSSH)
    formatted_body = textwrap.fill(clean_body, width=70)

    # Reassemble the key
    fixed_key = f"{header}\n{formatted_body}\n{footer}\n"
    
    return fixed_key

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_key.py <path_to_messy_key_file>")
        sys.exit(1)
        
    fixed = fix_ssh_key(sys.argv[1])
    print(fixed)
