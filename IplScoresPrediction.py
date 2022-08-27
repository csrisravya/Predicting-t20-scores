# problem statement: win predictor that displays the probability of the chasing team winning an IPL match after every over.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings 
warnings.filterwarnings( 'ignore') 

# Importing data
# dataset obtained from : https://www.kaggle.com/datasets/ramjidoolla/ipl-data-set

match_df = pd.read_csv(r'C:\!1 desktop\akka chelli\akka\reva\Python\IPL\matches.csv')
match_df.info() 

dlvr_df = pd.read_csv(r'C:\Python\IPL\deliveries.csv')
dlvr_df.info()

# Calculating total score in every match

inn_score = dlvr_df.groupby(['match_id', 'inning']).sum()['total_runs'].reset_index() 
# keeping only the 1st innings score of the 2 innings score
inn_score = inn_score[inn_score['inning'] == 1] 

# MERGE inn_score with match_df

match_df = match_df.merge(inn_score[['match_id', 'total_runs']], left_on='id', right_on='match_id')

# Cleaning  the data
match_df['team1'].unique()
#removing duplicates 
match_df['team1'] = match_df['team1'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
match_df['team1'] = match_df['team1'].str.replace('Delhi Daredevils','Delhi Capitals')
match_df['team2'] = match_df['team2'].str.replace('Delhi Daredevils','Delhi Capitals')
match_df['team2'] = match_df['team2'].str.replace('Deccan Chargers','Sunrisers Hyderabad')


teams = list(match_df['team1'].unique())
teams2 = list(match_df['team2'].unique())
if(teams.sort()==teams2.sort()):
    teams.remove('Rising Pune Supergiant')
    teams.remove('Rising Pune Supergiants')
    teams.remove('Kochi Tuskers Kerala')# removing teams which are no longer playing.
    teams.remove('Gujarat Lions')
    teams.remove('Pune Warriors')
else:
    teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Mumbai Indians',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
    ]

match_df = match_df[match_df['team1'].isin(teams)]
match_df = match_df[match_df['team2'].isin(teams)]

#removing matches where D/L was applied
match_df['dl_applied'].value_counts() # returns count of unique vaues
match_df=match_df[match_df['dl_applied']==0]

#getting rid of unnecessary/redundant columns 
# only the match_id,winner and total_runs are required

match_df=match_df[['match_id','winner','total_runs']]

# Now examining the status of the matches in the 2nd innings
dlvr_df = match_df.merge(dlvr_df,on='match_id')
dlvr_df=dlvr_df[dlvr_df['inning']==2]  # getting the dataframe for the 2nd inning
dlvr_df['current_score'] = dlvr_df.groupby('match_id').cumsum()["total_runs_y"] # the cumulative i.e score of the batting team until the present delivery is stored in a new colums current_score

dlvr_df['runs_left'] = dlvr_df['total_runs_x']-dlvr_df['current_score']
dlvr_df['balls_left'] = 120 -((dlvr_df['over']-1)*6 + dlvr_df['ball'])

# now we calculate at which ball the wicket was taken for the player
dlvr_df['player_dismissed'] = dlvr_df['player_dismissed'].fillna("0") 
dlvr_df['player_dismissed'] = dlvr_df['player_dismissed'].apply(lambda x:x if x == "0" else "1")
dlvr_df['player_dismissed'] = dlvr_df['player_dismissed'].astype('int') 
wkts = dlvr_df.groupby('match_id').cumsum()['player_dismissed'].values
dlvr_df['wickets'] = 10 - wkts


# calculating the present run rate 
dlvr_df['curr_run_rate'] = (dlvr_df['current_score']*6)/(120-dlvr_df['balls_left'])

# now we calculate the required run rate for the team to win the match

dlvr_df['req_run_rate'] = (dlvr_df['runs_left']*6) / dlvr_df['balls_left']

def match_won(entry):
    return 1 if entry['batting_team']== entry['winner'] else 0
dlvr_df['result']= dlvr_df.apply(match_won,axis=1)

