# О турнире, добавить турнир
import pandas as pd


def get_tournaments(conn):
    return pd.read_sql(
        '''
        select * from tournaments
        ''', conn)


def get_cur_tournament(conn, tournamentID):
    return pd.read_sql(
        '''
        select * from tournaments
        where tournamentID = :tournamentID
        ''', conn, params={'tournamentID':tournamentID})


def set_tournament(conn, tournament_number, name, start, end, control, tables, systemID, description):
    cur = conn.cursor()

    cur.execute('''
            UPDATE tournaments
            SET 
            tournament_name = :name,
            start_date = :start,
            end_date = :end,
            control = :control,
            tournament_tables = :tables,
            tournament_description = :description
            WHERE tournamentID = :tournament_number
                ''', {'tournament_number': tournament_number, 'name':name, 'start':start,'end':end, 'control':control,
    'tables':tables,'systemID':systemID,'description':description})
    conn.commit()
    return True


def add_tournament(conn, name, start, end, control, tables, systemID, description):
    cur = conn.cursor()

    cur.execute('''
            insert into tournaments (tournament_name, start_date, end_date, control, tournament_tables, FK_systemID, tournament_description)
            values (:name, :start, :end, :control, :tables, :systemID, :description)
                ''', {'name':name, 'start':start,'end':end, 'control':control,
    'tables':tables,'systemID':systemID,'description':description})
    conn.commit()
    return True