import pytest
import requests
import json
from coalesce import coalesce

BASE_URL='http://localhost:5000/coalesce?'

def test_ok():
    r = requests.get('{}{}'.format(BASE_URL, 'member_id=1'))
    assert r.status_code == 200

def test_bad_strategy():
    r = requests.get('{}member_id=1&strategy=bad'.format(BASE_URL))
    assert r.status_code == 400

def test_bad_member_id():
    r = requests.get('{}member_id=bad'.format(BASE_URL))
    assert r.status_code == 400

def test_average():
    r = requests.get('{}member_id=1'.format(BASE_URL))
    assert r.json() == {'deductible': 1066, 'oop_max': 5666, 'stop_loss': 11000}

def test_min():
    r = requests.get('{}member_id=1&strategy=min'.format(BASE_URL))
    assert r.json() == {'deductible': 1000, 'oop_max': 5000, 'stop_loss': 10000}

def test_max():
    r = requests.get('{}member_id=1&strategy=max'.format(BASE_URL))
    assert r.json() == {'deductible': 1200, 'oop_max': 6000, 'stop_loss': 13000}

def test_frequent():
    r = requests.get('{}member_id=1&strategy=frequent'.format(BASE_URL))
    assert r.json() == {'deductible': 1000, 'oop_max': 6000, 'stop_loss': 10000}

def test_random():
    rj = requests.get('{}member_id=1&strategy=random'.format(BASE_URL)).json()
    assert rj['deductible'] == 1000 or rj['deductible'] == 1200
    assert rj['oop_max'] == 5000 or rj['oop_max'] == 6000
    assert rj['stop_loss'] == 10000 or rj['stop_loss'] == 13000

def test_random2():
    rj = requests.get('{}member_id=1&strategy=random2'.format(BASE_URL)).json()
    assert (rj == {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}
            or rj == {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000}
            or rj == {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000})

def test_fastest():
    urls = ['http://localhost:5000/slow',
            'http://localhost:5000/fast']
    r = coalesce.get(1, 'fastest', urls)
    assert r == {'deductible': 2, 'stop_loss': 2, 'oop_max': 2}

def test_extra():
    urls = ['http://localhost:5000/api1',
            'http://localhost:5000/extra']
    r = coalesce.get(1, 'min', urls)
    assert r == {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000, 'extra': 1}
