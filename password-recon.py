import argparse
import requests
import sys

def search_dehashed(api_key, domain):
    url = "https://api.dehashed.com/v2/search"
    headers = {
        "Content-Type": "application/json",
        "Dehashed-Api-Key": api_key
    }

    page = 1
    size = 10000  # Max size allowed by the V2 API
    max_results = 50000  # Hard limit for pagination mentioned in docs
    
    extracted_credentials = set()
    
    print(f"[*] Searching DeHashed for: {domain}...")

    while True:
        # Prevent exceeding the hard limit
        if (page * size) > max_results:
            print("[!] Pagination limit reached (50,000 records). Stopping early.")
            break

        payload = {
            "query": domain,
            "page": page,
            "size": size,
            "de_dupe": True
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"[!] Error querying API: {e}")
            if e.response is not None:
                print(f"[!] Response: {e.response.text}")
            sys.exit(1)

        entries = data.get("entries")
        
        # If no entries are returned, we have reached the end
        if not entries:
            break

        for entry in entries:
            # Safely extract passwords, usernames, and emails
            passwords = entry.get("password") or []
            usernames = entry.get("username") or []
            emails = entry.get("email") or []

            # Filter out empty/null passwords to ensure we only get cleartext
            valid_passwords = [p.strip() for p in passwords if p and p.strip()]
            
            if not valid_passwords:
                continue

            # Combine emails and usernames into one list of login IDs
            logins = [u.strip() for u in (usernames + emails) if u and u.strip()]

            if not logins:
                continue

            # Map all valid logins to their corresponding cleartext passwords
            for login in logins:
                for pwd in valid_passwords:
                    extracted_credentials.add((login, pwd))

        total_results = data.get("total", 0)
        
        # Stop paginating if we've fetched everything available
        if (page * size) >= total_results:
            break
            
        page += 1

    return extracted_credentials


def main():
    parser = argparse.ArgumentParser(description="Query DeHashed V2 API for cleartext credentials.")
    parser.add_argument("--api-key", required=True, help="Your DeHashed API Key")
    parser.add_argument("--domain", required=True, help="The domain to search for (e.g., example.com)")
    
    args = parser.parse_args()

    credentials = search_dehashed(args.api_key, args.domain)

    if not credentials:
        print("[-] No cleartext credentials found.")
        sys.exit(0)

    print(f"\n[+] Found {len(credentials)} unique cleartext credentials:")
    print("-" * 40)
    for login, pwd in sorted(credentials):
        print(f"{login}:{pwd}")


if __name__ == "__main__":
    main()
