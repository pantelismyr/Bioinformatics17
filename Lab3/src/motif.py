#! /usr/bin/env python3.5

import pdb
import HelpFun as hf


def main():

    # get the fasta file from stdin and return the sequences (prots.fa)
    sequences= hf.Get_sequences()

    # if the file is not empty proceed
    if sequences:

        # define the motif in Prosite notation
        pattern = 'KL[EI]{2,}K'

        # collect the KLEEK sequences
        filtered_seqs = hf.Filter_sequences(sequences, pattern)

        # print the KLEEKs in stdout
        hf.PrintFasta(filtered_seqs, 'KLEEK')
        # print the number of KLEEK sequences
        # pdb.set_trace()
        print('\n' + 'There are ' + str(len(filtered_seqs)) +' KLEEK sequences in the file')


if __name__ == '__main__':
    main()
