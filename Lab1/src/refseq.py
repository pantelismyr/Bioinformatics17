import sys


def getIdsSeq(content):
    """
    Returns a list of tupples: i.e (ids,seq)
    """

    # get "ids" and "seq" in two lists respectively
    ids = []
    seqs = []
    sequence = ''
    for line in content:
        for i in range(len(line)):    
            if line[i]in [' ', '\t', '\n']:
                ids.append(line[:i])
                # remove the space between ids and sequence, same as .strip()
                for char in line[i:]:
                    if char in [' ', '\t', '\n']:
                        continue
                    else:
                        sequence += char
                seqs.append(sequence)
                sequence = ''
                break
            else:
                continue
    
    # create a list of tupples: i.e (ids,seq)
    idsSeqs = list(zip(ids, seqs))
    
    
    cleaned_idsSeqs = []
    for data in idsSeqs:
        if data[0] in ['//', '#', '#=GF', '#=GS', '#=GR', '#=GC']:
            continue
        else:
            cleaned_idsSeqs.append(data)        
    return cleaned_idsSeqs
    
    
    
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
        
        
def main():
    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.readlines()
    data = getIdsSeq(content)
    # print in fasta format
    Seq2fasta(data)
    
    
if __name__ == '__main__':
    main()

