import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def peptide_information(response):
    lines = response.strip().split('\n')
    peptide_info = {
        'Entry': '',
        'Entry_name': '',
        'ProteinName': '',
        'Gene': '',
        'Organism': '',
        'Length': '',
        'Function': '',
        'DiseaseInvolvement': ''
    }
    reading_function = False
    reading_disease = False

    for line in lines:
            
        if line.startswith("ID   "):
            peptide_info['Entry_name'] = line.split()[1]
            peptide_info['Length'] = line.split('Reviewed;        ')[1].split(';')[0].strip()
        elif line.startswith("AC   "):
            peptide_info['Entry'] = line.split()[1].rstrip(';')
        elif 'RecName: Full=' in line:
            peptide_info['ProteinName'] = line.split('Full=')[1].split(';')[0].strip()
        
        elif line.startswith("OS   "):
            peptide_info['Organism'] = line.split('OS   ')[1].rstrip('.')
        elif line.startswith("GN   Name="):
            peptide_info['Gene'] = line.split('Name=')[1].split(';')[0].strip()+ ", CALL"
        elif line.startswith("CC   -!- FUNCTION:"):
            reading_function = True
            peptide_info['Function'] = line[19:].strip()
        elif reading_function and line.startswith("CC       "):
            peptide_info['Function'] += ' ' + line.strip()
        elif not line.startswith("CC       ") and reading_function:
            reading_function = False
        elif line.startswith("CC   -!- DISEASE:"):
            reading_disease = True
            peptide_info['DiseaseInvolvement'] = line[19:].strip()
        elif reading_disease and line.startswith("CC       "):
            peptide_info['DiseaseInvolvement'] += ' ' + line.strip()
        elif not line.startswith("CC       ") and reading_disease:
            reading_disease = False

    return peptide_info

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uniprot_id = request.form.get('uniprot_id')
        if uniprot_id:
            return redirect(url_for('peptide_info_page', uniprot_id=uniprot_id))
    return render_template('index.html')

@app.route('/peptide/<uniprot_id>', methods=['GET'])
def peptide_info_page(uniprot_id):
    try:
        url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
        response = requests.get(url)
        response.raise_for_status()
        peptide_info = peptide_information(response.text)
        
        # Check if the disease involvement directly indicates Parkinson's disease
        peptide_info['IsParkinsonRelated'] = 'Parkinson' in peptide_info['DiseaseInvolvement']

        return render_template('peptide_info.html', peptide_info=peptide_info)
    except requests.HTTPError as e:
        return render_template('error.html', error=f"HTTP Error {e.response.status_code}: {e.response.reason}")

if __name__ == '__main__':
    app.run(debug=True)
