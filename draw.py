import pandas as pd
import math

from app import app

from flask import render_template, request, session
#import sqlite3
from utils import get_db_connection
from models.draw_model import *
@app.route('/draw', methods=['get'])


def draw():
    conn = get_db_connection()
    if request.args.get('tournament_number') == None:
        tournament_number = 1
    else:
        tournament_number = request.args.get('tournament_number')
    df_tournaments = get_tournaments(conn)
    df_draw = get_draw(conn, tournament_number)

    if request.args.get('state'):
        full_create_tour(conn, tournament_number)

    if request.args.get('res') != None:
        print(request.args.get('player1'))
        print(request.args.get('player2'))
        print(request.args.get('res'))
        set_result(conn, tournament_number, player1ID=request.args.get('player1'),
                   player2ID=request.args.get('player2'), result=request.args.get('res'))


    # выводим форму
    html = render_template(
        'draw.html',
        tournaments=df_tournaments,
        tournament_number=tournament_number,
        df_draw=df_draw,
        len=len,
        isnan=math.isnan
    )
    return html

