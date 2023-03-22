# importing libraries
import os
import re
import shutil
import pathlib
from datetime import datetime
import csv
import pandas

# defining location of parent folder
BASE_DIRECTORY = "C:/Users/Niels/Desktop/Python Projecten/TXT_project/TXTmicrobio"
DEST_BTU = "C:\\Users\\Niels\\Desktop\\Python Projecten\\TXT_project\\TXTmicrobio\\BTU"
DEST_CB = "C:\\Users\\Niels\\Desktop\\Python Projecten\\TXT_project\\TXTmicrobio\\CB"
file_list = []

# scanning through sub folders
for (dirpath, dirnames, filenames) in os.walk(BASE_DIRECTORY):
    for f in filenames:
        if 'txt' in str(f):
            e = os.path.join(str(dirpath), str(f))
            file_list.append(e)

# CB en BTU bestanden splitsen
for f in file_list:
    with open(f, 'r') as file:
        for line in file:
            if 'BTU' in line:
                shutil.copy(f, DEST_BTU)
            if 'CB' in line:
                shutil.copy(f, DEST_CB)

for f in file_list:
    if f.endswith(".txt"):
        os.remove(f)

####################################
# CB bestanden lezen
# defining location of parent folder
BASE_DIRECTORY_CB = "C:/Users/Niels/Desktop/Python Projecten/TXT_project/TXTmicrobio/CB"
output_file_CB = open("C:/Users/Niels\Desktop/Python Projecten/TXT_project/output_CB.txt", 'w')
output = {}
file_list = []

# Maak regex patterns
name_pattern = r'(?s)(?<=Naam)([\s\S]*?)(?=Geslacht)'
rapport_pattern = r'(?s)(?<=Rapportinformatie:)([\s\S]*?)(?=UITSLAG VOLLEDIG)'
determinatie_pattern = r'(?s)(?<=Determinatie stam)([\s\S]*?)(?=LEGENDA)'

# scanning through sub folders
for (dirpath, dirnames, filenames) in os.walk(BASE_DIRECTORY_CB):
    for f in filenames:
        if 'txt' in str(f):
            e = os.path.join(str(dirpath), str(f))
            file_list.append(e)

for f in file_list:
    with open(f, 'r') as file:
    text = file.read()
    name_match = re.search(name_pattern, text).group()
    name_match_stripped = name_match.strip()
    rapport_match = re.search(rapport_pattern, text).group()
    rapport_match_stripped = rapport_match.strip()
    determinatie_match = re.search(determinatie_pattern, text).group()
    determinatie_match_replaced = determinatie_match.replace('\n', '')
    determinatie_match_replaced2 = determinatie_match_replaced.replace('           ', ' ')
    determinatie_match_stripped = determinatie_match_replaced2.strip()
    print(f)
    txtfile = open(f, 'r')
    output[f] = []
    for line in txtfile:
        if 'Naam' in line:
            output[f].append(name_match_stripped)
            output[f].append(rapport_match_stripped)
            output[f].append('\n' + determinatie_match_stripped)

print(output)
tabs = []
for tab in output:
    tabs.append(tab)

for tab in tabs:
    output_file_CB.write('\n')
    for row in output[tab]:
        output_file_CB.write(row + '')
    output_file_CB.write('\n')
    output_file_CB.write('---')

##########################################################
# Extract output_CB naar tabel
# Open the text file and read its contents
with open("C:/Users/Niels/Desktop/Python Projecten/TXT_project/output_CB.txt", 'r') as f:
    data = f.read()

# Split the data into individual strings
strings = re.split('---', data)
strings.remove('')

# Create an empty list to store the table rows
table = []
df = pd.DataFrame(columns=['A','B','C','D','E','F','G'])

# Loop over each string and extract the required information
for i, s in enumerate(strings):
    # Extract the date using a regular expression
    date_str = re.search(r'\d{1,2}-\d{1,2}-\d{4}', s).group(0)
    date = datetime.strptime(date_str, '%d-%m-%Y').date()

    # Extract the name using a regular expression
    name = re.search(r'[A-Z]{3}', s).group(0)

    # Extract the name using a regular expression
    Determinatie = re.search(r'(?<=1:)(.*)', s).group(1)

    # Determine the type based on whether 'Sedimentatie' or 'Contact' is found in the string
    if 'Sedimentatie'in s:
        type = 'Sedimentatie'
    elif 'sedimentatie' in s:
        type = 'Sedimentatie'
    elif 'Contact' in s:
        type = 'Contact'
    elif 'contact'in s:
        type = 'Contact'
    else:
        type = ''

    # Determine the type based on whether 'Hand' or 'Mvk' is found in the string
    if 'Hand' in s:
        Locatie = 'Hand'
    elif 'hand' in s:
        Locatie = 'Hand'
    elif 'Mvk' in s:
        Locatie = 'Mvk'
    elif 'mvk' in s:
        Locatie = 'Mvk'
    elif 'MVK' in s:
        Locatie = 'Mvk'
    else:
        Locatie = ''

    # Append the row to the table
    table.append((i+1, date, name, type, Locatie, Determinatie))

# Schrijf naar CSV
header = ['Nr.', 'Datum', 'Naam', 'Type', 'Locatie', 'Determinatie']
with open('C:/Users/Niels/Desktop/Python Projecten/TXT_project/output_CB.csv', 'w', newline='') as out_file:
    writer = csv.writer(out_file, delimiter=',')
    writer.writerow(header)
    writer.writerows(table)

# Print the table
print('Nr.\tDatum\t\t\tNaam\t\t\tType\t\t\tLocatie\t\t\tDeterminatie')
for row in table:
    print('{}\t{}\t{}\t{}\t{}\t{}'.format(*row))



