import os

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "workflowdb")
DB_USER = os.getenv("DB_USER", "workflowuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "workflowpass")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        connect_timeout=3,
    )


@app.route("/")
def home():
    return "WorkFlowLab is running"


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/users")
def users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = [{"id": row[0], "name": row[1]} for row in rows]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "error": "database unavailable",
            "details": str(e)
        }), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
