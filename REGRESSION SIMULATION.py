from datetime import datetime
import numpy as np
import pandas as pd
from statsmodels.api import OLS

file_1 = 'regression.csv'
regression = pd.read_csv(file_1)
print(regression)

#print(movies1.columns)
# ['budget', 'genres', 'id', 'original_language', 'popularity',
#        'production_countries', 'release_date', 'revenue', 'runtime', 'status',
#        'title', 'vote_average', 'holiday', 'single_genre_Action',
#        'single_genre_Adventure', 'single_genre_Animation',
#        'single_genre_Comedy', 'single_genre_Crime', 'single_genre_Documentary',
#        'single_genre_Drama', 'single_genre_Family', 'single_genre_Fantasy',
#        'single_genre_Foreign', 'single_genre_History', 'single_genre_Horror',
#        'single_genre_Music', 'single_genre_Mystery', 'single_genre_Romance',
#        'single_genre_Science Fiction', 'single_genre_TV Movie',
#        'single_genre_Thriller', 'single_genre_War', 'single_genre_Western']

#Run regression analysis
dv = regression[]
iv = regression[[]]

movies1_regression = OLS(dv.astype(float), iv.astype(float)).fit()
#Print your regression result
print(movies1_regression.summary())
