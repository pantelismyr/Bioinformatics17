import random

def rand_DNA_seq(length):
    # Note: Distribution of the nucleotide is 1/4
    return ''.join(random.choice('AGCT') for _ in range(length))

def main():
        try:
            val = int(input("Enter the DNA sequence length: "))
            if val <= 0:
                raise ValueError 
            seq = rand_DNA_seq(val)
            print('\n>myrandomsequence: \n', seq, '\n')
        except ValueError:
            print("Invalid length.  Try again...")
        
if __name__ == '__main__':
    main()
