from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

DB_HOST   = os.environ.get("DB_HOST", "mysql_principal")
NODO_NAME = os.environ.get("NODO_NAME", "Nodo ?")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user="root",
        password="root",
        database="informacion"
    )

@app.route("/")
def index():
    return render_template("index.html", nodo=NODO_NAME, db=DB_HOST)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre      = request.form["nombre"]
    correo      = request.form["correo"]
    formacion   = request.form["formacion"]
    experiencia = request.form["experiencia"]

    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO informacion (nombre, correo, formacion, experiencia) VALUES (%s, %s, %s, %s)",
            (nombre, correo, formacion, experiencia)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        return f"Error al insertar: {e}", 500

    return redirect("/")

# API JSON para que el HTML consulte y agregue sin recargar
@app.route("/api/informacion")
def api_informacion():
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM informacion ORDER BY id DESC")
        registros = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify({"nodo": NODO_NAME, "db": DB_HOST, "data": registros})
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/agregar", methods=["POST"])
def api_agregar():
    data        = request.get_json()
    nombre      = data.get("nombre")
    correo      = data.get("correo")
    formacion   = data.get("formacion")
    experiencia = data.get("experiencia")

    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO informacion (nombre, correo, formacion, experiencia) VALUES (%s, %s, %s, %s)",
            (nombre, correo, formacion, experiencia)
        )
        conexion.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return jsonify({"success": True, "id": new_id, "nodo": NODO_NAME, "db": DB_HOST})
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
