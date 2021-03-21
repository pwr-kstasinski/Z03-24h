
import sys
import os

if len(sys.argv) < 3:
    print("Not enough arguments")
    sys.exit()

os.system("dir /b \"{}\\*.{}\"".format(sys.argv[1],sys.argv[2]))