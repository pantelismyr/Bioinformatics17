#!/bin/bash

# get all input files

for item in "$@"
do
	files+=($item)
done
clear

# makes sure that the python files are executable
chmod +x basedist.py
chmod +x mkcormat.py


echo "####################################################################" 
echo "Pass the files to basedist python script to get correlation matrix"
echo "The mkcormat python script prints (stdout) the correlation matrix of"
echo "the given genome files"
echo "####################################################################" 
#read -p "Press Enter to continue"
./basedist.py ${files[@]}


echo "####################################################################" 
echo "Pass the files to mkcormat python script to get infile as output"
echo "The mkcormat python script saves as infile the correlation matrix of"
echo "the given genome files"
echo "####################################################################" 
#read -p "Press Enter to continue"
./mkcormat.py ${files[@]}

echo "####################################################################" 
echo "Run Phylip's program neighbor to estimate the phylogenetic tree "
echo "given the infile from the above phase"
echo "####################################################################" 
#read -p "Press Enter to continue" 
printf "%s\n" r y r | phylip neighbor infil

# move the files to the Data/baseFiles/results
mkdir ../Data/baseFiles/results
mv -f outfile ../Data/baseFiles/results
mv -f outtree ../Data/baseFiles/results

# remove infile
rm infile
