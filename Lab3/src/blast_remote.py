#! /usr/bin/env python3.5

import pdb
import HelpFun as hf
from Bio.Blast import NCBIWWW

def main():

    # get the fasta file from stdin and return the sequence (cst3.fa)
    sequence= hf.Get_sequences()[0]

    # if the file is not empty proceed
    if sequence:
        # Do Blast search of a given protein sequence against the nr database at NCBI
        # https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome
        # see NCBIWWW documentation at http://biopython.org/DIST/docs/tutorial/Tutorial.html (chapter 7.1)

        # invoke the NCBI BLAST server over the internet
            # The first argument is the blast program to use for the search ('blastp' in our case)
            # The second argument specifies the databases to search against ('nr' in our case)
            # The third argument is a string containing your query sequence
        result_handle = NCBIWWW.qblast("blastp", "nr", sequence.seq)
        # print out the results (stdout)
        print(result_handle.read())

if __name__ == '__main__':
    main()
