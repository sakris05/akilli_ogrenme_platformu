import sys, os 
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

from reviews.models import Review, Wine 

def save_review_from_row(review_row):
    review = Review()

    # id, username, wine_id, rating, published_date, comment

    review.id = int(review_row[0]) + 1

    review.user_name = review_row[5]

    review.wine = Wine.objects.get(id=review_row[2])

    review.rating = review_row[3]

    review.pub_date = datetime.datetime.now()

    review.comment = datetime.datetime.fromtimestamp(
        int(review_row[4])
    ).strftime('%Y-%m-%d %H:%M:%S')

    print(review.id, 
        review.user_name,
        review.wine,
        review.rating,
        review.pub_date,
        review.comment)

    review.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        reviews_df = pd.read_csv(sys.argv[1])
        print(reviews_df)

        #reviews_df.apply(
        #    save_review_from_row,
        #    axis=1
        #)
        
        objs = [
                Review(
                    id=index,
                    user_name=e.username,
                    user_id = e.UserID,
                    wine=Wine.objects.get(id=e.MovieID),
                    rating=e.Rating,
                    pub_date=datetime.datetime.now(),
                    comment=e.Timestamp
                )
                for index, e in reviews_df.iterrows()
                ]

        msg = Review.objects.bulk_create(objs)

        print("There are {} reviews in DB".format(Review.objects.count()))
        
    else:
        print("Please, provide Reviews file path")
