#!/bin/bash

FILES=circle-flags/flags/*.svg
for f in $FILES
do
    convert -background none $f "${f%.svg}.png" 
done
