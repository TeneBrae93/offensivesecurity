import argparse
from collections import Counter

# Function to read names from a file and return a list of unique names and duplicates.
def get_unique_and_duplicates(file_path):
    try:
        with open(file_path, 'r') as file:
            names = file.read().splitlines()
        counts = Counter(names)
        # Only names that occur exactly once are considered "unique"
        unique_names = [name for name, count in counts.items() if count == 1]
        # Names that occur more than once are listed as duplicates.
        duplicates = [name for name, count in counts.items() if count > 1]
        return unique_names, duplicates
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return [], []

# Function to write names to a new file.
def write_names(names, output_file):
    try:
        with open(output_file, 'w') as file:
            for name in names:
                file.write(name + '\n')
        print(f"Names saved to {output_file}")
    except IOError:
        print(f"Error writing to {output_file}")

# Main function.
def main():
    parser = argparse.ArgumentParser(
        description="This is a super 1337 Python script created by Tyler Ramsbey that does the following:\n"
                    "- Removes duplicate names and outputs them to 'duplicates.txt' so you can see who may have tried to cheat the system (you dirty hackers)\n"
                    "- Puts all the names that appear only once in 'unique-names.txt' for a fair drawing"
    )
    parser.add_argument("-names", required=True, help="Input file containing names")
    args = parser.parse_args()

    input_file = args.names
    unique_file = "unique-names.txt"
    duplicates_file = "duplicates.txt"

    unique_names, duplicates = get_unique_and_duplicates(input_file)

    if unique_names:
        write_names(unique_names, unique_file)
    if duplicates:
        write_names(duplicates, duplicates_file)

if __name__ == "__main__":
    main()
