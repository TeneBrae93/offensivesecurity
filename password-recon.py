import requests
import sys
import json

def main():
    if len(sys.argv) != 4:
        print("Usage: python password-recon.py [TARGET-DOMAIN] [USERNAME] [API-KEY]")
        print("Note: Requires an active DeHashed.com account and API Key")
        print("Author: Tyler Ramsbey from Hack Smarter - https://hacksmarter.org")
        return

    target_domain = sys.argv[1]
    username = sys.argv[2]
    apikey = sys.argv[3]

    url = f"https://api.dehashed.com/search?query=domain:{target_domain}&size=10000"
    headers = {
        "Accept": "application/json"
    }
    auth = (username, apikey)

    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()

        data = response.json()
        if "entries" in data and data["entries"]:
            entries = data["entries"]
            filtered_entries = [entry for entry in entries if entry.get("email") and entry.get("password")]
            formatted_entries = [f"{entry['email']}:{entry['password']}" for entry in filtered_entries]
            unique_entries = sorted(set(formatted_entries))

            with open("emails_passwords.txt", "w") as file:
                file.write("\n".join(unique_entries))
            print("Results saved to emails_passwords.txt")
        else:
            print("The target domain does not have any dehashed results.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()