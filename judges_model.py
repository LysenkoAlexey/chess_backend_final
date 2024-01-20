# турниры, участники
# новый участник
import pandas as pd


def get_judge(conn):
    return pd.read_sql(
        '''
    SELECT * FROM judges
    ''', conn)


def get_tournaments_j(conn):
    return pd.read_sql(
        '''
        select * from tournaments
        ''', conn)


def get_tournament_judges(conn, check_tournamentID):
    return pd.read_sql(
        f'''
    select 
    FK_judgeID,
    judge_name as 'ФИО',
    degree as 'Степень',
    checking_tables as 'Проверяемые столы'
    from tournaments_judges
    join judges on judges.judgeID = tournaments_judges.FK_judgeID
    join tournaments on tournaments.tournamentID = tournaments_judges.FK_tournamentID

    where FK_tournamentID = :check_tournamentID
    ''', conn, params={'check_tournamentID': check_tournamentID})


def add_to_tournament_j(conn, FIO, degree, checking_tables, tournament_number):
    cur = conn.cursor()

    cur.execute('''
                insert into tournaments_judges (FK_tournamentID, FK_judgeID, checking_tables)
                with
                to_add_judge as
                (
                select 
                :tournament_number as tourn,
                judgeID as FK_playerID,
                :checking_tables as checking_tables
                from judges
                where judge_name = :FIO and degree = :degree
                )
                select tourn, FK_playerID, points
                from to_add_player
            ''', {'FIO': FIO, 'degree': degree, 'checking_tables':checking_tables, 'tournament_number': tournament_number})
    conn.commit()
    return True


def add_to_tournament_easy_j(conn, ID, tournament_number, checking_tables):
    cur = conn.cursor()

    cur.execute('''
                insert into tournaments_judges (FK_tournamentID, FK_judgeID, checking_tables)
                values(:tournament_number, :ID, :checking_tables)
            ''', {'ID': ID, 'tournament_number': tournament_number, 'checking_tables': checking_tables})
    conn.commit()
    return True


def delete_judge(conn, judgeID, tournament_number):
    cur = conn.cursor()

    cur.execute('''
                    delete from tournaments_judges
                    where FK_judgeID = :judgeID and FK_tournamentID = :tournament_number
                ''', {'judgeID': judgeID, 'tournament_number': tournament_number})
    conn.commit()
    return True


def find_judges(conn, FIO):
    return pd.read_sql(
        f'''
    select *
    from judges
    where judge_name = :FIO
    ''', conn, params={'FIO': FIO})
