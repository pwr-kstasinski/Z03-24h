# get N
echo Provide the N:
read N

# set first and second number of Fibonacci series
a=0
b=1

# print N Fibonacci numbers
for (( i=0; i<N; i++ ))
do
  echo $a
  buffer=$((a + b))
  a=$b
  b=$buffer
done