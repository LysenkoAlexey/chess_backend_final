import pandas as pd

from app import app

from flask import render_template, request, session
#import sqlite3
from utils import get_db_connection
from models.judges_model import *
@app.route('/judges', methods=['get'])

def judges():
    conn = get_db_connection()
    if request.args.get('tournament_number') is None:
        tournament_number = 1
    else:
        tournament_number = request.args.get('tournament_number')
    df_judges = get_tournament_judges(conn, tournament_number)
    df_tournaments = get_tournaments_j(conn)
    #print(request.query_string.decode())
    if request.args.get('state') == 'добавить':
        find_judge = True
    else:
        find_judge = False

    if request.values.get('сохранить'):
        if request.values.get('FIO') and request.values.get('degree') and request.values.get('checking_tables'):
            FIO = request.values.get('FIO')
            degree = request.values.get('degree')
            checking_tables = request.values.get('checking_tables')
            add_to_tournament_j(conn, FIO, degree, checking_tables, tournament_number)
        else:
            print('to do: add_list')

    if request.values.get('найти'):
        searcher=True
        if request.values.get('FIO'):
            FIO = request.values.get('FIO')
            new_judges = find_judges(conn, FIO)
        else:
            new_judges = pd.DataFrame()
    else:
        searcher=False
        new_judges = pd.DataFrame()


    if request.values.get('delete_judge'):
        delete_judge(conn, request.values.get('delete_judge'), tournament_number)

    if request.values.get('add_judge'):
        ID = request.values.get('add_judge')
        checking_tables = request.values.get('checking_tables')
        add_to_tournament_easy_j(conn, ID, tournament_number, checking_tables)


    # выводим форму
    html = render_template(
        'judges.html',
        tournament_judges = df_judges,
        tournaments = df_tournaments,
        tournament_number = tournament_number,
        find_judge = find_judge,
        new_judges = new_judges,
        searcher = searcher,
        len = len,
    )
    return html

