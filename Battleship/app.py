from flask import Flask, render_template, request, url_for


status_text_start = 'Start game'
status_text_place_ships = 'Place your ships'
status_text_battle = 'Battle'

icon_solid = '<i class="fa-solid"></i>'
icon_circle = '<i class="fa-solid fa-circle"></i>'
icon_crossedCircle = '<i class="fa-solid fa-circle-xmark"></i>'
icon_emptyCircle = '<i class="fa-regular fa-circle"></i>'

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', game_panel_text='Start game')


@app.route('/', methods=['POST'])
def response_to_cell_click():
    board = request.form['board']
    game_status = request.form['game_status']
    cell = request.form['cell']

    if board == 'player':
        if game_status != status_text_start:
            return {'is_changed': True,
                    'game_status': status_text_battle,
                    'cell': icon_emptyCircle}

    return {'is_changed': False}
# def return_result_js_data():
#     game_status = request.form['game_status']
#     cell = request.form['cell']
#     cell = icon_circle
#     result = {'game_status': game_status, 'cell': cell}
#     return result


if __name__ == '__main__':
    app.run(debug=True)
