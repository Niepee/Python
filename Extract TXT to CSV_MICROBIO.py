# importing libraries
import os
import re
import shutil
import pathlib
from datetime import datetime
import csv
import pandas
import xlsxwriter

# defining location of parent folder
BASE_DIRECTORY = "C:\\Users\\Niels\\Desktop\\Python\\SCRIPTS\\TXTmicrobio"
DEST_BTU = "C:\\Users\\Niels\\Desktop\\Python\\SCRIPTS\\BTU"
DEST_CB = "C:\\Users\\Niels\\Desktop\\Python\\SCRIPTS\\CB"
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
BASE_DIRECTORY_CB = "C:\\Users\\Niels\\Desktop\\Python\\SCRIPTS\\CB"
output_file_CB = open("C:\\Users\\Niels\\Desktop\\Python\\SCRIPTS\\output_CB.txt", 'w')
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
        determinatie_match_replaced21 = determinatie_match_replaced2.replace(',', '')
        determinatie_match_replaced3 = determinatie_match_replaced21.replace('KVE', 'KVE,')
        determinatie_match_replaced4 = determinatie_match_replaced3.replace('kve', 'kve,')
        determinatie_match_replaced5 = determinatie_match_replaced4.replace('2:', ' ')
        determinatie_match_replaced6 = determinatie_match_replaced5.replace('3:', ' ')
        determinatie_match_replaced7 = determinatie_match_replaced6.replace('4:', ' ')
        determinatie_match_replaced8 = determinatie_match_replaced7.replace('5:', ' ')
        determinatie_match_replaced9 = determinatie_match_replaced8.replace('6:', ' ')
        determinatie_match_replaced10 = determinatie_match_replaced9.replace('7:', ' ')
        determinatie_match_replaced11 = determinatie_match_replaced10.replace('8:', ' ')
        determinatie_match_replaced12 = determinatie_match_replaced11.replace('9:', ' ')
        determinatie_match_replaced13 = determinatie_match_replaced12.replace('10:', ' ')
        determinatie_match_replaced14 = determinatie_match_replaced13.replace('11:', ' ')
        determinatie_match_replaced15 = determinatie_match_replaced14.replace('12:', ' ')
        determinatie_match_stripped = determinatie_match_replaced15.strip()
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

output_file_CB.close()

##########################################################
# Extract output_CB naar tabel
# Open the text file and read its contents & split the data into individual strings
f = open("C:\\Users\\Niels\\Desktop\\Python\\SCRIPTS\\output_CB.txt", 'r')
data = f.read()
strings = re.split('---', data)
strings.remove('')

# Create an empty list to store the table rows
table = []
df = pandas.DataFrame(columns=['Plaat Nr.', 'Datum', 'Naam', 'Type', 'Locatie', 'Determinatie'])

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
    new_row = [i+1, date, name, type, Locatie, Determinatie]
    df.loc[len(df)] = new_row

def split_series(ser,sep):
    return pandas.Series(ser.str.cat(sep=sep).split(sep=sep))

df2=(df.groupby(df.columns.drop('Determinatie').tolist(), group_keys=True) #group by all but one column
          ['Determinatie'] #select the column to be split
          .apply(split_series,sep=', ') # split 'Seatblocks' in each group
        .reset_index(drop=True,level=-1).reset_index()) #remove extra index created
df2["Determinatie"] = df2["Determinatie"].str.lstrip()

df2[["Determinatie", "sep", "Aantal KVE"]] = df2["Determinatie"].str.split("(\d)", n=1, expand=True)
df2["Aantal KVE"] = df2["sep"] + df2["Aantal KVE"]
df2.drop("sep", inplace=True, axis=1)
df2['Aantal KVE'] = df2['Aantal KVE'].str.extract('(\d+)').astype(int)

df2.to_excel(excel_writer="C:\\Users\\Niels\\Desktop\\Python\\SCRIPTS\\output_CB.xlsx", sheet_name= "Datasheet")

#####################################################
# Excel opschonen




