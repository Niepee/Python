import os
import re
import pandas as pd
import glob

# Set the folder path
path = "C:/Users/Niels/Desktop/Python/SCRIPTS"
savepath = "C:/Users/Niels/Desktop"
os.chdir(path)
print(os.listdir(path))

# Sla alle txt files op in txtfiles
txtfiles = []
for file in glob.glob("*.txt"):
    txtfiles.append(file)

# Create an empty dataframe to hold the results
results_df = pd.DataFrame(columns=["Filename", "Name", "Date"])

# Define the regular expressions to match the fields we want to extract
name_regex = r'Naam\s+(.+)\n'
date_regex = r'Datum\s+(.+)\n'

#Sla de inhoud van de txtfiles op in files_content
files_content = []

for filename in txtfiles:
    filepath = os.path.join(path, filename)
    with open(filepath, mode='r') as f:
        files_content += [f.read()]

#NU ZOEKEN DATA IN IEDERE STRING, OF EERST ZOEKEN EN DAN OPSLAAN IN FILES_CONTENT

# Extract the name using regex
name_match = re.search(name_regex, files_content)
name = name_match.group()

# Extract the information using regex
date_match = re.search(date_regex, files_content)
date = date_match

# Add the results to the dataframe
results_df = results_df.append({
      "Filename": filename,
      "Name": name,
      "Date": date
      }, ignore_index=True)

# Write the dataframe to an Excel file
results_df.to_excel("results.xlsx", index=False)