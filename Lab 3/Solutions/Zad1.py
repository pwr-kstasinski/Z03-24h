#mozna wygodniej glob'em (glob.glob(argv[1] + '*.' + argv[2])
import os
import sys

files = []
extension = "." + sys.argv[1]
for(dirpath, dirnames, filenanmes) in os.walk(sys.argv[2]):
	files.extend(filenanmes)
	break #zeby nie wypisywal subfolderow

for f in files:
	if (f.endswith(extension)):
		print (f)
