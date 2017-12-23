#! /usr/bin/env python3.5
import sys
import pdb
import tempfile
import os
import subprocess
from Bio import SeqIO
import warnings
import re
from Bio.Blast import NCBIXML
import argparse

# In this file we collect all the common functions for reading files, manipulate formats etc.


# This function gets the fasta file from stdin and return the sequences
def Get_sequences():
    # get fasta file from stdin
    var = sys.argv[1:]
    filename = var[0]

    # check if the file is empty
    if os.stat(filename).st_size == 0:
        print("The file: " +filename + " is empty !!!")
        return 0

    # if the file is NOT empty proceed
    else:
        # get sequences from the file
        with open(filename, 'r') as f:
            sequences= list(SeqIO.parse(f, 'fasta'))
        return sequences


# This functions prints out (stdout) the seqences in fasta format
def PrintFasta(sequences,type):
    # print out the sequences in fasta format
    if  type == 'std':
        for sequence in sequences:
            print('>' + sequence.name)
            print(sequence.seq)


    if  type == 'KLEEK':
        for sequence in sequences:
            print('>' + sequence.name + ' This sequence contains KLEEK')
            print(sequence.seq)

    # print out the sequences in fasta format using BioPython
    elif type == 'biopython':
        for sequence in sequences:
            SeqIO.write(sequence, sys.stdout, 'fasta')

# This function whites out a fasta file
def WriteFasta(sequences):
    # write out the sequences in fasta format using BioPython
    SeqIO.write(sequences, 'infile', 'fasta')


# This function returns the translated sequences
def TranslateSeq(sequences):

    # remove warnings related to codon's lenght not a multiple of three
    warnings.filterwarnings("ignore")

    # do translation and replace the seq
    for sequence in sequences:
        sequence.seq = sequence.seq.translate()

    return sequences

# This function returns the sequences which contain a sepecific pattern
def Filter_sequences(sequences, pattern):
    filtered_seqs = []

    # Note:
    # re.search(pattern, string, flags=0) Scan through string looking
    # for the first location where the regular expression pattern produces
    # a match, and return a corresponding MatchObject

    # serach though all sequences
    for sequence in sequences:
        # append to the filtered list only those who contain KLEEK
        if re.search(pattern, str(sequence.seq)):
            filtered_seqs.append(sequence)

    return filtered_seqs



# This function gets the XML file from stdin and returns an iterator a Blast record for each query
def Get_XML():
    content =[]
    # get XML file and pattern from stdin
    for name in sys.argv[1:]:
        content.append(name)

    # isolate pattern
    pattern = content[0]
    # isolate filename
    filename = content[1]

    # if the file input is '-' read from stdin
    if filename == '-':
        filename = input("Please enter the file name: ")
    # check if the file is empty

    if os.stat(filename).st_size == 0:
        print("The file: " +filename + " is empty !!!")
        return 0

    # if the file is NOT empty proceed
    else:
        # get Blast record
        BlastRec= NCBIXML.parse(open(filename))

        return pattern, BlastRec


# This fumction gets the blast resutls and a pattern and returns the matches
# which respect the E-value threshold
def Get_BlastMatch(BlastRec, pattern, E_value):

    MatchResults = []

    for content in BlastRec:
        for record in content.alignments:
            # define new candidate
            candidate = []
            # append Query accession
            candidate.append(content.query)
            # append ID
            candidate.append(record.hit_id)
            # append Target accession
            candidate.append(record.hit_def)
            # append accession
            candidate.append(record.accession)
            for val in record.hsps:
                # append bit score
                candidate.append(val.bits)
                # append E-value
                candidate.append(val.expect)

            # Check if E_value is less than threshold and if continue
            if candidate[-1] > E_value:
                continue
            for j in [candidate[1], candidate[2], candidate[3]]:
                # search for matches (use re.IGNORECASE to perform case-insensitive matching)
                if re.search(pattern, j, re.IGNORECASE):
                    # if match append candidate to match results
                    MatchResults.append(candidate)

    # if multiple responses
    if len(MatchResults) > 1:
            # Get the match with the lowest E-value
        BestResult = [min(MatchResults, key=lambda x: x[-1])]
    else:
        BestResult = MatchResults

    return MatchResults, BestResult


# This function prints in strdout the blast maching results
def PrintBlastresults(MatchResults):
# if the list is empty print out warning msg
    if MatchResults == []:
        print("Warning: No hits")
    # For all entries print
    for match in MatchResults:

        # The Query accession: "BlastOutput_query-def"
        print(match[0], end='\t')
        # The Target accession: "Hit_def", but don't keep more than the 20 first characters!
        if len(match[2].strip('lcl|')) > 20:
            print(match[2].strip('lcl|')[:20], end='\t')
        else:
            print(match[2].strip('lcl|'), end='\t')
        # The The bit score, found in "Hsp_bit-score"
        print("{0:.1f}".format(match[-2]), end='\t')
        # E-value, found in "Hsp_evalue"
        print("{0:.1E}".format(match[-1]))


# This function gets the XML file from stdin and returns a Blast record of the input file and the name of the output file

def Get_files():
    # some tips for parser:
    # nargs='?' ->	0 or 1 arguments
    # nargs=N -> The absolute number of arguments
    # The default action is to store the argument value. In this case, if a type is provided, the value is converted to that type before it is stored
    parser = argparse.ArgumentParser(description = 'Read from the given input XML file and create a PDF with the histogram in the output file. ')
    parser.add_argument('input_file', nargs='?', help='Give the iput XML file or read from stdin if only on argument is given')
    parser.add_argument('output_filename', nargs='?', help='filename of the output PDF file (without the .pdf ending)')
    args = parser.parse_args()

    # if the input file has been given
    if args.input_file:
        # if the file input is blank read from stdin
        if args.output_filename:
            pass
        else:
            args.output_filename = input("Please enter the output file name: ")

        # check if the file is empty
        if os.stat(args.input_file).st_size == 0:
            print("The file: " + args.input_file + " is empty !!!")
            return 0, 0

        # if the file is NOT empty proceed
        else:
            # get Blast record
            BlastRec=  NCBIXML.parse(open(args.input_file))

            return BlastRec, args.output_filename
    else:
        parser.print_help()
        return 0, 0


def Get_First_Blast(BlastRec):
    FirstScores = []
    for i, content in enumerate(BlastRec):
        if i > 0: break
        for record in content.alignments:
            for val in record.hsps:
                # append bit score
                FirstScores.append(val.bits)


    return FirstScores