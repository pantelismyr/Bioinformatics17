echo "********************************************************************"
echo "How many columns are there (if you count by eye)?:"
cd ~/Desktop/Bioinformatics17/Lab1/Data/
head -n 1 gpcr.tab 			# "-n 1" print only the 1st row
echo "********************************************************************"
echo "How many lines are there in the file?:"
cd ~/Desktop/Bioinformatics17/Lab1/Data/
wc -l gpcr.tab | cut -d " " -f 4 			# cut gives only the 4th field, which is the requested number, fields 1-3 are gaps and 4... is the filename 	
echo "********************************************************************"
echo "How many human GPCRs there are listed. Do you search for "human" or "Homo sapiens"?:"
cd ~/Desktop/Bioinformatics17/Lab1/Data/
echo "human:" && grep "human" gpcr.tab | wc -l
echo "Human:" && grep "Human" gpcr.tab | wc -l
echo "Homo sapiens:" && grep "Homo sapiens" gpcr.tab | wc -l
echo "********************************************************************"
echo "How long is the shortest sequence listed in the same file?:"
cd ~/Desktop/Bioinformatics17/Lab1/Data/
cut -f 7 gpcr.tab | sort -ug | head -n 2
echo "********************************************************************"
echo "How many species are named in gpcr.tab?:"
cd ~/Desktop/Bioinformatics17/Lab1/Data/
cut -f 6 gpcr.tab | tail +2 | sort -u | wc -l
echo "********************************************************************"
read -p "Press enter to continue to MSA"
echo "Multi-sequence alignment (MSA):"
cd ~/Desktop/Bioinformatics17/Lab1/Data/yeast_genes/
FILES=*
for i in $FILES; 
    do 
    mkdir ~/Desktop/MSA
    ~/Desktop/Bioinformatics17/Lab1/muscle -in $i -out ~/Desktop/MSA/${i%.fasta}_MSA;
done

