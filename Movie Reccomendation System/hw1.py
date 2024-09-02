# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO CANVAS

from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    
    # creating movie ratings dictionary
    movie_ratings_dict = {}
    # reading file
    for line in open(f):
        # reading movie, rate, rater
        movie, rate, rater = line.split('|')
        # rating = rate
        rating = float(rate)
        # rater = user ID
        user = int(rater)
        if movie in movie_ratings_dict:
            # if movie exists in movie ratings dictionary
            movie_ratings_dict[movie].append(rating)
        else:
            # adding movie to movie ratings dictionary
            movie_ratings_dict[movie] = [rating]
    # returning movie ratings dictionary
    return movie_ratings_dict
    

# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre

    # creating movie genre dictionary
    movie_genres_dict = {}
    # reading file
    for line in open(f):
        # obtaining genre, movieid, movie name
        genre, movieid, name = line.strip().split('|')
        # movie name
        name = str(name)
        # genre
        genre = str(genre)
        # movie id
        movie_id = int(movieid)
        # assigning movie to genre in movie genre dictionary
        movie_genres_dict[name] = genre
    # returning movie genre dictionary
    return movie_genres_dict

# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    
    # creating genre dictionary
    genre_dict = {}
    # obtaining names and genre from dictionary d
    for name, genre in d.items():
        # if the genere is already in genre dictionary
        if genre in genre_dict:
            genre_dict[genre].append(name)
        else:
            # add genre to genre dictionary
            genre_dict[genre] = [name]
    return genre_dict
    
# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    
    # average dictionary to be returned
    average_dict = {}
    # obtaining movie and rating from dictionary d
    for movie, rating in d.items():
        # calculate total sum of all ratings
        asum = float(sum(rating))
        # calculate number of ratings
        aitems = float(len(rating))
        # calculate average
        average = float(asum/aitems)
        # assign average to movie in average dictionary
        average_dict[movie] = average
    # return average dictionary
    return average_dict
    
# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating, 
    #         in ranked order from highest to lowest average rating
    
    # convert d into a list
    dlist = list(d.items())
    # sort the list using sorted() function from highest to lowest rating
    dlist = sorted(dlist, key=lambda rating:rating[1], reverse = True)
    # slice list for first n items
    dlistsorted = dlist[:n]
    # creating dictionary of top n items
    sorted_averages = dict(dlistsorted)
    
    # return dictionary
    return sorted_averages
    
# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    
    # creating dictionary to be returned
    dictionary = {}
    # going through dictionary d
    for movie, avg_rate in d.items():
        # calling movies names
        name = str(movie)
        # calling average ratings rate
        rate = float(avg_rate)
        # adding movie to new dictionary if it is >= to threshold given
        if (rate >= thres_rating):
            dictionary[name] = rate
    # return dictionary
    return dictionary
    
# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    
    # casting genre as a string as a safety measure
    genre = str(genre)
    # create returnlist
    returnlist = []
    # search 2.1 dictionary for key (genre) and obtain values (movies)
    if genre in genre_to_movies:
        movies = genre_to_movies.get(genre)
    else:
        return None
    # creating counter
    c = Counter()
    # search 2.2 dictionary for movies key and obtain values (avgrating)
    for movie in movies:
        if movie in movie_to_average_rating:
            # add movie+avgrating to counter dictionary
            c[movie] = movie_to_average_rating[movie]
        else:
            c[movie] = None
    # sort returnlist
    returnlist = c.most_common(n)
    # convert returnlist to returndict
    returndict = dict(returnlist)
    # return returndict
    return returndict
    
# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    
    # total of all averages
    avgsum = float(0.0)
    # total number of movies
    avglen = float(0.0)
    # search 2.1 dictionary for key (genre) and obtain values (movies)
    if genre in genre_to_movies:
        movies = genre_to_movies.get(genre)
    
    # search 2.2 dictionary for movies key and obtain values (avgrating)
    for movie in movies:
        if movie in movie_to_average_rating:
            # get avgrating
            avgrating = float(movie_to_average_rating[movie])
            # add avgrating to float avgsum
            avgsum = avgsum + avgrating
            # add 1 to float var len
            avglen = avglen + 1

    # calculate average genre rating (a float called agr)
    agr = float(avgsum/avglen)
    return agr
    
# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    
    # counter bc we want to know top n genres
    c = Counter()
    # go through genres
    for genre in genre_to_movies:
        # setting avgsum and avglen to 0 for every genre calculation
        avgsum = float(0.0)
        avglen = float(0.0)
        # go through movies in genre
        for movie in genre_to_movies.get(genre):
            # obtaining average rating of movie in genre
            avgrating = float(movie_to_average_rating[movie])
            # sum of all movie rating averages in genre
            avgsum = avgsum + avgrating
            # total number of movies in genre
            avglen = avglen + 1
        # calculate average genre rating of all movies in a certain genre
        agr = float(avgsum/avglen)
        # store genre and it's average in c
        c[genre] = agr
    
    # store top n genres which are in c in a list
    returnlist = c.most_common(n)
    # convert list to dictionary
    returndict = dict(returnlist)
    # return dictionary
    return returndict

# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    
    # creating user ratings dictionary
    user_ratings = {}
    # reading file
    for line in open(f):
        # reading movie, rating, userid
        movie, rating, userid = line.strip().split('|')
        # store rating as float
        rating = float(rating)
        # store userid as int
        userid = int(userid)
        # storing value as (m, r)
        value = (movie, rating)
        # storing userid into dictionary
        if userid in user_ratings:
            # if userid exists in user_ratings dictionary
            user_ratings[userid].append(value)
        else:
            # adding userid to user_ratings dictionary
            user_ratings[userid] = [value]
    # return dictionary
    return user_ratings
    
# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    
    # 1.2 = movie_to_genre
    # 4.1 = user_to_movies
    # replace movie in value (m,r) in 4.1 with genre value assigned to movie key in 1.2
    # if the user_id is in the 4.1 dictionary provided
    if user_id in user_to_movies:
        # list storing (g,r)
        grlst = []
        # for (m,r) assigned to a user
        for movie, rating in user_to_movies[user_id]:
            # if movie is in the 1.2 dictionary
            if movie in movie_to_genre:
                # get the movie's genre
                genre = movie_to_genre[movie]
                # add the genre to the list along with rating
                grlst.append((genre, rating))
    # Iterate through (g,r) in g and get (g, avg r)
        # creating two dictionaries, 1 for totals and 1 for # of items
        gtotals = Counter()
        gcounts = Counter()
        for genre, rating in grlst:
            # adding to totals
            gtotals[genre] += rating
            # adding to counts
            gcounts[genre] += 1
    else:
        return ('Error: userID inputted does not exist in the file')
    # gar will be the counterdictionary with (g, avg r) for given user
    gar = Counter()
    for genre in gcounts:
        avg = gtotals[genre]/gcounts[genre]
        gar[genre] = avg
    
    # creating topgenre str to be returned
    topgenre = str('')
    # sort through gar using most_common 
    for genre, rating in gar.most_common(1):
        # assigning top genre to topgenre str
        topgenre = str(genre)
    # return topgenre str
    return topgenre
    
# 4.3    
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    
    top_genre = get_user_genre(user_id=user_id, user_to_movies= user_to_movies, movie_to_genre= movie_to_genre)
    if top_genre == str('Error: userID inputted does not exist in the file'):
        return ('Error: userID inputted does not exist in the file')
    # get movies not rated by user
    lst_unrated = []
    for movie, genre in movie_to_genre.items():
        if (genre == top_genre):
            if movie not in [m for m, x in user_to_movies.get(user_id, [])]:
                lst_unrated.append(movie)
    # get average rating for each of the movies in lst_unrated and store in country dictionary as movie = key, avg = value
    mtoac = Counter()
    for movie in lst_unrated:
        mtoac[movie] = movie_to_average_rating.get(movie)
    # sorting counter dictionary for most common
    returnlst = mtoac.most_common(3)
    returndict = dict(returnlst)
    return returndict

# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading
    
    # region 1.1 Reading Data
    print("1.1:")
    movie_ratings_dict = read_ratings_data("movieRatingTest3.txt")
    print(f"movie_ratings_dict = {movie_ratings_dict}")
    print("\n")
    # endregion
    # region 1.2 Reading Data
    print("1.2:")
    movie_genres_dict = read_movie_genre("genreMovieTest3.txt")
    print(movie_genres_dict)
    print("\n")
    # endregion
    # region 2.1 Processing Data - Genre Dictionary
    print("2.1:")
    genre_to_movies = create_genre_dict(movie_genres_dict)
    print(genre_to_movies)
    print("\n")
    # endregion
    # region 2.2 Processing Data - Average Rating
    print("2.2:")
    average_dictionary = calculate_average_rating(movie_ratings_dict)
    print(average_dictionary)
    print("\n")
    # endregion
    # region 3.1 Recomendation - Popularity Based
    print("3.1:")
    sortedratingsdict = get_popular_movies(average_dictionary)
    print(sortedratingsdict)
    print("top 3")
    top3 = get_popular_movies(average_dictionary, n=3)
    print(top3)
    print("\n")
    # endregion
    # region 3.2 Recommendation - Threshold Rating
    print("3.2:")
    print(filter_movies(average_dictionary, thres_rating=3))
    print(filter_movies(average_dictionary, thres_rating=3.5))
    print("\n")
    # endregion
    # region 3.3 Recommendation - Popularity + Genre Based
    print("3.3 (Testing for the Action genre):")
    print(get_popular_in_genre(genre='Action', genre_to_movies=genre_to_movies, movie_to_average_rating=average_dictionary, n=3))
    print("\n")
    # endregion
    # region 3.4 Recommendation - Genre Rating
    print("3.4 (Testing for the Action genre):")
    agr = float(get_genre_rating(genre='Action', genre_to_movies=genre_to_movies, movie_to_average_rating=average_dictionary))
    print(f'The average rating of the movies in the Action genre is {agr}.')
    print("\n")
    # endregion
    # region 3.5 Recommendation - Genre Popularity
    print("3.5")
    print(genre_popularity(genre_to_movies=genre_to_movies, movie_to_average_rating=average_dictionary,n=5))
    print(genre_popularity(genre_to_movies=genre_to_movies, movie_to_average_rating=average_dictionary,n=2))
    print("\n")
    # endregion
    # region 4.1 User Focused
    print("4.1:")
    user_ratings_dict = read_user_ratings("movieRatingTest3.txt")
    print(f'user_ratings_dict = {user_ratings_dict}')
    print("\n")
    # endregion
    # region 4.2 User Focused
    print("4.2 (Testing for User 6):")
    print(get_user_genre(user_id=6, user_to_movies=user_ratings_dict, movie_to_genre=movie_genres_dict))
    print("\n")
    # endregion
    # region 4.3 User Focused
    print("4.3 (Testing for User 6):")
    print(recommend_movies(user_id=6, user_to_movies=user_ratings_dict, movie_to_genre=movie_genres_dict, movie_to_average_rating=average_dictionary))
    print("\n")
    # endregion
# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions
    
# program will start at the following main() function call
# when you execute hw1.py
main()

    
