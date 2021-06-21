import os
import sys

arg_path = sys.argv[1]
def list_catalog(cat_path, spaces, name):
	for (root, dirnames, filenames) in os.walk(cat_path):
		for d in dirnames:
			if ((d == dirnames[-1]) & (filenames == [])):
				print(spaces + "└──" + d)
				list_catalog(root + "\\" + d, spaces + "   ", d)
			else:
				print(spaces + "├──" + d)
				list_catalog(root + "\\" + d, spaces + "│  ", d)
		
		for f in filenames:
			if (f == filenames[-1]):
				print(spaces + "└──" + f)
			else:
				print(spaces + "├──" + f)
			
		break


print (arg_path)
list_catalog(arg_path,"" , "")