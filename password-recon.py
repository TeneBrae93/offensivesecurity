import requests
import sys
import subprocess
import json

def main():
    if len(sys.argv) != 4:
        print("Usage: python password-recon.py [TARGET-DOMAIN] [USERNAME] [API-KEY]")
        print("Note: Requires an active DeHashed.com account and API Key")
        print("Author: Tyler Ramsbey from Hack Smarter - https://hacksmarter.org")
        return

    target_domain = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    url = f"https://api.dehashed.com/search?query=domain:{target_domain}&size=10000"
    url = url.replace("[DOMAIN]", target_domain)
    url = url.replace("[USERNAME]", username)
    url = url.replace("[API-KEY]", password)
    headers = {
        "Accept": "application/json"
    }
    auth = (username, password)

    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()

        with open("dehashed_results.txt", "w") as file:
            file.write(response.text)
            try:
                with open("dehashed_results.txt", "r") as file:
                    data = json.load(file)
                    entries = data["entries"]
                    filtered_entries = [entry for entry in entries if entry.get("email") and entry.get("password")]
                    formatted_entries = [f"{entry['email']}:{entry['password']}" for entry in filtered_entries]
                    unique_entries = sorted(set(formatted_entries))
                with open("emails_passwords.txt", "w") as file:
                    file.write("\n".join(unique_entries))
                print("Results saved to emails_passwords.txt")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
        print("Results saved to dehashed_results.txt")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()