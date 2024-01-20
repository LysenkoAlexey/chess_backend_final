import pandas as pd


def get_player(conn):
    return pd.read_sql(
        '''
    SELECT * FROM players
    ''', conn)


def get_tournaments(conn):
    return pd.read_sql(
        '''
        select * from tournaments
        ''', conn)


def get_tournament_players(conn, check_tournamentID):
    return pd.read_sql(
        f'''
    select 
    FK_playerID,
    player_name as 'ФИО',
    birthdate as 'Дата рождения',
    points as 'очки'
    from tournaments_players
    join players on players.playerID = tournaments_players.FK_playerID
    join tournaments on tournaments.tournamentID = tournaments_players.FK_tournamentID
    
    where FK_tournamentID = :check_tournamentID
    ''', conn, params={'check_tournamentID':check_tournamentID})


def add_to_tournament(conn, FIO, datebirth, tournament_number):
    cur = conn.cursor()

    cur.execute('''
                insert into tournaments_players (FK_tournamentID, FK_playerID, points)
                with
                to_add_player as
                (
                select 
                :tournament_number as tourn,
                playerID as FK_playerID,
                0.0 as points
                from players
                where player_name = :FIO and birthdate = :datebirth 
                )
                select tourn, FK_playerID, points
                from to_add_player
            ''', {'FIO': FIO, 'datebirth': datebirth, 'tournament_number':tournament_number})
    conn.commit()
    return True

def add_to_tournament_easy(conn, ID, tournament_number):
    cur = conn.cursor()

    cur.execute('''
                insert into tournaments_players (FK_tournamentID, FK_playerID, points)
                values(:tournament_number, :ID, 0)
            ''', {'ID': ID, 'tournament_number':tournament_number})
    conn.commit()
    return True


def delete_player(conn, playerID, tournament_number):
    cur = conn.cursor()

    cur.execute('''
                    delete from tournaments_players
                    where FK_playerID = :playerID and FK_tournamentID = :tournament_number
                ''', {'playerID': playerID, 'tournament_number':tournament_number})
    conn.commit()
    return True


def find_players(conn, FIO):
    return pd.read_sql(
        f'''
    select *
    from players
    where player_name = :FIO
    ''', conn, params={'FIO':FIO})
