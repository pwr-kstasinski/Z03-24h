import sys


def isFloat(arg):
    try:
        float(arg)
        return True
    except:
        return False


args = [float(arg) for arg in sys.argv[1:] if isFloat(arg)]

print(sorted(args))
