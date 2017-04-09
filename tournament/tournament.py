#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except Exception as e:
        print(e)


def connect_execute_close(sql):
    """Connect to the database, execute the SQL and then close the
    connection."""
    db, c = connect()
    c.execute(*sql)
    db.commit()
    db.close()


def connect_execute_close_fetch_results(sql):
    """Connect to the database, execute the SQL and then close the
    connection. Also passing out result for further use."""
    db, c = connect()
    c.execute(*sql)
    result = c.fetchall()
    db.close()
    return result


def deleteMatches():
    """Remove all the match records from the database."""
    connect_execute_close(("TRUNCATE matches CASCADE",))


def deletePlayers():
    """Remove all the player records from the database."""
    connect_execute_close(("TRUNCATE players CASCADE",))


def countPlayers():
    """Returns the number of players currently registered."""
    return \
        connect_execute_close_fetch_results(("SELECT COUNT(*) FROM players",))[
            0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connect_execute_close(
            ("INSERT INTO players (id, name) VALUES (DEFAULT, %s)", (name,)))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sql = "SELECT * from player_standings;"

    result = connect_execute_close_fetch_results((sql,))
    return [(int(row[0]), str(row[1]), int(row[2]), int(row[3])) for row in
            result]


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connect_execute_close((
        "INSERT INTO matches (id, winner, loser) VALUES ("
        "DEFAULT, %s, %s)",
        (winner, loser)))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    total_players = countPlayers()
    pairs = []

    # Ensure there are players, then iterate through and grab neighbouring
    # players from the standings
    # This followings the swiss pairings

    if total_players > 0:
        for player_index in range(0, total_players, 2):
            player_one_id = standings[player_index][0]
            player_one_name = standings[player_index][1]

            player_two_id = standings[player_index + 1][0]
            player_two_name = standings[player_index + 1][1]

            pair = (
                player_one_id, player_one_name, player_two_id, player_two_name)
            pairs.append(pair)
    return pairs
