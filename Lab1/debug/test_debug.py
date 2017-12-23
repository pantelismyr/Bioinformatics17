import sys
import pdb


def codonTable():
    """
    Returns the DNA codon table. (Standard genetic code)
    """
    std_gen_code = {'TTT':'F', 'TTC':'F',
                    'TTA':'L', 'TTG':'L','CTT':'L', 'CTC':'L', 'CTA':'L', 'CTG':'L',
                    'ATT':'I', 'ATC':'I', 'ATA':'I',
                    'ATG':'M',
                    'GTT':'V', 'GTC':'V', 'GTA':'V', 'GTG':'V',
                    'TCT':'S', 'TCC':'S', 'TCA':'S', 'TCG':'S', 'AGT':'S', 'AGC':'S',
                    'CCT':'P', 'CCC':'P', 'CCA':'P', 'CCG':'P',
                    'ACT':'T', 'ACC':'T', 'ACA':'T', 'ACG':'T',
                    'GCT':'A', 'GCC':'A', 'GCA':'A', 'GCG':'A',
                    'TAT':'Y', 'TAC':'Y',
                    'TAA':'', 'TAG':'', 'TGA':'', 
                    'CAT':'H', 'CAC':'H', 
                    'CAA':'Q', 'CAG':'Q', 
                    'AAT':'N', 'AAC':'N', 
                    'AAA':'K', 'AAG':'K', 
                    'GAT':'D', 'GAC':'D', 
                    'GAA':'E', 'GAG':'E', 
                    'TGT':'C', 'TGC':'C', 
                    'TGG':'W',
                    'CGT':'R', 'CGC':'R', 'CGA':'R', 'CGG':'R', 'AGA':'R', 'AGG':'R',
                    'GGT':'G', 'GGC':'G', 'GGA':'G', 'GGG':'G',

    }
    return std_gen_code


def getIdSeq(content):
    """
    Returns: a list of tuples: i.e (id,seq)
    Param: data in fasta format
    """
    ids = []
    seqs = []
    seq = ''
    for line in content:
        if line[0] == '>':
            ids.append(line[1:].split()[0])
            
            if seq != '':
                # when a new id arrives then the seq is completed and re-initialized
                seqs.append(seq)
                seq = ''
        else:
            seq += line.strip().upper()
    # for the last sequence (Note: not the most proper way but..)
    seqs.append(seq)
    # create the list of tuples 
    idsSeqs = list(zip(ids, seqs))
    return idsSeqs
 
     
def Seq2fasta(idsSeqs):
    """
    prints the fasta formatted file
    """
    for data in idsSeqs:
        if data[0] != '':
            print(">" + data[0], end = '\n')
            tmp = 0
            for c in range(len(data[1])+1):
                if data[1] == '':
                    break 
                else:
                    if c % 60 == 0 and c != 0:
                        print(data[1][tmp:c] + '')
                        tmp = c
                    elif c == len(data[1]):  
                        print(data[1][tmp:] + '')
                        break
        else:
            break  
    
    

def getORF(seq):
    """
    return the ORF in a reading frame
    """
    length = len(seq)
    ORF = ['']
    if length >= 3:
        for i in range(0,length,3):
            if seq[i:i+3] not in ['TAA', 'TAG', 'TGA']:         # the list contains the stop condons
                # -1: to keep the correct order of the triplets
                ORF[-1] += seq[i:i+3]
            else:
                # devide each ORF in the seq
                ORF.append('')
        return ORF
    else:
        return ''


def readDirection(seq):
    """
    5'-3' direction: 3 different starts, each if starting codon is a stop one
    """
    fivePrimethree = 3
    ORFs = []
    for i in range(fivePrimethree):
        ORFs += getORF(seq[i:])
    return ORFs
    

def longestORF(ORFs):
    '''
    Returns the longest ORF 
    '''
    try:
        return max(ORFs, key=len)
    except:
        # in case it's empty ORF
        return ''
    

def translateSeq2code(ORF):
    '''
    Translates an ORF to the Amino acid codes of the codons.
    '''
    genCode = codonTable()
    length = len(ORF)
    translation = []
    translation = ''
   
    if length >= 3:
        try:
            for i in range(0, length, 3):
                if ORF[i:i+3] not in genCode and len(ORF[i:i+3]) == 3:
                    # in case of ambiguity, 'Warning: should be a TRIPLET, so we ignore the cases where i.e the seq ends with less than 3 chars'
                    translation += 'X'
                else:
                    translation += genCode.get(ORF[i:i+3])
            return translation
        except:
            return translation
    else:
        return ' '
                

def main():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.readlines()
    
    pdb.set_trace()
    data = getIdSeq(content)
    
    allLongestORFs = []
    ids = []
    for d in data:
        # list with the ids
        ids.append(d[0])
        # find the longest ORF with reading direction 5'-3'
        longest = longestORF(readDirection(d[1]))
        # translate longest ORF
        translateLongest = translateSeq2code(longest)
        # list containing each ORF
        allLongestORFs.append(translateLongest)
    
    # create a list with tuples containing each id with its longest ORF i.e [('id','longestORF'),('..','..'),..]
    idsORFs = list(zip(ids,allLongestORFs))
    # print in fasta format
    Seq2fasta(idsORFs)



if __name__ == '__main__':
    main()
    