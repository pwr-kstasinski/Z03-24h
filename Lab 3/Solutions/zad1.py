import os
import sys

if (len(sys.argv)<2):
  print("You need to give one extension!")
  exit(-1)

ext = sys.argv[1]
if (len(sys.argv)>2):
  path = sys.argv[2]
else:
  path = "./"

for file in os.listdir(path):
  if file.endswith(ext):
    print(file)

