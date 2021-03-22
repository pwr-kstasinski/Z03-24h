import sys
import os

amount_of_arguments = len(sys.argv)

if amount_of_arguments <= 2 or amount_of_arguments > 3:
    print("Invalid parameter(s). The pattern is the following:\n"
          ">> python Task1.py <extension_of_file> <path_of_directory>\n")
    exit(-1)

extension_of_file = sys.argv[1]
path_of_directory = sys.argv[2]

if not os.path.isdir(path_of_directory):
    print("The system cannot find the specified path")
    sys.exit()

no_files_found = True

for file in os.listdir(path_of_directory):
    if os.path.isfile(os.path.join(path_of_directory, file)) and file.endswith(extension_of_file):
        print(file)
        no_files_found = False

if no_files_found:
    print("Any files have not been found")

print("The script has been completed successfully\n")