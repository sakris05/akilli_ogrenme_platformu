import webbrowser, os, re
import tmdbsimple as tmdb
from bs4 import BeautifulSoup
import requests
import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

from reviews.models import Wine 

tmdb.API_KEY = '2824ef0048b9cf1ffbba8902600c5d2d'

def fetch():
	#content = []
	wine_list = Wine.objects.order_by('-name')
	for movie in wine_list:
		if movie.poster_path == 'unspecified':
			search = tmdb.Search()
			name = (movie.name).split('(')[0]
			response = search.movie(query=name)
			temp_path = 'https://image.tmdb.org/t/p/w500{}'
			if search.results:
				temp_path = temp_path.format(search.results[0]['poster_path'])
				movie.poster_path = temp_path
			else:
				movie.poster_path = 'Not Found'
			movie.save(update_fields=["poster_path"]) 
			print(movie.poster_path, '-------', movie.name)
		#content.append(temp_path)
	#wine_list['image'] = content
	#return wine_list

fetch()