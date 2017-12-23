#! /usr/bin/env python3.5
import sys
import pdb
import HelpFun as hf



def main():
    files = []
    distances = []
    # get filenames from stdin and append them to list
    for filename in sys.argv[1:]:
        files.append(filename)

    # for all pairs in list
    for x_file in files:
        # create lattent list (one element per time to create row)
        _ = []
        # appent the spiece's name
        _.append(hf.GetFaNames(x_file))
        for y_file in files:

            # get the genome sequences out of the file
            genome1 = hf.ReadFasta(x_file)
            genome2 = hf.ReadFasta(y_file)
            if not genome1 or not genome2:
                print('File ' + filename + ' is empty. Try again!')
                return
            # get the related differences of genes
            diff = hf.dist(genome1, genome2)

            # append difference in lattent list
            _.append(diff)
        # appent in distaces (one column per time)
        distances.append(_)


    in_file = open("infile", "w")
    # Print the number of spieces
    in_file.write("%s\n" % len(files))

    # print the distance matrix (with accuracy ~e-3)
    hf.PrintList_file(distances, in_file)

    in_file.close()

if __name__ == '__main__':
    main()
