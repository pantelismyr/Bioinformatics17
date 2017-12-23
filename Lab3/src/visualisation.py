#! /usr/bin/env python3.5

import pdb
import HelpFun as hf
import matplotlib.pyplot as plt

def main():

    # get the XML file from stdin and return the Blast record (test1.xml, test2.xml, cst_blast.xml)
    # and the pattern to match
    BlastRec, outfile= hf.Get_files()

    # pdb.set_trace()
    # if the file is not empty proceed
    if BlastRec:
        # get scores for the first Blast result
        FirstScores = hf.Get_First_Blast(BlastRec)

        # plot the score's histogram
        plt.hist(FirstScores, round(max(FirstScores)), normed=1, facecolor='blue')
        # save histogram as pdf
        plt.savefig(outfile + '.pdf')


if __name__ == '__main__':
    main()
