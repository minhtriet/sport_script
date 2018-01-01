#! /bin/bash

for folder in $1/*/; do
  for file in $folder/*.jpg; do
    mogrify -flop $file    
  done
done
