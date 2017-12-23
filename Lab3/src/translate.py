#! /usr/bin/env python3.5
import HelpFun as hf
import pdb


def main():

    # get the fasta file from stdin and return the sequences (translationtest.dna)
    sequences= hf.Get_sequences()

    # if the file is not empty proceed
    if sequences:

        # do translation and replace the seq
        translated_seq = hf.TranslateSeq(sequences)

        # print out the translation
        hf.PrintFasta(translated_seq, 'std')

if __name__ == '__main__':
    main()
