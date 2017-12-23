#! /usr/bin/env python3.5
import sys
import pdb
import HelpFun as hf

def main():
    # get filenames from stdin (for n inputs)
    for filename in sys.argv[1:]:
        # get the name of the spiece
        spiece = hf.GetName(filename)
        if not spiece:
            print('File ' + filename + ' is empty. Try again!')
            return
        # get the genome sequence out of the file
        genome = hf.ReadFasta(filename)
        # print the length of the sequence
        print("The Genome size for the " + spiece + " is: " + str(len(genome)))

if __name__ == '__main__':
    main()
