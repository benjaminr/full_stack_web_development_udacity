-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;

-- Main tables for players and their matches
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    winner INTEGER REFERENCES players (id),
    loser INTEGER REFERENCES players (id)
);

-- Custom view for a players total wins
CREATE VIEW total_wins
    AS SELECT players.id, count(matches.winner) AS wins
    FROM players left join matches
    ON players.id = matches.winner
    GROUP BY players.id;

-- Custom view for players total matches
CREATE VIEW total_matches
    AS SELECT players.id, count(all_matches) AS total_matches
    FROM players left join
        (SELECT winner AS all_matches FROM matches UNION ALL SELECT loser FROM matches) AS all_matches
    ON players.id = all_matches
    GROUP BY players.id;

-- Combine custom views to display both wins and matches - for standings
CREATE VIEW matches_and_wins
    AS SELECT total_matches.id, total_wins.wins, total_matches.total_matches AS matches
    FROM total_matches, total_wins
    WHERE total_matches.id = total_wins.id;
