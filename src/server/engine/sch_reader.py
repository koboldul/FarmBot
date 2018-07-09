import json
import os.path

class ScheduleReader:
    @staticmethod
    def get_devices():
        script_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(script_path, "../data/sch.json")
        with open(path) as json_file:
            return json.load(json_file)['devices']
       
     