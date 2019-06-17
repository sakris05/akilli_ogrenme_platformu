import sys, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

import pandas as pd
import numpy as np

from reviews.models import Fake 


def save_user_from_row(user_row):
    fake = Fake()
    fake.actual_id = user_row[1]
    fake.fake_id = user_row[2]
    print(fake.actual_id, fake.fake_id)
    fake.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        users_df = pd.read_csv(sys.argv[1])
        print(users_df)

        users_df.apply(
            save_user_from_row,
            axis=1
        )

        print("There are {} users".format(Fake.objects.count()))
        
    else:
        print("Please, provide User file path")