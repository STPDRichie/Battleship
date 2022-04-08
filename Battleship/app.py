from modules import game_status

from flask import Flask, render_template, request, url_for


# status_text_start = 'Start game'
# status_text_place_ships = 'Ships placing'
# status_text_battle = 'Battle'
#
# needs_text_start = 'Click the button to start game'
# needs_text_place = 'Place ship'

# icon_solid = '<i class="fa-solid"></i>'
# icon_circle = '<i class="fa-solid fa-circle"></i>'
# icon_crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>'
# icon_emptyCircle = '<i class="fa-regular fa-circle"></i>'

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

    response = game_status\
        .change_game_status(current_status, current_needs)

    return response


@app.route('/cell_clicked', methods=['POST'])
def response_to_cell_click():
    board = request.form['board']
    current_status = request.form['game_status']
    cell = request.form['cell']

    response = current_status\
        .change_board_cell(board, current_status, cell)

    return response


if __name__ == '__main__':
    app.run(debug=True)
