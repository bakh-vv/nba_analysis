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


