import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import executor_utils as eu 


app = Flask(__name__)
CORS(app)

@app.route('/build_and_run', methods=['POST'])
def build_and_run():

    data = request.get_json()

    if data.get('code') is None or data.get('id') is None or data.get('lang') is None : 
        return 'Information is Insufficient'

    id = data['id']
    code = data['code']
    lang = data['lang']

    result = eu.build_and_run(code, lang, id)

    return jsonify(result)

if __name__ == '__main__':
       
    eu.client.images.get("ubuntu:onlineoj")
    app.run(debug=True)
