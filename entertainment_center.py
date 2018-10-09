import fresh_tomatoes
import media
import requests
import json


# Configure this if you are behind a proxy
proxies = dict(http='socks5://127.0.0.1:1080')
# Inset your https://themoviedb.org ID
api_key = ''
youtube = 'https://www.youtube.com/watch?v='


def create_movie(movie_name):
    movie_name = movie_name.replace(' ', '%20')
    # Request the API for the list of movies
    request_list_movies = requests.get('http://api.themoviedb.org/3/search/movie?api_key=' +  # noqa
                                       api_key + '&language=en-US&query=' +
                                       movie_name + '&include_adult=false',
                                       proxies=proxies)
    movie_name = movie_name.replace('%20', ' ')
    movies = json.loads(request_list_movies.text)
    # Get the ID of the first match for future requests
    movie_id = str(movies['results'][0]['id'])
    movie_overview = movies['results'][0]['overview'].encode("utf-8")
    poster = movies['results'][0]['poster_path'].encode("utf-8")
    # Request the API for directory configuration parameters
    request_config = requests.get('http://api.themoviedb.org/3/configuration?api_key=' +  # noqa
                                    api_key, proxies=proxies)
    config = json.loads(request_config.text)
    poster = config['images']['base_url'].encode("utf-8") + \
        config['images']['poster_sizes'][3].encode("utf-8") + poster
    # Request the API for trailers of movies
    request_trailer = requests.get('http://api.themoviedb.org/3/movie/' +
                                   movie_id + '/videos?api_key=' +
                                   api_key + '&language=en-US',
                                   proxies=proxies)
    # trailer = json.loads(request_trailer.text)
    trailer = json.loads(request_trailer.text)
    trailer = youtube + trailer['results'][0]['key']
    return media.Movie(movie_name, movie_overview, poster, trailer)


the_matrix = create_movie("The Matrix")
toy_story = create_movie("Toy Story")
the_godfather = create_movie("The Godfather")
top_gun = create_movie("Top Gun")
back_to_the_future = create_movie("Back to the Future")
lord_of_the_rings = create_movie("Lord of the Rings")
alien = create_movie("Alien")
rocky_iv = create_movie("Rocky IV")
predator = create_movie("Predator")
movies = [the_matrix, toy_story, the_godfather,
          top_gun, back_to_the_future,
          lord_of_the_rings, alien, rocky_iv, predator]
fresh_tomatoes.open_movies_page(movies)
