from flask import Flask, make_response, request
from data import data 

app = Flask(__name__)



@app.route("/")
def index():
    return "hello world"

@app.route("/no_content")
def no_content():
    return ({"message":"No content found"}, 204)

@app.route("/exp")
def index_explicit():
    resp = make_response({"message": "Hello World"})
    resp.status_code = 200
    return resp

@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of lenght {len(data)} found"}
        else:
            return {"message": "data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    query = request.args.get("q")

    if not query:
        return {"message": "Invalid input parameter"}
    
    for person in data:
        if query.lower() in person["first_name"].lower():
            return person

    return ({"message": "Person not found"}, 400)