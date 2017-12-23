#! /usr/bin/env python3.5
import pdb
import tempfile
import os
import subprocess
from Bio import AlignIO


# In this file we collect all the common functions for reading files, manipulate formats etc.

# This function reads a fasta file and return the pure genome sequence
def ReadFasta(filename):
    try:
        # with open file read the lines
        genome = []
        with open(filename, "r") as f:
            content = f.readlines()
            # if the content is empty raise error and return
            if content == '':
                raise IOError

            else:
                for cont in content:
                    # pdb.set_trace()
                    # if it is the 1st line skip it as it does not contain genome sequence (fasta format)
                    if cont[0] == '>':
                        continue
                    # else (normal run) append the lines to the genome
                    else:
                        genome.append(cont)
        # concatenate the list
        genome = ''.join(genome)
        # clean the genome list from letters other than ATGC
        genome = [s for s in genome if 'A' in s or 'T' in s or 'C' in s or 'G' in s]

        return genome
    except IOError:
        print('ERROR: Empty File!')

# This function returns the name of the genome's spiece
# WARNING: it works assuming that the fasta file follows the NCBI format
def GetName(filename):
    # open file and get contents
    with open(filename, "r") as f:
        content = f.readlines()
    if not content:
        return 0
    # splits the contents of the 1st line
    s_cont = content[0].split(' ')
    # join the 2nd and the 3rd s_cont i.e. get the name
    name = ' '.join([s_cont[1],s_cont[2]])

    return name

# This function computes the GC content of a sequence
def GC_content(genome):
    # count the occurances of each nucleodite
    Adenine = genome.count('A')
    Thymine = genome.count('T')
    Cytosine = genome.count('C')
    Guanine = genome.count('G')

    # compute the GC content
    GC = (Guanine + Cytosine) / (Adenine + Thymine + Guanine + Cytosine)

    return GC

# this function gets 2 genomes and returns the difference
# in composition (defined by distance)
def dist(genome1, genome2):

    # count the ratio of each nucleodite for the 1st genome
    Adenine1 = genome1.count('A') /len(genome1)
    Thymine1 = genome1.count('T') /len(genome1)
    Cytosine1 = genome1.count('C') /len(genome1)
    Guanine1 = genome1.count('G') /len(genome1)

    # count the ratio of each nucleodite 2nd genome
    Adenine2 = genome2.count('A') /len(genome2)
    Thymine2 = genome2.count('T') /len(genome2)
    Cytosine2 = genome2.count('C') /len(genome2)
    Guanine2 = genome2.count('G') /len(genome2)

    # compute the distance of the 2 genes (element-wise)

    A_diff = Adenine1 - Adenine2
    T_diff = Thymine1 - Thymine2
    C_diff = Cytosine1 - Cytosine2
    G_diff = Guanine1 - Guanine2

    # Get the mean
    mean = (1/4) *( A_diff**2 + T_diff**2 + C_diff**2 + G_diff**2 )

    # Get the rms

    rms_dist = mean**(1/2)

    return rms_dist

def PrintList(LiSt):
    for row in LiSt:
        for i, element in enumerate(row):
            # if it's in the 1st column print the name
            if i ==0:
                print(element, end="\t")
            # else print the distance
            else:
                print("%.3f" % element, end="\t")
        print()

def PrintList_file(LiSt, in_file):
    for row in LiSt:
        for i, element in enumerate(row):
            # if it's in the 1st column print the name
            if i == 0:
                in_file.write("%s\t" % element)
            # else print the distance
            else:
                in_file.write("%.3f\t" % element)
        in_file.write("\n")

# This function returns the name of the genome's name
# WARNING: it works assuming that the fasta file follows the std format
def GetFaNames(filename):
    # open file and get contents
    with open(filename, "r") as f:
        content = f.readlines()

    # get the first line without the '>'
    line = content[0][1:]
    # join the 1st line
    line = ''.join(line)
    # get only the fist name
    text = line.partition(" ")[0]
    # clean up the fist name in case of test files
    name = text.partition("\n")[0]
    # in the name is less that 10 characters add spaces
    addSpace = [' ']*(10-len(name))
    name += ''.join(addSpace)
    # get the fist 10 leters of the name
    name = name[:10]

    return name


# This function changes the ID names and defines a corresponding dictionary
def get_name(sequence):
    nameDic = {}
    for i in range(len(sequence)):
        key = 'GenID' + str(i+1)
        nameDic[key] = sequence[i].id
        sequence[i].id = key

    return nameDic


# This function returns the original names to the ids and prints out (stdout) the consensus tree
def retIDandPrint(ID_Dic):
    with open('outtree', "r") as f:
        for line in f.readlines():
            nl = line
            for key in ID_Dic.keys():
                nl = nl.replace(key, ID_Dic[key])
            print(nl, end='')



# This funcion performs bootstrap analysis on protein alignmens
def bootstrap_analysis(BootNum):

    # First, we run Seqboot to take the original data set and produce a large number of bootstrapped data sets
    # run Seqboot
    run_prg = subprocess.Popen(['phylip', 'seqboot'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # handle the inner process
    in_handler = 'r\n' + str(BootNum) + '\ny\n1\nr\n'
    run_prg.communicate(input=in_handler.encode('utf-8'))
    # remove and/or rename temp files
    os.remove('infile')
    os.rename('outfile', 'infile')

    # Then we find the phylogeny estimate for each of these.
    # (We don't use the seggested method "Dnapars". Instead we use "Protpars" as it uses new method,
    # intermediate between the approaches of Eck and Dayhoff (1966) and Fitch (1971))
    # run protpars
    run_prg = subprocess.Popen(['phylip', 'protpars'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # handle the inner process
    in_handler = 'y\nm\n\d\n' + str(BootNum) + '\n1\n1\ny\nr\n'
    run_prg.communicate(input=in_handler.encode('utf-8'))
    # remove and/or rename temp files
    os.remove('infile')
    os.rename('outtree', 'intree')
    os.rename('outfile', 'infile')

    # finally, we compute the consensus tree using 'consense' and print it (with stdout)
    # run consense
    run_prg = subprocess.Popen(['phylip', 'consense'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # handle the inner process
    in_handler = 'y\nr\n'
    run_prg.communicate(input=in_handler.encode('utf-8'))

