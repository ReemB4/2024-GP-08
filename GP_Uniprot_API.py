""" import requests

def get_peptide_info(uniprot_id, peptide_sequence):
    # URL for the UniProt API
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"

    # Making a request to the UniProt API
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return

    # Filter and search for the peptide sequence within the protein information
    protein_data = response.text
    if peptide_sequence in protein_data:
        print(f"Peptide '{peptide_sequence}' found in protein data for UniProt ID {uniprot_id}:")
        # Output the whole entry
        print(protein_data)
    else:
        print(f"Peptide '{peptide_sequence}' not found in the protein data for UniProt ID {uniprot_id}.")

# Example 
uniprot_id = 'O00391' 
peptide_sequence = 'NEQEQPLGQWHLS' 

get_peptide_info(uniprot_id, peptide_sequence)
 """

import requests
import pandas as pd

# Parses raw UniProt data in txt format to a pandas DataFrame.
def parse_uniprot_data(raw_data):
    
    data = []
    current_entry = {}
    for line in raw_data.splitlines():
        if line.startswith("ID"):
            current_entry['ID'] = ' '.join(line.split()[1:])
        elif line.startswith("AC"):
            current_entry['Accession'] = line.split()[1].strip(';')
        elif line.startswith("DE"):
            description = line[5:].strip()
            if 'RecName: Full=' in description:
                current_entry['Protein Name'] = description.replace('RecName: Full=', '').strip(';')
        elif line.startswith("OS"):
            current_entry['Organism'] = line.split('OS   ')[1].strip('.')
        elif line.startswith("//"):
            data.append(current_entry)
            current_entry = {}
    return pd.DataFrame(data)

#Retrieves peptide information by UniProt ID and returns a DataFrame.
def get_peptide_info_by_id(uniprot_id):

    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text.splitlines())
        return parse_uniprot_data(response.text)
        
    else:
        return pd.DataFrame()  # Return an empty on failure

def get_peptide_info_by_sequence(sequence):
  
    url = "https://www.uniprot.org/peptide-search/"
    params = {
        "from": "SEQUENCE",
        "to": "ACC",
        "format": "txt",
        "query": sequence
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return parse_uniprot_data(response.text)
    else:
        return pd.DataFrame()  # Return an empty on failure

# Example:
uniprot_id = "O00391" 
sequence = "NEQEQPLGQWHLS" 

# Retrieve information by UniProt ID
df_id = get_peptide_info_by_id(uniprot_id)
print("Information retrieved by UniProt ID:")
print(df_id)

# Retrieve information by Sequence
df_seq = get_peptide_info_by_sequence(sequence)
print("\nInformation retrieved by Sequence:")
print(df_seq)


