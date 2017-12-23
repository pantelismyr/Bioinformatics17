#! /usr/bin/env python3.5

import sys
import tempfile
import os
import subprocess
from Bio import AlignIO
import pdb

import HelpFun as hf


def main():

    # get fasta file and # of bootsrtaps from stdin
    var = sys.argv[1:]
    if len(var) < 2:
        print('Error: You have to specify the number of bootstraps.')
        print('\n' + 'Usage: \n'+ '\t bootstrap <filename> <number of boostraps>')
        return
    filename = var[0]
    BootNum = var[1]


    # get sequences from the fasta file and asign them to sequence objects
    with open(filename, 'r') as f:
        sequence= list(AlignIO.parse(f, 'fasta'))
    if not sequence:
        print('File ' + filename + ' is empty')
        return
    sequence = sequence[0]

    # get short names and return the dictionary
    names = hf.get_name(sequence)

    # create input file for bootstrap analysis
    # with open('infile', 'w') as infile:
    #     AlignIO.write(sequence, infile, 'phylip')
    pdb.set_trace()
    with tempfile.NamedTemporaryFile() as temp:
    # temp.write(sequence)
        
        temp = open('infile', 'w')
        temp = AlignIO.write(sequence, temp, 'phylip')
    
    # run bootstrap analysis
    hf.bootstrap_analysis(BootNum)

    # return the original names to the ids and print (stdout) the consensus tree
    hf.retIDandPrint(names)

    # # remove temp files
    # os.remove('infile')
    # os.remove('intree')
    # os.remove('outtree')
    # os.remove('outfile')
    
if __name__ == '__main__':
    main()

