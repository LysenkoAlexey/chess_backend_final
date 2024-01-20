from app import app

from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import *
@app.route('/', methods=['get'])

def index():
    conn = get_db_connection()
    if request.args.get('tournament_number') == None:
        tournament_number = 1
    else:
        tournament_number = request.args.get('tournament_number')
    df_players = get_tournament_players(conn, tournament_number)
    df_tournaments = get_tournaments(conn)

    if request.args.get('state') == 'добавить':
        find_player = True
    else:
        find_player = False

    if request.values.get('сохранить'):
        if request.values.get('FIO') and request.values.get('datebirth'):
            FIO = request.values.get('FIO')
            datebirth = request.values.get('datebirth')
            add_to_tournament(conn, FIO, datebirth, tournament_number)

    if request.values.get('найти'):
        searcher=True
        if request.values.get('FIO'):
            FIO = request.values.get('FIO')
            new_players = find_players(conn, FIO)
    else:
        searcher=False
        new_players = pd.DataFrame()


    if request.values.get('delete_player'):
        delete_player(conn, request.values.get('delete_player'), tournament_number)

    if request.values.get('add_player'):
        ID = request.values.get('add_player')
        add_to_tournament_easy(conn, ID, tournament_number)


    html = render_template(
        'index.html',
        tournament_players = df_players,
        tournaments = df_tournaments,
        tournament_number = tournament_number,
        find_player = find_player,
        new_players = new_players,
        searcher = searcher,
        len = len,
    )
    return html

