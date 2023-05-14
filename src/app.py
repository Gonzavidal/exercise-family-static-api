"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    fetch_member=jackson_family.get_member(member_id)
    if fetch_member:
        return jsonify(fetch_member), 200
    else:
        return jsonify({"status_code": 400})

@app.route('/member/', methods=['POST'])
def add_member():
    get_name= request.json.get("first_name")
    get_age= request.json.get("age")
    get_lucky_numbers= request.json.get("lucky_numbers")

    if not get_name: return jsonify({"status_code": 400})
    if not get_age: return jsonify({"status_code": 400})
    if not get_lucky_numbers: return jsonify({"status_code": 400})

    member = {
        "id": request.json.get("id") if request.json.get("id") is not None else jackson_family._generateId(),
        "first_name": get_name,
        "last_name": jackson_family.last_name,
        "age": get_age,
        "lucky_numbers": get_lucky_numbers
    }

    response = jackson_family.add_member(member)

    return jsonify({"status_code": response})

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member_selected = jackson_family.delete_member(member_id)   
    if member_selected:
        return jsonify({"status_code": 200, "done": True})
    else:
        return jsonify({"status_code": 400, "done": False}) 


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
