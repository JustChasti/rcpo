import json
import random
from flask import Blueprint, request, jsonify
from loguru import logger
from db.db import user_collection
from models.lobby import Lobby


bp = Blueprint('views', __name__)

# что в лобби {username: ... time: ...}
global_lobby = Lobby()


@bp.route("/user/registration", methods=["POST"])
def registration():
    try:
        data = request.get_json(force=True)
        user_model = {
            "login": data["login"],
            "password": data["password"],
            "email": data["email"],
            "games": 0,
            "wins": 0
        }
    except Exception as e:
        logger.exception(e)
        return (
            json.dumps({'info': 'Wrong data'}),
            406,
            {'ContentType': 'application/json'}
        )
    result = user_collection.find_one({'login': user_model["login"]})
    if result:
        return (
            json.dumps({'info': 'this login was used'}),
            409,
            {'ContentType': 'application/json'}
        )
    result = user_collection.find_one({'email': user_model["email"]})
    if result:
        return (
            json.dumps({'info': 'this email was used'}),
            409,
            {'ContentType': 'application/json'}
        )
    user_collection.insert_one(user_model)
    return (
            json.dumps({'info': 'User created'}),
            200,
            {'ContentType': 'application/json'}
        )


@bp.route("/user/autorization", methods=["GET"])
def autorization():
    try:
        data = request.get_json(force=True)
        user_model = {
            "login": data["login"],
            "password": data["password"]
        }
    except Exception as e:
        logger.exception(e)
        return (
            json.dumps({'info': 'Wrong data'}),
            406,
            {'ContentType': 'application/json'}
        )
    result = user_collection.find_one({'login': user_model["login"]})
    if result:
        if result["password"] == user_model["password"]:
            result['_id'] = str(result['_id'])
            return jsonify(result)
        else:
            return (
                json.dumps({'info': 'password incorrect'}),
                401,
                {'ContentType': 'application/json'}
            )
    else:
        return (
            json.dumps({'info': 'user does not exist'}),
            404,
            {'ContentType': 'application/json'}
        )


@bp.route("/user/connect", methods=["PUT"])
def connect():
    data = request.get_json(force=True)
    try:
        user_model = {
            "login": data["login"],
            "password": data["password"]
        }
    except Exception as e:
        logger.exception(e)
        return (
            json.dumps({'info': 'Wrong data'}),
            406,
            {'ContentType': 'application/json'}
        )
    
    status = global_lobby.check_status(user_model['login'])
    if status:
        if status['status'] == 'in_game':
            return jsonify(status)
    
    return jsonify(global_lobby.add_user(user_model['login']))


@bp.route("/user/win", methods=["PUT"])
def win_lose():
    data = request.get_json(force=True)
    try:
        user_model = {
            "login": data["login"],
            "password": data["password"]
        }
    except Exception as e:
        logger.exception(e)
        return (
            json.dumps({'info': 'Wrong data'}),
            406,
            {'ContentType': 'application/json'}
        )
    
    status = global_lobby.check_status(user_model['login'])
    if status:
        if status['status'] == 'lose':
            return jsonify({'result': "You lose"})
    
    return jsonify(global_lobby.win_lose(user_model['login']))
