# Simply Python script that just removes all informationals from .nessus file so it's easier to import into tooling with less noise 

import xml.etree.ElementTree as ET
import sys
import os

def filter_informational_findings(input_file, output_file):
    try:
        print(f"Parsing {input_file}...")
        # Parse the Nessus XML file
        tree = ET.parse(input_file)
        root = tree.getroot()

        removed_count = 0

        # Find all ReportHost elements
        for report_host in root.findall('.//ReportHost'):
            # Find all ReportItem elements within the ReportHost
            # We use list() to safely iterate while modifying the tree
            for report_item in list(report_host.findall('ReportItem')):
                severity = report_item.get('severity')
                
                # In Nessus: 0=Info, 1=Low, 2=Medium, 3=High, 4=Critical
                if severity == '0':
                    report_host.remove(report_item)
                    removed_count += 1

        # Write the modified XML tree to the output file
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Successfully removed {removed_count} informational findings.")
        print(f"Filtered report saved to: {output_file}")

    except ET.ParseError as e:
        print(f"Error parsing XML. Is this a valid .nessus file? Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_nessus.py <input.nessus> <output.nessus>")
        sys.exit(1)

    input_nessus = sys.argv[1]
    output_nessus = sys.argv[2]

    if not os.path.isfile(input_nessus):
        print(f"Error: Input file '{input_nessus}' does not exist.")
        sys.exit(1)

    filter_informational_findings(input_nessus, output_nessus)
