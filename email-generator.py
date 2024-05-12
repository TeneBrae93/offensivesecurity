# Creates an email permutation based on full name and domain because I cannot find the right tool when I need to do this 
#!/usr/bin/env python3
import argparse

def generate_emails(full_name, domain):
    names = full_name.lower().split()
    if len(names) < 2:
        print("Please provide a full name with at least two parts (e.g., 'John Doe').")
        return []

    first_name = names[0]
    last_name = names[-1]
    first_initial = first_name[0]
    last_initial = last_name[0]

    # Define all email permutations
    permutations = [
        f"{first_name}@{domain}",
        f"{last_name}@{domain}",
        f"{first_name}.{last_name}@{domain}",
        f"{first_initial}{last_name}@{domain}",
        f"{first_initial}.{last_name}@{domain}",
        f"{first_name}{last_initial}@{domain}",
        f"{first_name}.{last_initial}@{domain}",
        f"{first_initial}{last_initial}@{domain}",
        f"{first_initial}.{last_initial}@{domain}",
        f"{last_name}{first_name}@{domain}",
        f"{last_name}.{first_name}@{domain}",
        f"{last_name}{first_initial}@{domain}",
        f"{last_name}.{first_initial}@{domain}",
        f"{last_initial}{first_name}@{domain}",
        f"{last_initial}.{first_name}@{domain}",
        f"{last_initial}{first_initial}@{domain}",
        f"{last_initial}.{first_initial}@{domain}"
    ]

    return permutations

def main():
    parser = argparse.ArgumentParser(description="Generate email permutations based on full name and domain.")
    parser.add_argument("domain", help="Domain for the email addresses")
    parser.add_argument("full_name", help="Full name to base the email addresses on")
    args = parser.parse_args()

    emails = generate_emails(args.full_name, args.domain)

    if emails:
        # Write the email permutations to a file
        with open("emails.txt", "w") as f:
            for email in emails:
                f.write(email + "\n")
        print("Emails have been written to emails.txt")
    else:
        print("No emails generated; check the provided full name.")

if __name__ == "__main__":
    main()
