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
    player1_name = request.form['player1_name']
    session_key = request.form['session_key']

    lobby = Lobby(session_key, player1_name)
    lobbies.append(lobby)

    response = make_response()
    response.set_cookie(
        'session-key',
        value=session_key
    )
    return response


@app.route('/status_button_clicked', methods=['POST'])
def response_to_status_button_click():
    current_status = request.form['current_status']
    session_key = request.form['session_key']
    player1_name = request.form['player1_name']
    player2_name = request.form['player2_name']
    game_response = gs.change_game_status(current_status, session_key,
                                          player1_name, player2_name)
    server_response = make_response(game_response)
    if game_response['is_changed']:
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


@app.route('/restart_button_clicked', methods=['GET'])
def restart_game():
    session_key = request.cookies.get('session-key')
    return gs.reset_game(session_key)


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
