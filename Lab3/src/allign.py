#! /usr/bin/env python3.5

import pdb
import HelpFun as hf
import subprocess
import os


def main():

    # get the fasta file from stdin and return the sequences (prots.fa)
    sequences= hf.Get_sequences()

    # if the file is not empty proceed
    if sequences:

        # define the motif in Prosite notation
        pattern = 'KL[EI]{2,}K'

        # collect the KLEEK sequences
        filtered_seqs = hf.Filter_sequences(sequences, pattern)
        # write the filtered sequences to file
        hf.WriteFasta(filtered_seqs)

        # Call muscle and do multisequence allignment
        subprocess.call(["muscle", "-in", "infile", "-out", "multiseq"])

        # Call the alignment viewer to inspect the results
        subprocess.call(["seaview", "multiseq"])

        # remove temp files
        os.remove('infile')
        os.remove('multiseq')

if __name__ == '__main__':
    main()
