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

@app.route("/count")
def count():
    try:
        return {"data count": len(data)}, 200
    except NameError:
        return {"message": "data not defined"}, 500
    

@app.route("/person/<uuid:id>")
def find_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            return person
    return {"message": "person not found"}, 404


@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            data.remove(person)
            return {"message":f"{id}"}, 200

    return {"message": "person not found"}, 400

@app.route("/person", methods=['POST'])
def add_by_uuid():
    new_person = request.json
    if not new_person:
        return {"message": "invalid input parameter"}, 422
    try:
        data.append(new_person)
        
    except NameError:
        return {"message": "data not found"}, 500

    return {"message": f"{new_person['id']} created"}, 200