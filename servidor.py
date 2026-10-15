import sqlite3;
import bcrypt;
from flask import Flask, request, jsonify;

app = Flask(__name__)
DB= "tareas.db"

def get_db(): #conexión con la base de datos
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn: 
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    contraseña_hash BLOB NOT NULL
                    )
        """)

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "").strip()
    contraseña = datos.get("contraseña", "")

    if not usuario or not contraseña:
        return jsonify({"error": "Falta usuario o contraseña"}), 400
    
    hash_ = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt())

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)",
                (usuario, hash_),
            )
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "").strip()
    contraseña = datos.get("contraseña", "")

    with get_db() as conn:
        fila = conn.execute(
            "SELECT contraseña_hash FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()

    if fila and bcrypt.checkpw(contraseña.encode("uft-8"), fila["contraseña_hash"]):
        return jsonify({"mensaje": "Login exitoso!!", "tareas": "/tareas"}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401

@app.route("/tareas", methods=["GET"])
def tareas():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Tareas</title></head>
    <body>
        <h1>¡Bienvenido al Sistema de Gestión de Tareas!</h1>
        <p>Has accedido correctamente.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
