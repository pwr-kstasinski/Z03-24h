# get source path
echo Provide the source:
read source_path

# get destination path
echo Provide the destination:
read destination_path

# save source directory structure
source_structure=$(find $source_path -type d)

# create a copy of source structure in the destination
for directory in $source_structure
do
  mkdir $destination_path/$directory
done