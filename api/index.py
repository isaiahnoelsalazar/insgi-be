from flask import Flask, jsonify, request
import pymssql
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return 'insgi-be'

@app.route('/about')
def about():
    return sys.version

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

        data = {"response_data": data.strip()[:-1]}
        connection.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({"response_data": str(e)})

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

        return jsonify({"response_data": "Command completed."})
    except:
        return jsonify({"response_data": "Connection broken. Please check your parameters again."})