import pandas as pd

from app import app

from flask import render_template, request, session
#import sqlite3
from utils import get_db_connection
from models.about_model import *
@app.route('/about', methods=['get'])

def about():
    conn = get_db_connection()
    if request.args.get('tournament_number') == None:
        tournament_number = 1
    else:
        tournament_number = request.args.get('tournament_number')

    df_tournaments = get_tournaments(conn)

    if request.args.get('add_tournament') == None:
        add = False
        cur_tournament = get_cur_tournament(conn, tournament_number)
    else:
        add = True
        cur_tournament = pd.DataFrame()
    #print(request.query_string.decode())

    if request.args.get('сохранить') != None:
        set_tournament(conn, tournament_number,
                       name=request.args.get('name'),
                       systemID=request.args.get('system'),
                       start=request.args.get('start_date'),
                       end=request.args.get('end_date'),
                       description=request.args.get('description'),
                       control=request.args.get('control'),
                       tables=request.args.get('tournament_tables'))

    if request.args.get('добавить') != None:
        add_tournament(conn,
                       name=request.args.get('name'),
                       systemID=request.args.get('system'),
                       start=request.args.get('start_date'),
                       end=request.args.get('end_date'),
                       description=request.args.get('description'),
                       control=request.args.get('control'),
                       tables=request.args.get('tournament_tables'))


    # выводим форму
    html = render_template(
        'about.html',
        tournaments = df_tournaments,
        tournament_number = tournament_number,
        cur_tournament = cur_tournament,
        add = add,
        len = len,
    )
    return html

