import os
import sys

if (len(sys.argv) == 1):
  print("You need to give path!")
  exit(-1)

def recursive_listing(given_path, space):
  for root, dirs, files in os.walk(given_path):
    for d in dirs:
      if ((d == dirs[-1]) & (files == [])):
        print(space + "└─" + d)
        recursive_listing(root + "\\" + d, space + "  ")
      else:
        print(space + "├─" + d)
        recursive_listing(root + "\\" + d, space + "| ")
    for f in files:
      if (f == files[-1]):
        print(space + "└─" + f)
      else:
        print(space + "├─" + f)
    break
recursive_listing(sys.argv[1], "")