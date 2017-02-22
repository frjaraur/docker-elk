#!/bin/bash

for I in {1..10}
do
	printf "data$I=$(( ( RANDOM % 10 )  + 1 ));"
done
echo

