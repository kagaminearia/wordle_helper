#!/bin/bash

if [ ${#1} == 0 ]
then
    echo "You are getting results for wordle.png"
    python3 main.py
else
    echo "You are getting results for $1"
    python3 main.py $1
fi