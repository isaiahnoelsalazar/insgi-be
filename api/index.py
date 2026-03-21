from flask import Flask, jsonify, request
from flask_cors import CORS
import pymssql
import sys
import os
from PythonSimpleFunctions import bake

app = Flask(__name__)
CORS(app)

def get_connection():
    return pymssql.connect(
        os.environ.get("DB_SERVER"),
        os.environ.get("DB_USER"),
        os.environ.get("DB_PASS"),
        os.environ.get("DB_NAME")
    )

@app.route("/")
def home():
    return jsonify(bake("insgi-be"))

@app.route("/about")
def about():
    return jsonify(bake(sys.version))

@app.route("/test")
def test():
    return jsonify(bake("Test JSON"))

@app.route("/api/test", methods=["GET"])
def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(as_dict=True)

        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME")
        rows = cursor.fetchall()

        conn.close()
        return jsonify(rows)

    except Exception as e:
        return jsonify(bake(str(e))), 500

@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(as_dict=True)

        cursor.execute("SELECT id, name FROM Users")
        rows = cursor.fetchall()

        conn.close()
        return jsonify(rows)

    except Exception as e:
        return jsonify(bake(str(e))), 500

@app.route("/api/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        name = data.get("name")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Users (name) VALUES (%s)",
            (name,)
        )
        conn.commit()
        conn.close()

        return jsonify(bake("User created successfully"))

    except Exception as e:
        return jsonify(bake(str(e))), 500

@app.route("/mssql_query")
def python_mssql_query():
    try:
        server = request.args.get("server")
        database = request.args.get("database")
        username = request.args.get("username")
        password = request.args.get("password")
        query = request.args.get("query")

        connection = pymssql.connect(server, username, password, database)

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        data = ""

        for row in rows:
            data += str(row) + ","

        data = bake(data.strip()[:-1])
        connection.close()

        return jsonify(data)
    except:
        return jsonify(bake("Connection broken. Please check your parameters again."))

@app.route("/mssql_execute")
def python_mssql_execute():
    try:
        server = request.args.get("server")
        database = request.args.get("database")
        username = request.args.get("username")
        password = request.args.get("password")
        execute = request.args.get("execute")

        connection = pymssql.connect(server, username, password, database)

        cursor = connection.cursor()
        cursor.execute(execute)
        connection.commit()
        connection.close()

        return jsonify(bake("Command completed."))
    except:
        return jsonify(bake("Connection broken. Please check your parameters again."))