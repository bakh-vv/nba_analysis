# py jsoncsv.py GSteamgamelogs

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import math


team_3p_percentages_1_quarter = []
team_3p_percentages_1_quarter_with_volume = []

for csv_file in os.listdir(r'C:\Users\Bakhtiyar\source\repos\NBA_analysis\NBA_analysis\csv 1 quarters'):
     csv_path = str.format(r'C:\Users\Bakhtiyar\source\repos\NBA_analysis\NBA_analysis\csv 1 quarters\{0}', csv_file)
     df_quarter = pd.read_csv(csv_path, sep=', ')
     three_p_percentage = (df_quarter['FG3M'].sum() / df_quarter['FG3A'].sum()) * 100

     team_3p_percentages_1_quarter.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_1st' : three_p_percentage})
     team_3p_percentages_1_quarter_with_volume.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_1st' : three_p_percentage, '3p_volume_attempted_1st': df_quarter['FG3A'].sum()})



team_3p_percentages_3_quarter = []
team_3p_percentages_3_quarter_with_volume = []

for csv_file in os.listdir(r'C:\Users\Bakhtiyar\source\repos\NBA_analysis\NBA_analysis\csv 3 quarters'):
     csv_path = str.format(r'C:\Users\Bakhtiyar\source\repos\NBA_analysis\NBA_analysis\csv 3 quarters\{0}', csv_file)
     df_quarter = pd.read_csv(csv_path, sep=', ')
     three_p_percentage = (df_quarter['FG3M'].sum() / df_quarter['FG3A'].sum()) * 100

     team_3p_percentages_3_quarter.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_3rd' : three_p_percentage})
     team_3p_percentages_3_quarter_with_volume.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_3rd' : three_p_percentage, '3p_volume_attempted_3rd': df_quarter['FG3A'].sum()})


df_3p_1_quarter = pd.DataFrame(team_3p_percentages_1_quarter)
df_3p_3_quarter = pd.DataFrame(team_3p_percentages_3_quarter)

#merge the two dataframes for convenience
df_3p_1st_and_3rd = df_3p_1_quarter.merge(df_3p_3_quarter)
df_3p_1st_and_3rd = df_3p_1st_and_3rd[['team', '3p_percentage_1st', '3p_percentage_3rd']]

stats.ttest_rel(df_3p_1st_and_3rd['3p_percentage_1st'], df_3p_1st_and_3rd['3p_percentage_3rd'])
# nothing significant, but the "3 quarter warriors"


###

#each game is duplicated (counted once for both home and away team)
df_first_half_duplicated = pd.read_csv('all_games_first_half_plus_minus.csv', sep=', ')
#duplicates are removed (each game is counted only once)
df_first_half = df_first_half_duplicated.drop_duplicates(subset = 'GAME_ID')


# checked if lead within 2 points is significant, far from that
df_first_half_close_game = df_first_half[((df_first_half['PLUS_MINUS'] >= -2) & (df_first_half['PLUS_MINUS'] <= -1)) | ((df_first_half['PLUS_MINUS'] >= 1) & (df_first_half['PLUS_MINUS'] <= 2))]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)

#checking if lead of exactly 2 points is significant, still not significant
df_first_half_close_game = df_first_half[(df_first_half['PLUS_MINUS'] == -2) | (df_first_half['PLUS_MINUS'] == 2)]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)


#checking if lead within 3 points is significant, still not
df_first_half_close_game = df_first_half[((df_first_half['PLUS_MINUS'] >= -3) & (df_first_half['PLUS_MINUS'] <= -1)) | ((df_first_half['PLUS_MINUS'] >= 1) & (df_first_half['PLUS_MINUS'] <= 3))]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)

#checking if lead of exactly 3 points is significant, still not
df_first_half_close_game = df_first_half[(df_first_half['PLUS_MINUS'] == -3) | (df_first_half['PLUS_MINUS'] == 3)]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)

#checking if lead within 4 points is significant, not
df_first_half_close_game = df_first_half[((df_first_half['PLUS_MINUS'] >= -4) & (df_first_half['PLUS_MINUS'] <= -1)) | ((df_first_half['PLUS_MINUS'] >= 1) & (df_first_half['PLUS_MINUS'] <= 4))]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)

#checking if lead within 5 points is significant
df_first_half_close_game = df_first_half[((df_first_half['PLUS_MINUS'] >= -5) & (df_first_half['PLUS_MINUS'] <= -1)) | ((df_first_half['PLUS_MINUS'] >= 1) & (df_first_half['PLUS_MINUS'] <= 5))]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)