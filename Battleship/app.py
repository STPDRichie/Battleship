from modules import game_status
from modules.player import Player

from flask import Flask, render_template, request, url_for

app = Flask(__name__)

person = Player()
opponent = Player()


@app.route('/')
def index():
    return render_template('index.html', game_panel_text='Start game')


@app.route('/game_button_clicked', methods=['POST'])
def response_to_button_click():
    current_status = request.form['current_status']
    return game_status\
        .change_game_status(current_status)


@app.route('/person_cell_clicked', methods=['POST'])
def response_to_player_cell_click():
    current_status = request.form['game_status']
    current_ship = request.form['current_ship']
    ship_direction = request.form['direction']
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']
    return game_status\
        .change_person_cells(cell_icon, cell_id,
                             current_ship, ship_direction,
                             current_status)


@app.route('/opponent_cell_clicked', methods=['POST'])
def response_to_ai_cell_click():
    current_status = request.form['game_status']
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']
    return game_status\
        .change_opponent_cell(cell_icon, cell_id, current_status)


if __name__ == '__main__':
    app.run(debug=True)
