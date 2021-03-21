
import sys

for i in range(1,len(sys.argv),1):
    isSorted=True
    for j in range(1,len(sys.argv)-1):
        if float(sys.argv[j]) > float(sys.argv[j+1]):
            isSorted=False
            temp = sys.argv[j]
            sys.argv[j] = sys.argv[j+1]
            sys.argv[j+1] = temp
    if isSorted:
        break

print(sys.argv[1:])

