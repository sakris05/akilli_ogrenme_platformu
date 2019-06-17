import json, urllib
import tmdbsimple as tmdb

tmdb.API_KEY = '2824ef0048b9cf1ffbba8902600c5d2d'

def fetch(movie):
	search = tmdb.Search()
	name = (movie.name).split('(')[0]
	response = search.movie(query=name)
	movieid = (search.results[0])['id']
	url_full_movie_details = 'https://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=videos'.format(movieid, tmdb.API_KEY)
	response = urllib.request.urlopen(url_full_movie_details)
	data = json.loads(response.read())
	key = data['videos']['results']
	#print(key)
	if key:
		YouTube_URL = "https://www.youtube.com/watch?v={}".format(key[0]['key'])
	else:
		YouTube_URL = 'Not Found'
	return {'YouTube_URL': YouTube_URL, 'overview': data['overview']}