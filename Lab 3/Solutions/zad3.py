import os
import sys

if (len(sys.argv) == 1):
  print("You need to at least one number!")
  exit(-1)

numbers = sys.argv[1:]
numbers.sort()
print(numbers)