from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# قائمة المستخدمين الوهميين
users = [
    {"id": 1, "username": "doctor1", "password": "password1", "patient": "patient1"},
    {"id": 2, "username": "doctor2", "password": "password2", "patient": "patient2"},
    {"id": 3, "username": "patient1", "password": "password3", "doctor": "doctor1"},
    {"id": 4, "username": "patient2", "password": "password4", "doctor": "doctor2"},
    {"id": 5, "username": "patient3", "password": "password5", "doctor": "doctor2"},
    {"id": 6, "username": "patient4", "password": "password6", "doctor": "doctor1"},
    {"id": 7, "username": "admin", "password": "adminpassword", "role": "admin"}
]

# معلومات مرضى وهمية
patients_db = {
    "patient1": {"name": "مريض 1", "age": 30, "gender": "ذكر", "diagnosis": "التهاب الحلق"},
    "patient2": {"name": "مريض 2", "age": 45, "gender": "أنثى", "diagnosis": "ارتفاع ضغط الدم"},
    "patient3": {"name": "مريض 3", "age": 55, "gender": "ذكر", "diagnosis": "سكري"},
    "patient4": {"name": "مريض 4", "age": 28, "gender": "أنثى", "diagnosis": "التهاب المفاصل"}
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = next((user for user in users if user["username"] == username), None)
        
        if user:
            if user["password"] == password:
                if user.get("role") == "admin":
                    return redirect(url_for("dashboard"))
                elif user["username"].startswith("doctor"):
                    return redirect(url_for("doctor", user_id=user["id"]))
                else:
                    return redirect(url_for("patient", user_id=user["id"]))
        
        error = "اسم المستخدم أو كلمة المرور غير صحيحة."
        return render_template("login.html", error=error)
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/doctor/<int:user_id>")
def doctor(user_id):
    doctor = next((user for user in users if user["id"] == user_id), None)
    patient_username = doctor.get("patient")
    patient_info = patients_db.get(patient_username)
    
    return render_template("doctor.html", doctor=doctor, patient=patient_info)

@app.route("/patient/<int:user_id>", methods=["GET", "POST"])
def patient(user_id):
    patient = next((user for user in users if user["id"] == user_id), None)
    doctor_username = patient.get("doctor")
    
    if request.method == "POST":
        return redirect(url_for("home"))
    
    return render_template("patient.html", patient=patient, doctor_username=doctor_username)

if __name__ == "__main__":
    app.run(debug=True)