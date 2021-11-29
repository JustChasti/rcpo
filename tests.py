from datetime import time
import requests
import json
import time


def test_registration():
    data = {
        "login": "Abcd",
        "password": "qwerty",
        "email": "kot@gmail.com"
    }
    url = 'user/registration'
    answer = requests.post(f'http://127.0.0.1:5000/{url}', data=json.dumps(data))
    print(answer.status_code)
    print(answer.json())


def test_autorization():
    data = {
        "login": "Abcde",
        "password": "qwerty"
    }
    url = 'user/autorization'
    answer = requests.get(f'http://127.0.0.1:5000/{url}', data=json.dumps(data))
    print(answer.status_code)
    print(answer.json())


def test_connect1():
    data = {
        "login": "Abcd",
        "password": "qwerty"
    }
    url = '/user/connect'
    answer = requests.put(f'http://127.0.0.1:5000/{url}', data=json.dumps(data))
    print(answer.status_code)
    print(answer.json())


def test_connect2():
    data = {
        "login": "Abcde",
        "password": "qwerty"
    }
    url = '/user/connect'
    answer = requests.put(f'http://127.0.0.1:5000/{url}', data=json.dumps(data))
    print(answer.status_code)
    print(answer.json())


def test_wl2():
    data = {
        "login": "Abcde",
        "password": "qwerty"
    }
    url = '/user/win'
    answer = requests.put(f'http://127.0.0.1:5000/{url}', data=json.dumps(data))
    print(answer.status_code)
    print(answer.json())


def test_wl1():
    data = {
        "login": "Abcd",
        "password": "qwerty"
    }
    url = '/user/win'
    answer = requests.put(f'http://127.0.0.1:5000/{url}', data=json.dumps(data))
    print(answer.status_code)
    print(answer.json())


test_autorization()

"""
test_connect1()
time.sleep(1)
test_connect2()
time.sleep(1)
test_connect1()

time.sleep(2)
test_wl2()
time.sleep(1)
test_wl1()
"""