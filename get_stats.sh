#!/bin/bash

while [ 1 ]
do
    ps -p 6344 -o %cpu,%mem >> performance.txt 
done
