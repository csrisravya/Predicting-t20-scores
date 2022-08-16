import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings( 'ignore')

# Importing data
# dataset link : https://www.kaggle.com/datasets/ramjidoolla/ipl-data-set

match_df = pd.read_csv(r'C:\!1 desktop\akka chelli\akka\reva\Python\IPL\matches.csv')
match_df.sample(3)
match_df.info() # gives you all the columns adn non noull values in them
# match_df.shape() # gives you the no of rows and columns
dlvr_df = pd.read_csv(r'C:\!1 desktop\akka chelli\akka\reva\Python\IPL\deliveries.csv');
dlvr_df.head()
dlvr_df.info()

# Calculating total score in every match

inn_score = dlvr_df.groupby(['id','inning']).sum()['total_runs'] # we sum the scores of eavery match and each inning adn only display the total_runs column
# keeping only the 1st innings score of the 2 innings score
inn_score = inn_score[inn_score['inning'] == 1] #display all where inning has value 1 only

# MERGE inn_score with match_df

match_df = match_df.merge(inn_score['match_id','total_runs'],left_on="id",right_on = 'match_id')

# Cleaning  the data
match_df['team1'].unique()
match_df['team1'] = match_df['team1'].str.replace('Deccan Charges','Sunrisers Hyderabad')

#using isin method to retain rows that are in the lis above  
match_df = match_df[match_df['team1'].isin(teams)]

match_df['dl_applied'].unique()
