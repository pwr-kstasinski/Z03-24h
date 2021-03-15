# get user id
# if it is a root -> id will be equal to 0
user_id=$(id -u)

# if it is not a root -> print the info
if [ $user_id != 0 ];
then
  echo This script is not running in admin mode
fi