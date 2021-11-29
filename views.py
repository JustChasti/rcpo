import json
import random
from flask import Blueprint, request, jsonify
from loguru import logger
from db.db import Session, User
from models.lobby import Lobby


bp = Blueprint('views', __name__)

# что в лобби {username: ... time: ...}
global_lobby = Lobby()


@bp.route("/user/registration", methods=["POST"])
def registration():
    session = Session()
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
    result = session.query(User).filter_by(login=user_model["login"]).all()
    if result:
        return (
            json.dumps({'info': 'this login was used'}),
            409,
            {'ContentType': 'application/json'}
        )
    result = session.query(User).filter_by(email=user_model["email"]).all()
    if result:
        return (
            json.dumps({'info': 'this email was used'}),
            409,
            {'ContentType': 'application/json'}
        )
    model = User(login=user_model["login"], password=user_model["password"], email=user_model["email"], games=user_model["games"], wins=user_model["wins"])
    session.add(model)
    session.commit()
    session.close()
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
    session = Session()
    result = session.query(User).filter_by(login=user_model["login"]).first()
    session.close()
    print(result)
    if result:
        if result.password== user_model["password"]:
            return (
                json.dumps({
                    'info': 'autorized',
                    'username': result.login,
                    'games': result.games,
                    'wins': result.wins
                    }),
                201,
                {'ContentType': 'application/json'}
            )
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
    
    session = Session()
    result = session.query(User).filter_by(login=user_model["login"]).first()
    result.wins += 1
    session.commit()
    session.close()
    return jsonify(global_lobby.win_lose(user_model['login']))
