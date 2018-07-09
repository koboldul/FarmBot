from flask import Blueprint
from flask import jsonify
from flask import request
from engine.engine import Engine

import os.path

import json

schedule = Blueprint('schedule', __name__, template_folder='templates')
engine = Engine()

@schedule.route("/schedule", methods=['GET'])
def get_schedule():
    data = get_schedule_from_file()
    
    return jsonify( {'devices': data, 'status': 'success' })


@schedule.route("/schedule", methods=['POST'])
def add_timeslot():
    response_object = {'status': 'success'}
    
    return jsonify( {'devices': response_object, 'status': 'success' })

@schedule.route("/toggle_device", methods=['POST'])
def toggle_device():
    response_object = {'status': 'success'}
    id = request.get_json().get('id')

    if id == 'all':
        engine.stop_all()
    else:
        op = request.get_json().get('should_start')

        if bool(op):
            engine.start_device(id)
        else:
            engine.stop_device(id)

    return jsonify( {'devices': response_object, 'status': 'success' })

@schedule.route("/logs", methods=['GET'])
def get_logs():
    data =  engine.get_logs()
    
    return jsonify( {'logs': data, 'status': 'success' })

def get_schedule_from_file():
    data = None

    f_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(f_path, "../data/sch.json")

    try: 
        with open(data_path) as f:
            data = json.load(f)
    except IOError:
        print ("Nu such file")

    return data['devices']