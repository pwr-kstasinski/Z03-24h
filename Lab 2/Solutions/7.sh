# get the N
echo Provide the N:
read N

# initialize the result value
result=1

# calculate the factorial
for (( i=N; i>0; i-- ))
do
  result=$((result * i))
done

# print the result
echo $result