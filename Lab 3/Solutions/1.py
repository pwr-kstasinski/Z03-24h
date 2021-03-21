import sys
import os

if len(sys.argv) <3:
    print("Not enough arguments")
    exit(1)


for f in os.listdir(sys.argv[2]):
    if f.endswith(sys.argv[1]):
        print(f)
