from dataclasses import asdict


import modules.game_status as gs
import modules.lobby_status as ls

from modules.game import Game
from modules.lobby import Lobby

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

games = []
lobbies = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/host_lobby', methods=['POST'])
def host_lobby():
    session_key = request.form['session_key']
    username = request.form['username']
    
    response = make_response(asdict(ls.host_lobby(session_key, username)))
    response.set_cookie(
        'session-key',
        value=session_key
    )
    return response


@app.route('/wait_for_member_connect')
def wait_for_member_connect():
    session_key = request.cookies.get('session-key')
    return asdict(ls.wait_for_member_connect(session_key))


@app.route('/check_is_member_in_lobby')
def check_is_member_in_lobby():
    session_key = request.cookies.get('session-key')
    return asdict(ls.check_is_member_in_lobby(session_key))


@app.route('/connect_to_lobby', methods=['POST'])
def connect_to_lobby():
    session_key = request.form['session_key']
    username = request.form['username']
    
    connection_response = asdict(ls.connect_to_lobby(session_key, username))
    server_response = make_response(connection_response)
    if connection_response['is_changed']:
        server_response.set_cookie(
            'session-key',
            value=session_key
        )
    return server_response


@app.route('/wait_for_start_game')
def wait_for_start_game():
    session_key = request.cookies.get('session-key')
    return asdict(ls.wait_for_start_game(session_key))


@app.route('/leave', methods=['POST'])
def leave():
    session_key = request.cookies.get('session-key')
    username = request.form['username']
    return asdict(ls.leave(session_key, username))


@app.route('/wait_for_opponent_ready_for_battle', methods=['POST'])
def wait_for_opponent_ready_for_battle():
    session_key = request.cookies.get('session-key')
    username = request.form['username']
    return asdict(gs.wait_for_opponent_ready_for_battle(session_key, username))


@app.route('/start_game', methods=['POST'])
def start_game():
    session_key = request.cookies.get('session-key')
    current_status = request.form['current_status']
    return asdict(gs.start_game(session_key, current_status))


@app.route('/restart_game', methods=['GET'])
def restart_game():
    session_key = request.cookies.get('session-key')
    return asdict(gs.restart_game(session_key))


@app.route('/get_ship_outline_cells', methods=['POST'])
def get_ship_outline_cells():
    session_key = request.cookies.get('session-key')
    username = request.form['username']
    ship = request.form['current_ship']
    ship_direction = request.form['direction']
    cell_id = request.form['cell_id']
    return asdict(gs.get_ship_outline_cells(session_key, username, ship,
                                            ship_direction, cell_id))


@app.route('/person_cell_clicked', methods=['POST'])
def response_to_person_cell_click():
    session_key = request.cookies.get('session-key')
    username = request.form['username']
    current_status = request.form['game_status']
    ship = request.form['current_ship']
    ship_direction = request.form['direction']
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']
    return asdict(gs.change_person_cells(session_key, username,
                                         cell_icon, cell_id, ship,
                                         ship_direction, current_status))


@app.route('/fire_opponent_cell', methods=['POST'])
def fire_opponent_cell():
    session_key = request.cookies.get('session-key')
    username = request.form['username']
    current_status = request.form['game_status']
    cell_id = request.form['cell_id']
    return asdict(gs.fire_opponent_cell(session_key, username,
                                        cell_id, current_status))


@app.route('/get_opponent_turn', methods=['POST'])
def get_opponent_turn():
    session_key = request.cookies.get('session-key')
    username = request.form['username']
    current_status = request.form['game_status']
    return asdict(gs.get_opponent_turn(session_key, username, current_status))


@app.route('/get_opponent_remaining_ships', methods=['POST'])
def get_opponent_remaining_ship_cells():
    session_key = request.cookies.get('session-key')
    username = request.form['username']
    return asdict(gs.get_opponent_remaining_ship_cells(session_key, username))


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
