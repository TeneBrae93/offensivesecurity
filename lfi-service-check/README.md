# LFI Service Identification Script

This script leverages a Local File Inclusion (LFI) vulnerability to identify a service running on a specified port. It was created while going through the "Airplane" room on TryHackMe. A big thank you to [n3ph0s](https://www.nephos.guru/) for sharing his original base script, which this script is built upon.

## Description

The script retrieves the command line of processes on a remote server using LFI to determine which service is running on a specified port. It uses threading to speed up the process.

## Usage

### Prerequisites

- Python 3.x
- `requests` library (install using `pip install requests`)

### Running the Script

1. Save the script to a file, for example, `lfi_service_finder.py`.
2. Run the script from the command line with the required arguments:

```sh
python3 lfi_service_finder.py -p <port_number> -t <number_of_threads>
```

![image](https://github.com/TeneBrae93/offensivesecurity/assets/86263907/8e77b67f-3f75-4314-bada-3b9312184cbc)

