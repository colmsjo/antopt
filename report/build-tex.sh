#!/bin/bash

for i in $( ls *.tex ); do
  echo compiling: $i
  pdflatex $i
done

for i in $( ls *.aux ); do
  echo compiling: $i
  bibtex $i
done

for i in $( ls *.tex ); do
  echo compiling: $i
  echo compiling: $i
  pdflatex $i
done

