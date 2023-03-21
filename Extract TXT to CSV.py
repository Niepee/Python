# importing libraries
import os

# defining location of parent folder
BASE_DIRECTORY = "C:/Users/Niels/Desktop/Python/SCRIPTS/TXTfiles"
output_file = open('output.txt', 'w')
output = {}
file_list = []

# scanning through sub folders
for (dirpath, dirnames, filenames) in os.walk(BASE_DIRECTORY):
    for f in filenames:
        if 'txt' in str(f):
            e = os.path.join(str(dirpath), str(f))
            file_list.append(e)

for f in file_list:
    print(f)
    txtfile = open(f, 'r')
    output[f] = []
    for line in txtfile:
        if 'Naam' in line:
            output[f].append(line)
        elif 'Datum' in line:
            output[f].append(line)
tabs = []
for tab in output:
    tabs.append(tab)

tabs.sort()
for tab in tabs:
    output_file.write(tab)
    output_file.write('\n')
    for row in output[tab]:
        output_file.write(row + '')
    output_file.write('\n')
    output_file.write('---\n')

#######################################################
#Hieronder zal output.txt omgezet worden naar formatted_output.txt
with open("C:/Users/Niels/Desktop/Python/SCRIPTS/output.txt", 'r') as f:
    lines = f.readlines()

formatted_lines = []
for i in range(0, len(lines), 4):
    filename = lines[i].strip()
    name = lines[i+1].split('\t')[1].strip()
    date = lines[i+2].split('\t')[1].strip()
    formatted_lines.append(f"{i//4+1}, {name}, {date}\n")

with open('formatted_output.txt', 'w') as f:
    f.writelines(formatted_lines)

#######################################################
#Hieronder wordt TXT omgezet naar CSV
import csv

with open('C:/Users/Niels/Desktop/Python/SCRIPTS/formatted_output.txt', 'r') as f:
    lines = f.readlines()

data = [line.strip().split(', ') for line in lines]

with open('C:/Users/Niels/Desktop/Python/SCRIPTS/output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Nr', 'Naam', 'Datum'])
    writer.writerows(data)