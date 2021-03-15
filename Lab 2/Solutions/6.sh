show_directories() {
  for directory in $1/*/
  do
    if [ "${directory: -2}" != "*/" ];
    then
      directory_name=$(basename $directory)
      spaces=$2
      echo -e "$spaces$directory_name"
      spaces="$spaces\t"
      show_directories $directory $spaces
    fi
  done
}

show_directories . ""