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


@app.route('/cell_clicked', methods=['POST'])
def response_to_cell_click():
    board = request.form['board']
    current_status = request.form['game_status']
    current_needs = request.form['current_needs']
    cell_icon = request.form['cell_icon']
    cell_id = request.form['cell_id']

    response = game_status_changer\
        .change_board_cell(board,
                           current_status, current_needs,
                           cell_icon, cell_id)

    return response


if __name__ == '__main__':
    app.run(debug=True)
