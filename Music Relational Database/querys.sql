Question 1: 
SELECT Genre.genre_name AS genre, COUNT(*) AS number_of_songs
FROM Genre
JOIN Song_To_Genre ON Genre.genre_ID = Song_To_Genre.genre_ID
GROUP BY Genre.genre_name
ORDER BY number_of_songs DESC
LIMIT 3;

Question 2:
SELECT DISTINCT Artist.artist_name
FROM Artist
JOIN Song ON Artist.artist_ID = Song.artist_ID
WHERE Song.album_ID IS NOT NULL AND Song.is_Single = TRUE
AND Artist.artist_name IN (
    SELECT Artist.artist_name
    FROM Artist
    JOIN Song ON Artist.artist_ID = Song.artist_ID
    WHERE Song.album_ID IS NULL OR Song.is_Single = FALSE
);

Question 3:
SELECT Album.album_name, AVG(Rating.rating) AS average_user_rating
FROM Album
JOIN Rating ON Album.album_ID = Rating.album_ID
WHERE YEAR(Rating.rating_date_and_time) BETWEEN 1990 AND 1999
GROUP BY Album.album_name
ORDER BY average_user_rating DESC, Album.album_name ASC
LIMIT 10;



Question 4:
SELECT Genre.genre_name, COUNT(Rating.rating_ID) AS number_of_song_ratings
FROM Genre
JOIN Song_To_Genre ON Genre.genre_ID = Song_To_Genre.genre_ID
JOIN Song ON Song_To_Genre.song_ID = Song.song_ID
JOIN Rating ON Song.song_ID = Rating.song_ID
WHERE YEAR(Rating.rating_date_and_time) BETWEEN 1991 AND 1995
GROUP BY Genre.genre_name
ORDER BY number_of_song_ratings DESC
LIMIT 3;


Question 5:
SELECT DISTINCT U.username, P.playlist_name AS playlist_title, AVG(SR.avg_rating) AS average_song_rating
FROM User U
JOIN Playlist P ON U.user_ID = P.user_ID
JOIN (
    SELECT SIP.playlist_ID, AVG(R.rating) AS avg_rating
    FROM Songs_In_Playlist SIP
    JOIN Rating R ON SIP.song_ID = R.song_ID
    GROUP BY SIP.playlist_ID, R.song_ID
) AS SR ON P.playlist_ID = SR.playlist_ID
GROUP BY U.username, P.playlist_name
HAVING average_song_rating >= 4.0;

Question 6:
SELECT u.username, COUNT(*) AS number_of_ratings
FROM users u
JOIN ratings r ON u.user_id = r.user_id
GROUP BY u.username
ORDER BY number_of_ratings DESC
LIMIT 5;

Question 7:
SELECT artist_name, COUNT(*) AS number_of_songs
FROM songs
WHERE YEAR(song_release_date) BETWEEN 1990 AND 2010
GROUP BY artist_name
ORDER BY number_of_songs DESC
LIMIT 10;

Question 8:
SELECT song_title, COUNT(*) AS number_of_playlists
FROM playlist_songs
JOIN songs ON playlist_songs.song_id = songs.song_id
GROUP BY song_title
ORDER BY number_of_playlists DESC, song_title ASC
LIMIT 10;

Question 9:
SELECT s.song_title, s.artist_name, COUNT(*) AS number_of_ratings
FROM songs s
JOIN ratings r ON s.song_id = r.song_id
WHERE s.album_name IS NULL
GROUP BY s.song_title, s.artist_name
ORDER BY number_of_ratings DESC
LIMIT 20;

Question 10:
SELECT DISTINCT artist_name
FROM songs
WHERE artist_name NOT IN (
    SELECT artist_name
    FROM songs
    WHERE YEAR(song_release_date) > 1993
);


