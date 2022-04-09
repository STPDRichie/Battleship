from modules import game_status_changer

from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           game_panel_text='Start game',
                           game_needs_text='Click the button to start game')


@app.route('/game_button_clicked', methods=['POST'])
def response_to_button_click():
    current_status = request.form['current_status']
    current_needs = request.form['current_needs']

    response = game_status_changer\
        .change_game_status(current_status)

    return response


@app.route('/player_cell_clicked', methods=['POST'])
def response_to_player_cell_click():
    ship_direction = request.form['direction']
    current_status = request.form['game_status']
    current_ship = request.form['current_needs'].split()[1]
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']

    return game_status_changer\
        .change_player_cell(cell_icon, cell_id,
                            current_ship, ship_direction,
                            current_status)


@app.route('/ai_cell_clicked', methods=['POST'])
def response_to_ai_cell_click():
    current_status = request.form['game_status']
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']

    return game_status_changer\
        .change_ai_cell(cell_icon, cell_id, current_status)


if __name__ == '__main__':
    app.run(debug=True)
