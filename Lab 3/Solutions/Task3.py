import sys

def arg_is_floating_point(arg):
  try:
      float(arg)
      return True
  except:
      return False

array_of_args = [arg for arg in sys.argv[1:] if arg_is_floating_point(arg)]
print(sorted(array_of_args))