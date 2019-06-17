from keras.models import model_from_json
import tensorflow as tf
import keras
from .models import Review, Wine, Fake
from django.contrib.auth.models import User
import pandas as pd
from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
from keras.layers import Embedding, Reshape, Merge, Dropout, Dense, Flatten, merge, Input
from keras.models import Sequential, Model
from keras.constraints import non_neg
from keras.regularizers import l1, l2
import numpy as np

MODEL_WEIGHTS_FILE = "./model.h5"
mf_dim = 8
layers = [64,32,16,8]
reg_mf = 0
reg_layers = [0,0,0,0]
callbacks = [EarlyStopping('val_loss', patience=2), 
             ModelCheckpoint(MODEL_WEIGHTS_FILE, save_best_only=True)]

def get_model(n_users, m_items, k_factors, p_dropout=0.2, **kwargs):
         # Creating the model
        n_latent_factors_user = 8
        n_latent_factors_movie = 10
        n_latent_factors_mf = 8

        print(n_users, m_items)

        movie_input = keras.layers.Input(shape=[1],name='Item')
        movie_embedding_mlp = keras.layers.Embedding(m_items, 
        	n_latent_factors_movie, 
        	name='Movie-Embedding-MLP'
        	)(movie_input)

        movie_vec_mlp = keras.layers.Flatten(name='FlattenMovies-MLP')(movie_embedding_mlp)
        movie_vec_mlp = keras.layers.Dropout(p_dropout)(movie_vec_mlp)

        movie_embedding_mf = keras.layers.Embedding(m_items, 
        	n_latent_factors_mf, 
        	name='Movie-Embedding-MF')(movie_input)

        movie_vec_mf = keras.layers.Flatten(name='FlattenMovies-MF')(movie_embedding_mf)
        movie_vec_mf = keras.layers.Dropout(p_dropout)(movie_vec_mf)


        user_input = keras.layers.Input(shape=[1],name='User')
        user_embedding_mlp = keras.layers.Embedding(n_users, 
        	n_latent_factors_user, 
        	name='user-Embedding-MLP'
        	)(user_input)
        user_vec_mlp = keras.layers.Flatten(name='FlattenUsers-MLP')(user_embedding_mlp)

        user_vec_mlp = keras.layers.Dropout(p_dropout)(user_vec_mlp)

        user_vec_mf = keras.layers.Flatten(
        	name='FlattenUsers-MF'
        	)(keras.layers.Embedding(
        		n_users + 1, 
        		n_latent_factors_mf,
        		name='User-Embedding-MF')(user_input))

        user_vec_mf = keras.layers.Dropout(p_dropout)(user_vec_mf)


        concat = keras.layers.merge([movie_vec_mlp, user_vec_mlp], mode='concat',name='Concat')
        concat_dropout = keras.layers.Dropout(p_dropout)(concat)
        dense = keras.layers.Dense(200,name='FullyConnected')(concat_dropout)
        dense_batch = keras.layers.BatchNormalization(name='Batch')(dense)
        dropout_1 = keras.layers.Dropout(p_dropout,name='Dropout-1')(dense_batch)
        dense_2 = keras.layers.Dense(100,name='FullyConnected-1')(dropout_1)
        dense_batch_2 = keras.layers.BatchNormalization(name='Batch-2')(dense_2)


        dropout_2 = keras.layers.Dropout(p_dropout,name='Dropout-2')(dense_batch_2)
        dense_3 = keras.layers.Dense(50,name='FullyConnected-2')(dropout_2)
        dense_4 = keras.layers.Dense(20,name='FullyConnected-3', activation='relu')(dense_3)

        pred_mf = keras.layers.merge([movie_vec_mf, user_vec_mf], mode='dot',name='Dot')


        pred_mlp = keras.layers.Dense(1, activation='relu',name='Activation')(dense_4)

        combine_mlp_mf = keras.layers.merge([pred_mf, pred_mlp], mode='concat',name='Concat-MF-MLP')
        result_combine = keras.layers.Dense(100,name='Combine-MF-MLP')(combine_mlp_mf)
        deep_combine = keras.layers.Dense(50,name='FullyConnected-4')(result_combine)


        result = keras.layers.Dense(1,name='Prediction')(deep_combine)


        model = keras.Model([user_input, movie_input], result)
        return model

def load_model():
	#with tf.Session():
	#	json_file=open("./model.json","r")
	#	loaded_json=json_file.read()
	#	json_file.close()

	#	model=model_from_json(loaded_json)
	#	model.load_weights(MODEL_WEIGHTS_FILE)
	#	return model
	k_factors = 20
	n_users = max(list(Fake.objects.values_list('fake_id', flat=True)))
	m_items = max(list(Wine.objects.values_list('id', flat=True)))

	print(n_users, '-----------', m_items)

	model = get_model(n_users + 1, m_items + 1, k_factors)

	return model


def update_model(user_id_, noReview = False):

    print('Updating Model')
    #all_movie_ids = list(map(lambda x: x.wine.id, Review.objects.only("wine")))
    #all_user_ids = list(map(lambda x: x.id, Review.objects.only('id')))

    train_set = pd.DataFrame(list(Review.objects.values_list('user_id', 'wine__id', 'rating')),
    						 columns=['userid', 'movieid', 'rating'])

    temps = Review.objects.filter(user_id__gte=944)

    temps = set(temps.values_list('user_id', flat=True))

    for i in temps:
        train_set.loc[train_set['userid'] == i] = Fake.objects.get(actual_id=i).fake_id


    model = load_model()
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=["accuracy"])

    # print(train_set.userid.values.max(), '--------------')

    if noReview:
        user_id_ = Fake.objects.get(actual_id=user_id_).fake_id
        index = np.random.choice(train_set.movieid.values.max(), 1)[0]
        print(index, '--------------', user_id_)
        temp = pd.DataFrame({'userid': [user_id_], 'movieid': [index], 'rating': [0]})
        #temp = pd.DataFrame([user_id, index, 0])
        train_set = train_set.append(temp)
        #train_set.loc[-1] = [user_id_, index, 0]

    with tf.Session():

    	history = model.fit(
    			[train_set.userid, train_set.movieid], 
    			train_set.rating,
    			epochs=1,
    	        verbose=1,
    	        validation_split=0.10, 
    	        shuffle=True, 
    	        callbacks=callbacks
    	    )

    	return
