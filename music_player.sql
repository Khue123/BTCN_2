CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    song_name VARCHAR(255) NOT NULL,
    play_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from songs