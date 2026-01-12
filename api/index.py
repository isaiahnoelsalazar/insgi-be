from flask import Flask, jsonify, request
import pymssql
import sys
from PythonSimpleFunctions import bake

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(bake("insgi-be"))

@app.route("/about")
def about():
    return jsonify(bake(sys.version))

@app.route("/test")
def test():
    return jsonify(bake("Test JSON"))

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