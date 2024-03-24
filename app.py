
from flask import Flask, render_template, request, make_response, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Function to establish connection to SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    #conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    #c = conn.cursor()
    print("Connected to database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE,password TEXT NOT NULL,score TEXT NOT NULL)')
    conn.execute('CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY AUTOINCREMENT,patient_id INTEGER NOT NULL,visit_date DATE NOT NULL,FOREIGN KEY (patient_id) REFERENCES users (id))')
    conn.execute('CREATE TABLE IF NOT EXISTS proteins (id INTEGER PRIMARY KEY AUTOINCREMENT,visit_id INTEGER NOT NULL,protein_name TEXT NOT NULL,NPX TEXT NOT NULL,FOREIGN KEY (visit_id) REFERENCES visits (id))')
    conn.execute('CREATE TABLE IF NOT EXISTS peptides ( id INTEGER PRIMARY KEY AUTOINCREMENT, visit_id INTEGER NOT NULL, peptide_name TEXT NOT NULL,PeptideAbundance TEXT NOT NULL,FOREIGN KEY (visit_id) REFERENCES visits (id))')

    print("Created table successfully!")
    conn.commit()
    conn.close()

    fill_info()

def patients_l():
    patients_l = [
        {"username":"Arwa","password":"qwertyuiop[]", "score":15},
        {"username":"Rana","password":"asdfghjkl;'", "score":70},
        {"username":"Eman","password":"zxcvbnm,.", "score":8}
    ]

    conn = get_db_connection()

    for i in patients_l:
      conn.execute('INSERT INTO patients (username ,password ,score ) VALUES (?,?,?)',(i['username'],i['password'],i['score']))

    conn.commit()
    conn.close()


def visits_l():
    visits_l = [
        {"patient_id":1,"visit_date":"3 March"},
        {"patient_id":2,"visit_date":"4 June"},
        {"patient_id":3,"visit_date":"2 May"},
        {"patient_id":1,"visit_date":"11 May"}
    ]

    conn = get_db_connection()

    for i in visits_l:
        conn.execute('INSERT INTO visits (patient_id ,visit_date ) VALUES (?,?)',(i['patient_id'],i['visit_date']))
    conn.commit()

    conn.close()

def proteins_l():
    proteins_l = [
        {"visit_id":1, "protein_name":"O00391","NPX":"11254.3"},
        {"visit_id":1, "protein_name":"P01717","NPX":"110750"},
        {"visit_id":1, "protein_name":"P01024","NPX":"3916980"},
        {"visit_id":1, "protein_name":"P00747","NPX":"43235500"},
        {"visit_id":1, "protein_name":"P01033","NPX":"732430"},
        {"visit_id":1, "protein_name":"P00450","NPX":"39585.8"},
        {"visit_id":1, "protein_name":"O60888","NPX":"1829650"},
        {"visit_id":1, "protein_name":"O00533","NPX":"24917"},
        {"visit_id":1, "protein_name":"O00584","NPX":"1613890"},
        {"visit_id":1, "protein_name":"P01019","NPX":"396955"},#-#
        {"visit_id":2, "protein_name":"O00391","NPX":"11254.3"},
        {"visit_id":2, "protein_name":"P01717","NPX":"110750"},
        {"visit_id":2, "protein_name":"P01024","NPX":"3916980"},
        {"visit_id":2, "protein_name":"P00747","NPX":"43235500"},
        {"visit_id":2, "protein_name":"P01033","NPX":"732430"},
        {"visit_id":2, "protein_name":"P00450","NPX":"39585.8"},
        {"visit_id":2, "protein_name":"O60888","NPX":"1829650"},
        {"visit_id":2, "protein_name":"O00533","NPX":"24917"},
        {"visit_id":2, "protein_name":"O00584","NPX":"1613890"},
        {"visit_id":2, "protein_name":"P01019","NPX":"396955"},
        {"visit_id":3, "protein_name":"P01019","NPX":"396955"},#-#
        {"visit_id":3, "protein_name":"O00391","NPX":"11254.3"},
        {"visit_id":3, "protein_name":"P01717","NPX":"110750"},
        {"visit_id":3, "protein_name":"P01024","NPX":"3916980"},
        {"visit_id":3, "protein_name":"P00747","NPX":"43235500"},
        {"visit_id":3, "protein_name":"P01033","NPX":"732430"},
        {"visit_id":3, "protein_name":"P00450","NPX":"39585.8"},
        {"visit_id":3, "protein_name":"O60888","NPX":"1829650"},
        {"visit_id":3, "protein_name":"O00533","NPX":"24917"},
        {"visit_id":3, "protein_name":"O00584","NPX":"1613890"},
        {"visit_id":4, "protein_name":"P01019","NPX":"396955"},#-#
        {"visit_id":4, "protein_name":"O00391","NPX":"11254.3"},
        {"visit_id":4, "protein_name":"P01717","NPX":"110750"},
        {"visit_id":4, "protein_name":"P01024","NPX":"3916980"},
        {"visit_id":4, "protein_name":"P00747","NPX":"43235500"},
        {"visit_id":4, "protein_name":"P01033","NPX":"732430"},
        {"visit_id":4, "protein_name":"P00450","NPX":"39585.8"},
        {"visit_id":4, "protein_name":"O60888","NPX":"1829650"},
        {"visit_id":4, "protein_name":"O00533","NPX":"24917"},
        {"visit_id":4, "protein_name":"O00584","NPX":"1613890"},
    ]

    conn = get_db_connection()

    for i in proteins_l:
        conn.execute('INSERT INTO proteins (visit_id ,protein_name ,NPX) VALUES (?,?,?)',(i['visit_id'],i['protein_name'],i['NPX']))

    conn.commit()


def peptides_l():
    peptides_l = [
        {"visit_id":1, "peptide_name":"NEQEQPLGQWHLS",  "PeptideAbundance":"11254.3"},
        {"visit_id":1, "peptide_name":"GNPEPTFSWTK",    "PeptideAbundance":"11254.3"},
        {"visit_id":1, "peptide_name":"IEIPSSVQQVPTIIK","PeptideAbundance":"110750"},
        {"visit_id":1, "peptide_name":"SMEQNGPGLEYR",   "PeptideAbundance":"3916980"},
        {"visit_id":1, "peptide_name":"TLKIENVSYQDKGNYR","PeptideAbundance":"43235500"},
        {"visit_id":1, "peptide_name":"VIAVNEVGR","PeptideAbundance":"732430"},
        {"visit_id":1, "peptide_name":"VMTPAVYAPYDVK","PeptideAbundance":"39585.8"},
        {"visit_id":1, "peptide_name":"VNGSPVDNHPFAGDVVFPR","PeptideAbundance":"1829650"},
        {"visit_id":1, "peptide_name":"ELDLNSVLLK","PeptideAbundance":"24917"},
        {"visit_id":1, "peptide_name":"ALPGTPVASSQPR","PeptideAbundance":"1613890"},
        {"visit_id":2, "peptide_name":"P01019","PeptideAbundance":"396955"},#-#
        {"visit_id":2, "peptide_name":"NEQEQPLGQWHLS","PeptideAbundance":"11254.3"},
        {"visit_id":2, "peptide_name":"GNPEPTFSWTK","PeptideAbundance":"11254.3"},
        {"visit_id":2, "peptide_name":"IEIPSSVQQVPTIIK","PeptideAbundance":"110750"},
        {"visit_id":2, "peptide_name":"SMEQNGPGLEYR","PeptideAbundance":"3916980"},
        {"visit_id":2, "peptide_name":"TLKIENVSYQDKGNYR","PeptideAbundance":"43235500"},
        {"visit_id":2, "peptide_name":"VIAVNEVGR","PeptideAbundance":"732430"},
        {"visit_id":2, "peptide_name":"VMTPAVYAPYDVK","PeptideAbundance":"39585.8"},
        {"visit_id":2, "peptide_name":"VNGSPVDNHPFAGDVVFPR","PeptideAbundance":"1829650"},
        {"visit_id":2, "peptide_name":"ELDLNSVLLK","PeptideAbundance":"24917"},
        {"visit_id":3, "peptide_name":"ALPGTPVASSQPR","PeptideAbundance":"1613890"},
        {"visit_id":3, "peptide_name":"NEQEQPLGQWHLS","PeptideAbundance":"11254.3"},
        {"visit_id":3, "peptide_name":"GNPEPTFSWTK","PeptideAbundance":"11254.3"},
        {"visit_id":3, "peptide_name":"IEIPSSVQQVPTIIK","PeptideAbundance":"110750"},
        {"visit_id":3, "peptide_name":"SMEQNGPGLEYR","PeptideAbundance":"3916980"},
        {"visit_id":3, "peptide_name":"TLKIENVSYQDKGNYR","PeptideAbundance":"43235500"},
        {"visit_id":3, "peptide_name":"VIAVNEVGR","PeptideAbundance":"732430"},
        {"visit_id":3, "peptide_name":"VMTPAVYAPYDVK","PeptideAbundance":"39585.8"},
        {"visit_id":3, "peptide_name":"VNGSPVDNHPFAGDVVFPR","PeptideAbundance":"1829650"},
        {"visit_id":3, "peptide_name":"ELDLNSVLLK","PeptideAbundance":"24917"},
        {"visit_id":4, "peptide_name":"ALPGTPVASSQPR","PeptideAbundance":"1613890"},
        {"visit_id":4, "peptide_name":"NEQEQPLGQWHLS","PeptideAbundance":"11254.3"},
        {"visit_id":4, "peptide_name":"GNPEPTFSWTK","PeptideAbundance":"11254.3"},
        {"visit_id":4, "peptide_name":"IEIPSSVQQVPTIIK","PeptideAbundance":"110750"},
        {"visit_id":4, "peptide_name":"SMEQNGPGLEYR","PeptideAbundance":"3916980"},
        {"visit_id":4, "peptide_name":"TLKIENVSYQDKGNYR","PeptideAbundance":"43235500"},
        {"visit_id":4, "peptide_name":"VIAVNEVGR","PeptideAbundance":"732430"},
        {"visit_id":4, "peptide_name":"VMTPAVYAPYDVK","PeptideAbundance":"39585.8"},
        {"visit_id":4, "peptide_name":"VNGSPVDNHPFAGDVVFPR","PeptideAbundance":"1829650"},
        {"visit_id":4, "peptide_name":"ELDLNSVLLK","PeptideAbundance":"24917"}
        
    ]

    conn = get_db_connection()

    for i in peptides_l:
        conn.execute('INSERT INTO peptides (visit_id ,peptide_name, PeptideAbundance ) VALUES (?,?,?)',(i['visit_id'],i['peptide_name'], i['PeptideAbundance']))

    conn.commit()

    


def fill_info():
    conn = get_db_connection()
    #patients_l()
    #visits_l()
    #proteins_l()
    #peptides_l()
    j=0
    j=j+1
    conn.close()




# Fetch all patients from the database
def get_patients():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()
    return patients



@app.route("/")
def home():
    #create_table()
    fill_info()
    return render_template( "home.html")

@app.route('/Patients' , methods=['GET'])
def Patients():
    Patients = get_patients()


    return render_template( "Patients.html",Patients=Patients)


@app.route('/patient_info/<int:p_id>')
def patient_info(p_id):
    conn = get_db_connection()
    
    # Fetch patient details
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (p_id,)).fetchone()

    # Fetch visits and sort them by date in descending order
    visits = conn.execute('SELECT * FROM visits WHERE patient_id = ? ORDER BY visit_date DESC', (p_id,)).fetchall()

    proteins = {}
    peptides = {}
    for visit in visits:
        visit_id = visit['id']
        visit_date = visit['visit_date']
        proteins[visit_date] = conn.execute('SELECT * FROM proteins WHERE visit_id = ?', (visit_id,)).fetchall()
        peptides[visit_date] = conn.execute('SELECT * FROM peptides WHERE visit_id = ?', (visit_id,)).fetchall()

    conn.close()

    # Preprocess data for JavaScript
    proteins_list = [{'date': date, 'name': protein['name'], 'score': protein['score']} for date, proteins_for_date in proteins.items() for protein in proteins_for_date]
    peptides_list = [{'date': date, 'name': peptide['name'], 'score': peptide['score']} for date, peptides_for_date in peptides.items() for peptide in peptides_for_date]

    return render_template('patient_info.html', patient=patient, proteins=proteins_list, peptides=peptides_list)

if __name__ == '__main__':
    app.run(debug=True)

