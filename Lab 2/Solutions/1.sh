# get extension
echo Provide the extension:
read extension

# get path
echo Provide the path:
read path

# list files with $extension in provided $path directory
for file in $path/*.$extension
do
  echo $file
done