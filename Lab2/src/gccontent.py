#! /usr/bin/env python3.5
import sys
import pdb
import HelpFun as hf



def main():
    # get filenames from stdin (for n inputs)
    for filename in sys.argv[1:]:
        # get the genome sequence out of the file
        genome = hf.ReadFasta(filename)
        if not genome:
            print('File ' + filename + ' is empty. Try again!')
            return
        # get the GC content for th[is file
        GC = hf.GC_content(genome)
        # print the GC content (with accuracy ~e-3)
        print("%.3f" % GC)

if __name__ == '__main__':
    main()
    # Note: we need the CG content for hierarchical classification