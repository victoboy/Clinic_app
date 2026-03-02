from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "vanditClinic2026SecureKey!"

# Database Setup
def init_db():
    conn = sqlite3.connect("clinic.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  age TEXT,
                  gender TEXT,
                  contact TEXT,
                  diagnosis TEXT,
                  prescription TEXT,
                  followup TEXT,
                  created_at TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "doctor" and request.form["password"] == "1234":
            session["user"] = "doctor"
            return redirect("/dashboard")
    return render_template("login.html")

# Dashboard with Search
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    search = request.args.get("search", "")
    conn = sqlite3.connect("clinic.db")
    c = conn.cursor()

    if search:
        c.execute("SELECT * FROM patients WHERE name LIKE ? OR contact LIKE ?",
                  ('%'+search+'%', '%'+search+'%'))
    else:
        c.execute("SELECT * FROM patients ORDER BY id DESC")

    patients = c.fetchall()
    conn.close()

    return render_template("dashboard.html", patients=patients, search=search)

# Add Patient
@app.route("/add", methods=["GET", "POST"])
def add_patient():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        conn = sqlite3.connect("clinic.db")
        c = conn.cursor()
        c.execute("""INSERT INTO patients 
                     (name, age, gender, contact, diagnosis, prescription, followup, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (request.form["name"],
                   request.form["age"],
                   request.form["gender"],
                   request.form["contact"],
                   request.form["diagnosis"],
                   request.form["prescription"],
                   request.form["followup"],
                   datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    return render_template("add_patient.html")

# Delete
@app.route("/delete/<int:id>")
def delete_patient(id):
    if "user" not in session:
        return redirect("/")
    conn = sqlite3.connect("clinic.db")
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
