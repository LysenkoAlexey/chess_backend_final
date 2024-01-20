import sqlite3
import pandas as pd

def get_db_connection():
    return sqlite3.connect('chessbd.sqlite')

#conn = sqlite3.connect('chessbd.sqlite')
#conn.execute("""update draw set tour = 0;""")
#conn.commit()


#df = pd.read_sql("""select * from players""",conn)
#cur = conn.cursor()
#cur.execute('''
#delete from tournaments
#where tournamentID = 4
#''')

#conn.commit()
#print(df)

'''
insert into tournaments_players (FK_tournamentID, FK_playerID, points)
            values (2, 1, 0)
            
            
insert into judges (judge_name, degree)
            values ("Судьянов И.И.", 1)
'''

'''insert into players (player_name, birthdate, rating)
            values ('Иванов И.И.', '2000-01-10', 2000), ('Федоров А.М.', '2002-10-10', 1800)'''

'''create table systems (
	systemID integer primary key autoincrement,  
	system_name text
);

create table tournaments (
	tournamentID integer primary key autoincrement,
    tournament_name text,
    tournament_tables integer,
    start_date date,
    end_date date,
    control text,
    tournament_description text,
    FK_systemID integer
    foreign key (FK_systemID) references systems (systemID)
    on update cascade
	on delete cascade
);


create table players (
	playerID integer primary key autoincrement,
    player_name text,
    birthdate date,
    rating integer
);

create table judges (
	judgeID integer primary key autoincrement,
    judge_name text,
    degree text
);

create table tournaments_judges (
	FK_judgeID integer,
	FK_tournamentID integer,
    checking_tables text,
	foreign key (FK_judgeID) references judges (judgeID)
	on update cascade
	on delete cascade,
	foreign key (FK_tournamentID) references tournaments (tournamentID)
	on update cascade
	on delete cascade,
	primary key (FK_judgeID, FK_tournamentID)
);

create table tournaments_players (
	FK_playerID integer,
	FK_tournamentID integer,
    points float,
	foreign key (FK_playerID) references players (playerID)
	on update cascade
	on delete cascade,
	foreign key (FK_tournamentID) references tournaments (tournamentID)
	on update cascade
	on delete cascade,
	primary key (FK_playerID, FK_tournamentID)
);

create table draw (
	tour integer,
	FK_tournamentID integer,
	FK_playerID1 integer,
    FK_playerID2 integer,
    result float,
    foreign key (FK_playerID1) references players (playerID)
	on update cascade
	on delete cascade,
	foreign key (FK_playerID2) references players (playerID)
	on update cascade
	on delete cascade,
	foreign key (FK_tournamentID) references tournaments (tournamentID)
	on update cascade
	on delete cascade,
	primary key (FK_playerID1, FK_playerID2, FK_tournamentID)
);

'''