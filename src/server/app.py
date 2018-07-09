from flask import Flask
from flask_cors import CORS
from flask import jsonify

from bp.schedule_blueprint import schedule

DEBUG=True

app = Flask(__name__)
CORS(app)

app.register_blueprint(schedule)

if (__name__ == "__main__"):
    app.run()