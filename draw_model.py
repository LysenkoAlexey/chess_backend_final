import pandas as pd


def get_tournaments(conn):
    return pd.read_sql(
        '''
        select * from tournaments
        ''', conn)


def get_tournament_players(conn, check_tournamentID):
    return pd.read_sql(
        f'''
    select *
    from tournaments_players
    join players on players.playerID = tournaments_players.FK_playerID
    join tournaments on tournaments.tournamentID = tournaments_players.FK_tournamentID

    where FK_tournamentID = :check_tournamentID
    ''', conn, params={'check_tournamentID': check_tournamentID})


# cross_join
# набрать все комбинации
# убрать идентичные
#
def get_draw(conn, tournamentID):
    return pd.read_sql(
        f'''
        select
        tour as 'Тур',
        FK_tournamentID,
	    FK_playerID1 as 'Белые',
        FK_playerID2 as 'Черные',
        result as 'Результат'
        from draw
        where (FK_tournamentID = :tournamentID)
        order by tour, FK_playerID1;
        ''', conn, params={'tournamentID': tournamentID})


def create_all_tours(conn, tournamentID):
    cur = conn.cursor()

    cur.execute('''
                    insert into draw (tour, FK_tournamentID, FK_playerID1, FK_playerID2)
                    with to_add as 
                    (
                    select
                    0 as tour,
                    :tournamentID as FK_tournamentID ,
                    playerA.FK_playerID as FK_playerID1,
                    playerB.FK_playerID as FK_playerID2
                    from tournaments_players playerA, tournaments_players playerB
                    where ((playerA.FK_tournamentID = :tournamentID) and (playerB.FK_tournamentID = :tournamentID))
                    and (playerA.FK_playerID <> playerB.FK_playerID))
                    select tour, FK_tournamentID, FK_playerID1, FK_playerID2
                    from to_add
                ''', {'tournamentID': tournamentID})
    conn.commit()
    print('all_tours')
    return True


def create_tour(conn, tournamentID):
    draw_df = pd.read_sql(f"""SELECT * FROM draw WHERE FK_tournamentID={tournamentID}
                           ORDER BY random()""",
                          conn)
    #draw_df.tour=draw_df.tour.astype(int)
    last_tour = max(draw_df.tour)
    for idx in draw_df.index:
        if draw_df['tour'][idx] == 0:
            #возможно пара еще не встречалась
            p1 = draw_df['FK_playerID1'][idx]; p2 = draw_df['FK_playerID2'][idx]
            now_playing = draw_df[(draw_df.tour == last_tour+1)]
            # проверяем, что никто из пары еще не играет в новом туре
            if p1 in now_playing.FK_playerID1.values \
                    or p1 in now_playing.FK_playerID2.values \
                    or p2 in now_playing.FK_playerID1.values \
                    or p2 in now_playing.FK_playerID2.values:
                continue

            # проверяем что пара не встречалась в предыдущих турах с переменой цвета
            if draw_df[(draw_df.FK_playerID1 == p2) & (draw_df.FK_playerID2 == p1)].tour.iloc[0] == 0:
                # not played before
                draw_df['tour'][idx] = last_tour+1

    cur = conn.cursor()

    draw_df_other = pd.read_sql(f"""SELECT * FROM draw WHERE FK_tournamentID<>{tournamentID}
                               ORDER BY random()""",
                          conn)
    draw_df.to_sql('draw', conn, index=False, if_exists='replace')
    draw_df_other.to_sql('draw', conn, index=False, if_exists='append')

    return True


def full_create_tour(conn, tournamentID):
    if_empty = pd.read_sql(f"select count(*) from draw where FK_tournamentID = {tournamentID}", conn)
    print(if_empty.shape)
    if_empty_int = if_empty.iloc[0,0]
    print(if_empty_int)
    #if_empty_int = if_empty.getInt(0)
    if if_empty_int > 0:
        create_tour(conn, tournamentID)
    else:
        print("---creating all tours")
        create_all_tours(conn, tournamentID)
        #create_tour(conn, tournamentID)
    return True


def set_result(conn, tournamentID, player1ID, player2ID, result):
    result = float(result)
    cur = conn.cursor()
    cur.execute('''
                    update draw
                    set result = :result
                    where (FK_tournamentID = :tournamentID and FK_playerID1=:player1ID and FK_playerID2=:player2ID)
                ''', {'tournamentID': tournamentID, 'player1ID':player1ID, 'player2ID':player2ID, 'result':result})
    cur.execute('''
    update tournaments_players
    set points = points + :result
    where (FK_tournamentID = :tournamentID and FK_playerID = :player1ID)
    ''', {'tournamentID': tournamentID, 'player1ID':player1ID, 'result':result})
    if (result == 0):
        result = 1
    cur.execute('''
    update tournaments_players
    set points = points + :result
    where (FK_tournamentID = :tournamentID and FK_playerID = :player2ID)
    ''', {'tournamentID': tournamentID, 'player2ID':player2ID, 'result':result})
    conn.commit()
    return True
