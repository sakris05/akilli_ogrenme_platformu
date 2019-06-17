import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

from django.contrib.auth.models import User
from reviews.models import Wine, Review

#while User.objects.count():
#    ids = User.objects.values_list('id')[:500]
#    User.objects.filter(id__in = ids).delete()

#while Wine.objects.count():
#    ids = Wine.objects.values_list('id')[:500]
#    Wine.objects.filter(id__in = ids).delete()

#while Review.objects.count():
#    ids = Review.objects.values_list('id')[:600]
#    Review.objects.filter(id__in = ids).delete()