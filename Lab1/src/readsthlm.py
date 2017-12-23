import sys



def getIdsSeq(filename):
    """
    Returns a list of tupples: i.e (ids,seq)
    """
    with open(filename, "r") as f:
        content = f.readlines()
     
    # file without the heading
    # content = content[1:]       
    
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
            



def main():
    filename = sys.argv[1]
    data = getIdsSeq(filename)
    
    empty_file = False
    length = 0
    for d in data:
        if d[0] == '':
            empty_file = True
            length = 0
            print("Note: This stockholm file is empty!")
        else:
            length += 1
    print(length)
    [print(line[0]) for line in data if empty_file == False]

    for d in data:
        if d[1] == '' and d[0]:
            print()
            print('Note: There is no sequence for accession: %s ' %(d[0]))    
            print()
    """
    using libraries and modules
    """
    # from Bio import AlignIO
    # from os.path import splitext
    # while True:
    #     try:
    #         filename = sys.argv[1]

    #         # get the extention of file
    #         _, extension = splitext(filename)
            
    #         # check if the type of file is correct
    #         if extension != '.sth' and extension != '.sthlm':
    #             raise NameError 
            
    #         # read file
    #         file = AlignIO.read(open(filename), "stockholm")

    #         # count the number of sequences
    #         count = 0
    #         for data in file:
    #             if data.seq != " ":
    #                 count += 1
                    
    #         print()
    #         print("Number of sequences: " + str(count) + "\n")
    #         print("Accessions of sequences:")
    #         [print(data.ids) for data in file]
    #         print()
    #         break
        
    #     except NameError:
    #         print("Invalids filename.  Try again...")

    
if __name__ == '__main__':
    main()
