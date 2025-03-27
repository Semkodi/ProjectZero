from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Funktion, um die Datenbankverbindung herzustellen
def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="socialmedia"
    )
    return db


# Route zum Bearbeiten des Profils
@app.route("/profil", methods=["GET", "POST"])
def bearbeiten_profil():
    if request.method == "POST":
        try:
            # Daten aus dem Formular abrufen
            name = request.form["name"]
            job = request.form["job"]
            age = request.form["age"]
            about = request.form["about"]
            profilbild = request.files["profilbild"]

            # Daten in der Datenbank aktualisieren
            db = connect_db()
            cursor = db.cursor()
            query = "UPDATE profiles SET job=%s, age=%s, about=%s WHERE name=%s"
            cursor.execute(query, (job, age, about, name))
            db.commit()

            # Profilbild speichern
            profilbild.save("static/profilbild.jpg")

            cursor.close()
            db.close()

            return redirect(url_for('profil'))
        except mysql.connector.Error as err:
            return "Fehler beim Speichern der Daten: {}".format(err)
    else:
        return render_template("bearbeiten_profil.html")

if __name__ == "__main__":
    app.run(debug=True)
