import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def protein_information(protein):
    lines = protein.strip().split('\n')
    protein_info = {
        'ID': '',
        'Accession': '',
        'ProteinName': '',
        'Organism': '',
        'Function': '',
        'DiseaseInvolvement': ''
    }
    reading_function = False
    reading_disease = False

    for line in lines:
        if line.startswith("ID   "):
            protein_info['ID'] = line.split()[1]
        elif line.startswith("AC   "):
            protein_info['Accession'] = line.split()[1].rstrip(';')
        elif 'RecName: Full=' in line:
            protein_info['ProteinName'] = line.split('Full=')[1].split(';')[0].strip()
        elif line.startswith("OS   "):
            protein_info['Organism'] = line.split('OS   ')[1].rstrip('.')
        elif line.startswith("CC   -!- FUNCTION:"):
            reading_function = True
            protein_info['Function'] = line[19:].strip()
        elif reading_function and line.startswith("CC       "):
            protein_info['Function'] += ' ' + line.strip()
        elif not line.startswith("CC       ") and reading_function:
            reading_function = False
        elif line.startswith("CC   -!- DISEASE:"):
            reading_disease = True
            protein_info['DiseaseInvolvement'] = line[19:].strip()
        elif reading_disease and line.startswith("CC       "):
            protein_info['DiseaseInvolvement'] += ' ' + line.strip()
        elif not line.startswith("CC       ") and reading_disease:
            reading_disease = False

    return protein_info

def get_variants(uniprot_id):
    url = f"https://www.ebi.ac.uk/proteins/api/variation/{uniprot_id}?format=json"
    try:
        response = requests.get(url, headers={"Accept": "application/json"})
        response.raise_for_status()  # This will handle HTTP errors
        return response.json().get('features', [])
    except requests.RequestException as e:
        app.logger.error(f"Error fetching variant data: {str(e)}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uniprot_id = request.form.get('uniprot_id')
        if uniprot_id:
            return redirect(url_for('protein_info_page', uniprot_id=uniprot_id))
    return render_template('index.html')

@app.route('/protein/<uniprot_id>', methods=['GET'])
def protein_info_page(uniprot_id):
    try:
        url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
        response = requests.get(url)
        response.raise_for_status()
        protein_info = protein_information(response.text)
        
        # Check if the disease involvement directly indicates Parkinson's disease
        protein_info['IsParkinsonRelated'] = 'Parkinson' in protein_info['DiseaseInvolvement']

        return render_template('protein_info.html', protein_info=protein_info)
    except requests.HTTPError as e:
        return render_template('error.html', error=f"HTTP Error {e.response.status_code}: {e.response.reason}")

if __name__ == '__main__':
    app.run(debug=True)
