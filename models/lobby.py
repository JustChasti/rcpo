from datetime import datetime, timedelta
from time import sleep

from db.db import Session, User

delta_wait = 7
delta_game = 180 # максимум катка


class Lobby():
    def __init__(self):
        self.player_list = []
        # структура player_list {username: ... time: ... status: ...}
        self.connections = []
        # структура connections {player: ... player: ... time: ...}

    def clear_lobby(self):
        for i in self.player_list:
            if datetime.now() - i["time"] > timedelta(seconds=delta_wait) and (i["status"] != "in_game" or i["status"] != "lose"):
                self.player_list.remove(i)
            if datetime.now() - i["time"] > timedelta(seconds=delta_game):
                self.player_list.remove(i)

    def clear_connections(self):
        for i in self.connections:
            if datetime.now() - i["time"] > timedelta(seconds=delta_game):
                self.connections.remove(i)

    def check_status(self, username):
        for i in self.player_list:
            if i["username"] == username:
                return {
                    'status': i['status'],
                    'time': i['time'],
                }

    
    def set_status(self, username, status):
        for i in self.player_list:
            if i["username"] == username:
                i['status'] = status



    def add_user(self, username):
        self.clear_lobby()
        user_in_list = False

        user = {
            'username': username,
            'time': datetime.now(),
            'status': 'wait'
        }

        for i in self.player_list:
            if i["username"] == username:
                user_in_list = True
                i["status"] = user['status']
                i["time"] = user['time']
        if not user_in_list:
            self.player_list.append(user)

        for i in self.player_list:
            if i["status"] == "wait":
                if i['username'] != user['username']:
                    user_2 = i
                    self.player_list.remove(i)
                    self.player_list.remove(user)

                    gamestart = datetime.now() + timedelta(seconds=delta_wait + 2)

                    user_2['status'] = 'in_game'
                    user_2['time'] = gamestart

                    user['status'] = 'in_game'
                    user['time'] = gamestart

                    self.player_list.append(user)
                    self.player_list.append(user_2)
                    
                    connection = {
                        'player_1': user['username'],
                        'player_2': user_2['username'],
                        'time': gamestart
                    }
                    self.connections.append(connection)

                    session = Session()
                    result = session.query(User).filter_by(login=user["username"]).first()
                    result.games += 1

                    result = session.query(User).filter_by(login=user_2["username"]).first()
                    result.games += 1

                    session.commit()
                    session.close()

                    return {
                        'status':user['status'],
                        'time': gamestart
                    }

        return {
            'status':user['status'],
            'time': 0
        }

    def win_lose(self, username):
        for i in self.player_list:
            if i["username"] == username and i["status"] == 'in_game':
                for j in self.connections:
                    if j["player_1"] == username:
                        self.set_status(j["player_2"], 'lose')
                        self.connections.remove(j)
                        self.player_list.remove(i)
                        return {'result': "You win"}
                    if j["player_2"] == username:
                        self.set_status(j["player_1"], 'lose')
                        self.connections.remove(j)
                        self.player_list.remove(i)
                        return {'result': "You win"}
                self.player_list.remove(i)
                return {'result': "You lose"}
            if i["username"] == username and i["status"] == 'lose':
                self.player_list.remove(i)
                return {'result': "You lose"}
        return {'result': "Error"}
 


def test_lobby():
    global_lobby = Lobby()

    chek = global_lobby.check_status('Kot')
    if not chek or chek['status'] == "wait":
        print(global_lobby.add_user('Kot'))

    sleep(3)

    chek = global_lobby.check_status('Gray')
    if not chek or chek['status'] == "wait":
        print(global_lobby.add_user('Gray'))

    chek = global_lobby.check_status('Kot')
    if not chek or chek['status'] == "wait":
        print(global_lobby.add_user('Kot'))

    sleep(1)

    print(global_lobby.win_lose('Gray'))
    # print(global_lobby.win_lose('Kot'))
    print(global_lobby.add_user('Kot'))

    print(global_lobby.player_list)
    print(global_lobby.connections)
