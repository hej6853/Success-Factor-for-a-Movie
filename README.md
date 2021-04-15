# Success-Factor-for-a-Movie

from datetime import datetime
import numpy as np
import pandas as pd
from statsmodels.api import OLS


# import two separate dataframes
file_1 = 'movies_metadata.csv'
metadata = pd.read_csv(file_1)
print(metadata)

file_2 = 'credits_revised.csv'
credits = pd.read_csv(file_2,encoding='latin-1')
#encoding ->

#print(metadata_rename.columns)
print(credits.columns)

credits = credits.astype(str)
print(credits.dtypes)

# Merge the three data frames appropriately.
metadata_credits_merge = pd.merge(metadata, credits, how='inner', on = 'id')
print(metadata_credits_merge.columns)

# Remove unnecessary columns 45538 rows ---> 45537
movies_remove_unnecessaries =metadata_credits_merge.drop(columns=['adult','belongs_to_collection','homepage','imdb_id','overview',
                                                  'poster_path','spoken_languages','tagline','video','vote_count','cast',
                                                  'original_title', 'production_companies', 'crew'])

print(movies_remove_unnecessaries)

#Find duplcate rows
movies_find_duplicated = movies_remove_unnecessaries[movies_remove_unnecessaries.duplicated()]
print(movies_find_duplicated)

#Drop duplicate rows (if any) : columns 45538 rows(merged) ---> 45537rows (removed unnecessary columns) --> 45462 rows
# (removed duplicated) 45509 -> 45014
movies_dropdups = movies_remove_unnecessaries.drop_duplicates()
print(movies_dropdups)

# Find missing values : original_languages: 11 , popularity:3, production_companies:3, production_countries:3,
#                       release_date:87, revenue:3, runtime:260, status:84, title:3, vote_average:3, vote_count:3
movies_dropdups_find_missing = movies_dropdups.isnull().sum()
print(movies_dropdups_find_missing)

# Deal with any missing values: columns 45538 rows(merged) ---> 45537rows (removed unnecessary columns) --> 45462 rows
# # (removed duplicated) --> 45042 rows (removed missing values)
# (missing values can be dropped as it's huge dataset)
movies_dropdups_dropmissing = movies_dropdups.dropna()
print(movies_dropdups_dropmissing)

# Remove unnecessary rows in each columns: columns 45538 rows(merged) ---> 45537rows (removed unnecessary columns) --> 45462 rows
# # # (removed duplicated) --> 45042 rows (removed missing values) --> 32131 rows (Removed en) --> 31890 rows (not released)
# ---> 30249 rows(removed genres' '[]')--> 23299(production_companies []) --> 22874 (production_countiries []) -->
# 22815(removed crew's [])
movies_dropen = movies_dropdups_dropmissing[movies_dropdups_dropmissing.original_language == 'en']
print(movies_dropen)

movies_dropen_not_released1 = movies_dropen[movies_dropen.status == 'Released']
print(movies_dropen_not_released1)

movies1= movies_dropen_not_released1[movies_dropen_not_released1.genres != '[]']
print(movies1)

movies1 = movies1[movies1.production_countries != '[]']
print(movies1)

#obtain genre
genre_column = []
for row in movies1['genres']:
    row = eval(row)
    if len(row) != 0:
        genre_column.append(row[0]['name'])
    else:
        genre_column.append(None)
movies1['single_genre'] = genre_column
print(movies1['single_genre'].nunique())
# unique: print only the unique values in the columns, nunique: number of unique values
# creates blank lists, adding value to it and turning into column


#obtain holiday dummy variable - Christmast season
date_column = []
for row in movies1['release_date']:
    if str(row) == 'nan' or len(str(row)) not in {8, 9, 10}:
        date_column.append(None)
    else:
        try:
            date_column.append(datetime.strptime(str(row), '%Y.%m.%d'))
        except:
            date_column.append(datetime.strptime(str(row), '%Y-%m-%d'))
movies1['release_date'] = date_column
movies1 = movies1.dropna()
movies1['holiday'] = pd.DatetimeIndex(movies1['release_date']).month
movies1['holiday'] = np.where(movies1['holiday'] == 12, 1, 0)
# not 8,9,10 then put null value


movies1 = movies1[movies1.revenue != 0]
print(movies1)

#Get 'single_genre' dummies
movies1= pd.get_dummies(movies1, columns=['single_genre'], prefix=['single_genre'])
print(movies1)
movies1.to_csv('regression.csv', index=False)

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
dv = movies1['revenue']
iv = movies1[['budget']]


movies1_regression = OLS(dv.astype(float), iv.astype(float)).fit()
#Print your regression result
print(movies1_regression.summary())

print(movies1['budget'].describe())

#print(movies1['budget'].astype(int).describe())
#pd.set_option('display.max_columns', None)
#print(movies1.describe())
#print(homework_data['comp_sent_score'].describe())
