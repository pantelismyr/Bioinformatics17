#! /usr/bin/env python3.5

import pdb
import HelpFun as hf

def main():

    # get the XML file from stdin and return the Blast record (test1.xml, test2.xml, cst_blast.xml)
    # and the pattern to match
    pattern, BlastRec= hf.Get_XML()

    # if the file is not empty proceed
    if BlastRec:

        # set E-value upper limit
        E_value = 10**-20

        # get the blast matches basted on the pattern and the E-value
        MatchResults, BestResult = hf.Get_BlastMatch(BlastRec, pattern, E_value)

        # print out in stdout the matches
        hf.PrintBlastresults(MatchResults)
        if len(MatchResults) < 2:
            return
        print()
        # print out in stdout the best match
        print('The Best result (Smaller E-value) is:')
        hf.PrintBlastresults(BestResult)

if __name__ == '__main__':
    main()
