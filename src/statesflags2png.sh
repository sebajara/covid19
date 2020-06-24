#!/bin/bash

FILES=flags/svg/us/*.svg
for f in $FILES
do
    convert -background none -resize 400x $f "${f%.svg}.png" 
done
