from flask import Flask, request, Response, current_app
from time import sleep
import requests
import json

from coalesce import coalesce

app = Flask(__name__)
if app.config['ENV'] == 'development':
    app.config['TESTING'] = True
    app.config['API_URLS'] = [
        "http://localhost:5000/api1",
        "http://localhost:5000/api2",
        "http://localhost:5000/api3"
    ]

@app.route('/coalesce')
def handle():
    strategy = request.args.get('strategy', '')
    try:
        member_id = int(request.args.get('member_id'))
        return coalesce.get(member_id, strategy, app.config['API_URLS'])
    except (TypeError, ValueError) as err:
        return Response(str(err), status=400)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError) as err:
        return Response(str(err), status=500)

if app.config['TESTING']:
    @app.route('/api1')
    def api1():
        return {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}

    @app.route('/api2')
    def api2():
        return {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000}

    @app.route('/api3')
    def api3():
        return {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000}

    @app.route('/slow')
    def slow():
        sleep(3)
        return {'deductible': 1, 'stop_loss': 1, 'oop_max': 1}

    @app.route('/fast')
    def fast():
        return {'deductible': 2, 'stop_loss': 2, 'oop_max': 2}

    @app.route('/extra')
    def extra():
        return {'deductible': 999999,
                'stop_loss': 999999,
                'oop_max': 999999,
                'extra': 1}
