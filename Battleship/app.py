import modules.game_status as gs
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

    response = make_response(gs.host_lobby(session_key, username))
    response.set_cookie(
        'session-key',
        value=session_key
    )
    return response


@app.route('/wait_for_member_connect')
def wait_for_member_connect():
    session_key = request.cookies.get('session-key')
    return gs.wait_for_member_connect(session_key)


@app.route('/check_for_member_connection')
def check_for_member_connection():
    session_key = request.cookies.get('session-key')
    return gs.check_for_member_connection(session_key)


@app.route('/connect_to_lobby', methods=['POST'])
def connect_to_lobby():
    session_key = request.form['session_key']
    username = request.form['username']

    connection_response = gs.connect_to_lobby(session_key, username)
    server_response = make_response(connection_response)
    if connection_response['is_changed']:
        server_response.set_cookie(
            'session-key',
            value=session_key
        )
    return server_response


@app.route('/check_for_start_game')
def check_for_start_game():
    session_key = request.cookies.get('session-key')
    return gs.check_for_start_game(session_key)


@app.route('/leave', methods=['POST'])
def leave():
    username = request.form['username']
    session_key = request.cookies.get('session-key')
    return gs.leave(session_key, username)


@app.route('/start_game', methods=['POST'])
def start_game():
    current_status = request.form['current_status']
    session_key = request.cookies.get('session-key')
    game_change_response = gs.start_game(current_status, session_key)
    server_response = make_response(game_change_response)
    if game_change_response['is_changed']:
        server_response.set_cookie(
            'session-key',
            value=session_key
        )
    return server_response


@app.route('/person_cell_hovered', methods=['POST'])
def response_to_person_cell_hover():
    current_status = request.form['game_status']
    ship = request.form['current_ship']
    ship_direction = request.form['direction']
    cell_id = request.form['cell_id']
    return gs.get_person_outline_cells(ship, ship_direction,
                                       cell_id, current_status)


@app.route('/person_cell_clicked', methods=['POST'])
def response_to_person_cell_click():
    current_status = request.form['game_status']
    ship = request.form['current_ship']
    ship_direction = request.form['direction']
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']
    session_key = request.cookies.get('session-key')
    return gs.change_person_cells(cell_icon, cell_id,
                                  ship, ship_direction,
                                  current_status, session_key)


@app.route('/opponent_cell_clicked', methods=['POST'])
def response_to_opponent_cell_click():
    current_status = request.form['game_status']
    cell_id = request.form['cell_id']
    session_key = request.cookies.get('session-key')
    return gs.fire_opponent_cell(cell_id, current_status, session_key)


@app.route('/get_opponent_fire', methods=['POST'])
def fire_person():
    current_status = request.form['game_status']
    session_key = request.cookies.get('session-key')
    return gs.fire_person_cell(current_status, session_key)


@app.route('/get_opponent_remaining_ships', methods=['GET'])
def get_opponent_remaining_ship_cells():
    session_key = request.cookies.get('session-key')
    return gs.get_opponent_remaining_ship_cells(session_key)


@app.route('/restart_game', methods=['GET'])
def restart_game():
    session_key = request.cookies.get('session-key')
    return gs.restart_game(session_key)


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
