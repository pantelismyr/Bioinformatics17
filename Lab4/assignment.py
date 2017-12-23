import sqlite3
import sys

# create a connection object that represents the database.
conn = sqlite3.connect('db1.db')
# create a cursor object and call its execute() method to perform SQL commands
c = conn.cursor()

totalspecies = []
longprot = []
speciesNHR3 = []
numProt = []
protStruct = []
#=============================== 1.What species are in the database?
for sp in c.execute('SELECT name FROM species;'):
        totalspecies.append(sp)

#=============================== 2.Add another species to the database: Sus scrofa!
'''
Warning: Since abbreviation(abbrev) in the table is a Primary key, you are allowed only once to insert an enrty with a specific abbrev.
         So 'Sus Scrofa' with the abbrev SS could be inserted only once.
'''
try:
    c.execute("INSERT INTO species values('SS', 'Sus scrofa','Wild Boar');")
    # Save (commit) the changes
    conn.commit()
except:
    print('Warning on line {}:'.format(sys.exc_info()[-1].tb_lineno),"The UNIQUE species.abbrev entry already exists!")
    
# To delete the entry uncomment the following lines
# c.execute('DELETE FROM species WHERE name=?;', ('Sus scrofa',))
# conn.commit()

#=============================== 3.What proteins are longer than 1000 aa?

for acc in c.execute('SELECT accession FROM protein WHERE length(sequence)>1000;'):
    longprot.append(acc)

#=============================== 4.What species are present in family NHR3? Give a full list with full species names using one SQL statement.

for name in c.execute("SELECT name FROM species WHERE abbrev IN (SELECT species FROM protein WHERE accession IN (SELECT protein FROM familymembers WHERE family='NHR3'));"):
    speciesNHR3.append(name)

#=============================== 5.How many proteins from each species are present in the database?
for entry in c.execute("SELECT name,common,count(species)  FROM protein,species WHERE species.abbrev=protein.species group by name;"):
    numProt.append(entry)

#=============================== 6.How do you change the schema to add information about a protein's structure?

# create a table if not already exists
c.execute('''CREATE TABLE IF NOT EXISTS pstructure (
                    protein character PRIMARY KEY,
                    structure name character,
                    resolution real,
                    method character);'''
        )

# insert an entry
try:
    c.execute("INSERT INTO pstructure values('RORB_HUMAN', '5fvl', '1.97Å', 'Solution NMR');")
    # Save (commit) the changes
    conn.commit()
except:
    print('Warning on line {}:'.format(sys.exc_info()[-1].tb_lineno),"The UNIQUE pstructure.protein entry already exists!")

# To delete the table pstructure uncomment the following lines
# c.execute('DROP TABLE pstructure')
# conn.commit()

for entry in c.execute('SELECT * FROM pstructure;'):
    protStruct.append(entry)


print('='*100,'START','\n')
print("Q1 --->> What species are in the database?\n\n", totalspecies,'\n')
print('@'*100,'\n')
print("Q3 --->> What proteins are longer than 1000 aa?\n\n", longprot, '\n')
print('@'*100,'\n')
print("Q4 --->> What species are present in family NHR3? Give a full list with full species names using one SQL statement.\n\n", speciesNHR3, '\n')
print('@'*100,'\n')
print("Q5 --->> How many proteins from each species are present in the database?\n")
[print(numProt[i][0], numProt[i][2]) for i in range(len(numProt))]
print()
print('@'*100,'\n')
print("Q6 --->> Protein Structures Table:\n\n",protStruct,'\n')
print('='*100,'END')