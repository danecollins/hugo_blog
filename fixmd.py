import sys
import re

def process_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Pattern to match lines like "#*In Search of Wyland Walls.*"
        pattern = re.compile(r'^[# ]*In Search of Wyland Walls.*$')
        lines = [line for line in lines if not pattern.match(line)]

        # Remove existing subtitle
        lines = [line for line in lines if not line.startswith('subtitle:')]

        # Insert the new subtitle after the "title:" line
        for i, line in enumerate(lines):
            if line.startswith("title:"):
                lines.insert(i + 1, 'subtitle: "In Search of Wyland Walls"\n')
                break

        # Write the modified content back to the file
        with open(filename, 'w') as file:
            file.writelines(lines)

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")

def main():
    for filename in sys.argv[1:]:
        process_file(filename)

if __name__ == "__main__":
    main()
