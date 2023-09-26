import json
from flask import Flask, jsonify, request

from model.twit import Twit
from model.user import User

twits = []

app = Flask(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Twit, User)):
            return obj.to_dict()
        return super().default(obj)


app.json_encoder = CustomJSONEncoder


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong'})


@app.route('/twit', methods=['POST'])
def create_twit():
    twit_json = request.get_json()
    twit = Twit(twit_json['body'], User(twit_json['author']))
    twits.append(twit)
    return jsonify({'status': 'success'})


@app.route('/twit', methods=['GET'])
def read_twits():
    twits_dict = [twit.to_dict() for twit in twits]
    return jsonify({'twits': twits_dict})


@app.route('/twit/<int:index>', methods=['PUT'])
def update_twit(index):
    if 0 <= index < len(twits):
        twit_json = request.get_json()
        twit = twits[index]
        twit.body = twit_json['body']
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Invalid index'})


@app.route('/twit/<int:index>', methods=['DELETE'])
def del_twit(index):
    if 0 <= index < len(twits):
        del twits[index]
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Invalid index'})


if __name__ == '__main__':
    app.run(debug=True)
