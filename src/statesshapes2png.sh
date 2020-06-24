#!/bin/bash

FILES=state-svg-defs/SVG/*.svg
for f in $FILES
do
    convert -background none $f "${f%.svg}.png" 
done
