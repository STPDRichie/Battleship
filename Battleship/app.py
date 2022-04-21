from modules import game_status
from modules.player import Player
from modules.robot import Robot

from flask import Flask, render_template, request


app = Flask(__name__)

person = Player()
robot = Robot()


@app.route('/')
def index():
    return render_template('index.html', game_panel_text='Start game')


@app.route('/status_button_clicked', methods=['POST'])
def response_to_status_button_click():
    current_status = request.form['current_status']
    return game_status\
        .change_game_status(current_status)


@app.route('/person_cell_hovered', methods=['POST'])
def response_to_person_cell_hover():
    current_status = request.form['game_status']
    ship = request.form['current_ship']
    ship_direction = request.form['direction']
    cell_id = request.form['cell_id']
    return game_status\
        .get_person_outline_cells(ship, ship_direction,
                                  cell_id, current_status)


@app.route('/person_cell_clicked', methods=['POST'])
def response_to_person_cell_click():
    current_status = request.form['game_status']
    ship = request.form['current_ship']
    ship_direction = request.form['direction']
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']
    return game_status\
        .change_person_cells(cell_icon, cell_id,
                             ship, ship_direction,
                             current_status)


@app.route('/opponent_cell_clicked', methods=['POST'])
def response_to_opponent_cell_click():
    current_status = request.form['game_status']
    cell_id = request.form['cell_id']
    return game_status\
        .fire_opponent_cell(cell_id, current_status)


@app.route('/get_opponent_fire', methods=['POST'])
def fire_person():
    current_status = request.form['game_status']
    return game_status.fire_person_cell(current_status)


@app.route('/get_opponent_remaining_ships', methods=['GET'])
def get_opponent_remaining_ship_cells():
    return game_status.get_opponent_remaining_ship_cells()


if __name__ == '__main__':
    app.run(debug=True)
