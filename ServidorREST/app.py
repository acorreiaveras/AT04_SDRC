from flask import Flask, request, Response, jsonify
import requests
import json
from flask_cors import CORS
from json2xml import json2xml
from json2xml.utils import readfromjson
import breed_pb2
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('FAVORITE_DOG_API')

@app.route('/api/breeds', methods=['GET'])
def get_breeds():
    url = "https://api.thedogapi.com/v1/breeds"

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url=url, headers=headers)

    if response.status_code == 200:
        response_format = request.headers['Content-Type']

        if response_format == 'application/xml':
            xml_response = generate_xml_response_breeds(response)
            return Response(xml_response, mimetype='text/xml')
        if response_format == 'application/x-protobuf':
            protobuf_response = generate_protobuf_response_breeds (response)
            return Response(protobuf_response, mimetype='application/x-protobuf')
        else:
            json_response = generate_json_response_breeds(response)
            return jsonify(json_response)

    else:
        return jsonify({'error': 'Failed to retrieve breeds'}), 400
    

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    url = "https://api.thedogapi.com/v1/favourites"

    payload={}
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url=url, headers=headers, data=payload)

    if response.status_code == 200:
        response_format = request.headers['Content-Type']

        if response_format == 'application/xml':
            xml_response = generate_xml_response(response)
            return Response(xml_response, mimetype='text/xml')
        else:
            json_response = generate_json_response(response)
            return jsonify(json_response)
    
    else:
        return jsonify({'error': 'Failed to retrieve favorites'}), 400
    

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    payload = json.dumps(request.json)
    print(payload)
    url = "https://api.thedogapi.com/v1/favourites"

    headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url=url, headers=headers, data=payload)

    if response.status_code == 200:
        response_format = request.headers['Content-Type']

        if response_format == 'application/xml':
            xml_response = generate_xml_response(response)
            return Response(xml_response, mimetype='text/xml')
        else:
            json_response = generate_json_response(response)
            return jsonify(json_response)

    else:
        return jsonify({'error': 'Failed to add favorite'}), 400


@app.route('/api/favorites/<favoriteid>', methods=['DELETE'])
def delete_favorite(favoriteid):
    url = "https://api.thedogapi.com/v1/favourites/" + favoriteid

    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url=url, headers=headers)

    if response.status_code == 200:
        response_format = request.headers['Content-Type']

        if response_format == 'application/xml':
            xml_response = generate_xml_response(response)
            return Response(xml_response, mimetype='text/xml')
        else:
            json_response = generate_json_response(response)
            return jsonify(json_response)

    else:
        return jsonify({'error': 'Failed to delete favorite'}), 400

def generate_json_response_breeds(data):
    breeds = data.json()
    breedsList = []

    for breed in breeds:
        breedsList.append({
            'name': breed['name'], 
            'reference_image_id': breed['reference_image_id'],
            'image': breed['image']
        })

    return breedsList

def generate_xml_response_breeds(data):
    breeds = generate_json_response_breeds(data)

    xml_data = json2xml.Json2xml(breeds).to_xml()

    return xml_data    

def generate_xml_response(data):
    xml_data = json2xml.Json2xml(data.json()).to_xml()

    return xml_data    

def generate_protobuf_response_breeds (data):
    breeds = generate_json_response(data)
    breed_messages = []

    for breed in breeds:
        breed_message = breed_pb2.Breed()

        breed_message.name = breed['name']
        breed_message.reference_image_id = breed['reference_image_id']

        image_message = breed_message.image
        image_message.id = breed['image']['id']
        image_message.width = breed['image']['width']
        image_message.height = breed['image']['height']
        image_message.url = breed['image']['url']

        breed_messages.append(breed_message)

    breeds_response = breed_pb2.BreedsResponse()
    breeds_response.breeds.extend(breed_messages) 

    protobuf_data = breeds_response.SerializeToString()

    return protobuf_data

def generate_json_response(data):
    return data.json()

if __name__ == '__main__':
    app.run()