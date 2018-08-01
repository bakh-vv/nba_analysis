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

for csv_file in os.listdir('CSV datasets\csv 1 quarters'):
     csv_path = str.format('CSV datasets\csv 1 quarters\{0}', csv_file)
     df_quarter = pd.read_csv(csv_path, sep=', ')
     three_p_percentage = (df_quarter['FG3M'].sum() / df_quarter['FG3A'].sum()) * 100

     team_3p_percentages_1_quarter.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_1st' : three_p_percentage})
     team_3p_percentages_1_quarter_with_volume.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_1st' : three_p_percentage, '3p_volume_attempted_1st': df_quarter['FG3A'].sum()})



team_3p_percentages_3_quarter = []
team_3p_percentages_3_quarter_with_volume = []

for csv_file in os.listdir('CSV datasets\csv 3 quarters'):
     csv_path = str.format('CSV datasets\csv 3 quarters\{0}', csv_file)
     df_quarter = pd.read_csv(csv_path, sep=', ')
     three_p_percentage = (df_quarter['FG3M'].sum() / df_quarter['FG3A'].sum()) * 100

     team_3p_percentages_3_quarter.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_3rd' : three_p_percentage})
     team_3p_percentages_3_quarter_with_volume.append({'team' : df_quarter['TEAM_NAME'][0], '3p_percentage_3rd' : three_p_percentage, '3p_volume_attempted_3rd': df_quarter['FG3A'].sum()})


df_3p_1_quarter = pd.DataFrame(team_3p_percentages_1_quarter)
df_3p_3_quarter = pd.DataFrame(team_3p_percentages_3_quarter)

#merge the two dataframes for convenience
df_3p_1st_and_3rd = df_3p_1_quarter.merge(df_3p_3_quarter)
df_3p_1st_and_3rd = df_3p_1st_and_3rd[['team', '3p_percentage_1st', '3p_percentage_3rd']]

# difference μ1−μ2 between quarter accuracy for each team
df_3p_1st_and_3rd['Difference_between_1st_and_3rd'] = df_3p_1st_and_3rd['3p_percentage_1st'] - df_3p_1st_and_3rd['3p_percentage_3rd']
df_3p_1st_and_3rd[['team', 'Difference_between_1st_and_3rd']]

# histogram and descriptive statistics
df_3p_1st_and_3rd.hist("Difference_between_1st_and_3rd")
plt.title("Histogram of the difference between 1st and 3rd quarter 3 point shot accuracy")
plt.xlabel("Difference")
plt.ylabel("Teams")
df_3p_1st_and_3rd['Difference_between_1st_and_3rd'].describe()

# in Russian
df_3p_1st_and_3rd.hist("Difference_between_1st_and_3rd")
plt.title("Гистограмма разницы в точности трехочковых бросков между 1ой и 3ей четвертями")
plt.xlabel("Разница")
plt.ylabel("Команды")

stats.ttest_rel(df_3p_1st_and_3rd['3p_percentage_1st'], df_3p_1st_and_3rd['3p_percentage_3rd'])
# nothing significant, but the "3 quarter warriors"


### C->C Chi-square test for independence
# in games where the lead is within 5 points at the half, does being ahead correlate with winning?

#each game is duplicated (counted once for both home and away team)
df_first_half_duplicated = pd.read_csv('CSV datasets\\all_games_first_half_plus_minus.csv', sep=', ')
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

#checking if lead of exactly 4 points is significant, still not
df_first_half_close_game = df_first_half[(df_first_half['PLUS_MINUS'] == -4) | (df_first_half['PLUS_MINUS'] == 4)]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)

#checking if lead within 5 points is significant, yes
df_first_half_close_game = df_first_half[((df_first_half['PLUS_MINUS'] >= -5) & (df_first_half['PLUS_MINUS'] <= -1)) | ((df_first_half['PLUS_MINUS'] >= 1) & (df_first_half['PLUS_MINUS'] <= 5))]

df_first_half_close_game['1st_half_win'] = df_first_half_close_game['PLUS_MINUS'] > 0
df_first_half_close_game[['WL', 'PLUS_MINUS', '1st_half_win']]

pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL']), correction = False)



### Multiple C->Q ANOVA
# Position – age?
df_position_age = pd.read_csv('CSV datasets\\positionage.csv', sep=', ')


df_position_age_cleaned = df_position_age.drop(499)
sns.boxplot(df_position_age_cleaned['PLAYER_POSITION'], df_position_age_cleaned['AGE'])
plt.title("Boxplots of the ages of players by different positions")
plt.xlabel("Position")
plt.ylabel("Age")

# In Russian
sns.boxplot(df_position_age_cleaned['PLAYER_POSITION'], df_position_age_cleaned['AGE'])
plt.title("Диаграммы размаха возрастов игроков в разных позициях")
plt.xlabel("Позиция")
plt.ylabel("Возраст")

df_position_age_cleaned.groupby('PLAYER_POSITION')['AGE'].describe()

df_position_age_cleaned.query('PLAYER_POSITION=="C-F"')['AGE'].hist() #potential outlier
df_position_age_cleaned.query('PLAYER_POSITION=="C-F"')['AGE'].idxmax() #116

#running ANOVA on the full data
stats.f_oneway(df_position_age_cleaned.query('PLAYER_POSITION=="C"')['AGE'], \
    df_position_age_cleaned.query('PLAYER_POSITION=="C-F"')['AGE'], df_position_age_cleaned.query('PLAYER_POSITION=="F"')['AGE'], \
    df_position_age_cleaned.query('PLAYER_POSITION=="F-C"')['AGE'], df_position_age_cleaned.query('PLAYER_POSITION=="F-G"')['AGE'], \
    df_position_age_cleaned.query('PLAYER_POSITION=="G"')['AGE'], df_position_age_cleaned.query('PLAYER_POSITION=="G-F"')['AGE'])

# running ANOVA on the data without the outliers in the "C-F' and 'F-C" positions - Dirk Nowitzki and Nick Collison
df_position_age_cleaned_outliers = df_position_age_cleaned.drop(116)
df_position_age_cleaned_outliers = df_position_age_cleaned_outliers.drop(df_position_age_cleaned_outliers.query('PLAYER_POSITION=="F-C"')['AGE'].idxmax())

stats.f_oneway(df_position_age_cleaned_outliers.query('PLAYER_POSITION=="C"')['AGE'], \
    df_position_age_cleaned_outliers.query('PLAYER_POSITION=="C-F"')['AGE'], df_position_age_cleaned_outliers.query('PLAYER_POSITION=="F"')['AGE'], \
    df_position_age_cleaned_outliers.query('PLAYER_POSITION=="F-C"')['AGE'], df_position_age_cleaned_outliers.query('PLAYER_POSITION=="F-G"')['AGE'], \
    df_position_age_cleaned_outliers.query('PLAYER_POSITION=="G"')['AGE'], df_position_age_cleaned_outliers.query('PLAYER_POSITION=="G-F"')['AGE'])
#the results are the same, so the outliers did not influence the results


### C->C Chi-square test for independence
# Usa/not usa -> position?
df_position_usa = pd.read_csv('CSV datasets\\positionUSA.csv', sep=', ')
df_position_int = pd.read_csv('CSV datasets\\positionInt.csv', sep=', ')

df_position_usa['Origin'] = 'USA'
df_position_int['Origin'] = 'International'

# remove data entry outlier (he's not the only "pure" pg)
df_position_origin = df_position_usa.append(df_position_int)
df_position_origin_clean = df_position_origin.drop(df_position_origin.index[df_position_origin['PLAYER_POSITION'] == "PG"].tolist()[0])

pd.crosstab(df_position_origin['Origin'], df_position_origin['PLAYER_POSITION'], margins=True)
pd.crosstab(df_first_half_close_game['1st_half_win'], df_first_half_close_game['WL'], normalize='index', margins=True)

pd.crosstab(df_position_origin_clean['PLAYER_POSITION'], df_position_origin_clean['Origin'], margins=True)
pd.crosstab(df_position_origin_clean['PLAYER_POSITION'], df_position_origin_clean['Origin'], normalize='index', margins=True)

stats.chi2_contingency(pd.crosstab(df_position_origin_clean['PLAYER_POSITION'], df_position_origin_clean['Origin']), correction = False)




### Q->Q regression t-test for the slope
# Draft number height?
df_player_bios = pd.read_csv('CSV datasets\\playerbios.csv', sep=', ')

df_player_bios['DRAFT_NUMBER'] = pd.to_numeric(df_player_bios['DRAFT_NUMBER'], errors='coerce')
df_player_bios['PLAYER_HEIGHT_INCHES'] = pd.to_numeric(df_player_bios['PLAYER_HEIGHT_INCHES'], errors='coerce')

df_player_bios.plot.scatter('DRAFT_NUMBER', 'PLAYER_HEIGHT_INCHES')
# not linear 


### Q->Q  regression t-test for the slope
# Windgspan deflections?
df_player_wingspan = pd.read_csv('CSV datasets\\namewingspanposition.csv', sep=',')
df_player_deflections = pd.read_csv('CSV datasets\\playerdeflections.csv', sep=', ')

df_wingspan_deflections_with_nans = df_player_deflections.merge(df_player_wingspan, left_on = 'PLAYER_NAME', right_on = 'Player', how = 'left')
# weed out inconsistencies in data
df_wingspan_deflections_oneoff = df_wingspan_deflections_with_nans.dropna()
df_wingspan_deflections = df_wingspan_deflections_oneoff.query('GP >= 15')

df_wingspan_deflections['DEFLECTIONS'] = pd.to_numeric(df_wingspan_deflections['DEFLECTIONS'], errors='coerce')

df_wingspan_deflections_centers = df_wingspan_deflections.query('Pos=="C"')
df_wingspan_deflections_forwards = df_wingspan_deflections[(df_wingspan_deflections['Pos'] == "PF") | (df_wingspan_deflections['Pos'] == "SF")]
df_wingspan_deflections_guards = df_wingspan_deflections[(df_wingspan_deflections['Pos'] == "PG") | (df_wingspan_deflections['Pos'] == "SG")]


df_wingspan_deflections.plot.scatter('Wingspan-in', 'DEFLECTIONS')
df_wingspan_deflections_centers.plot.scatter('Wingspan-in', 'DEFLECTIONS')
df_wingspan_deflections_forwards.plot.scatter('Wingspan-in', 'DEFLECTIONS')
df_wingspan_deflections_guards.plot.scatter('Wingspan-in', 'DEFLECTIONS')

# In Russian
df_wingspan_deflections_guards.plot.scatter('Wingspan-in', 'DEFLECTIONS')
plt.title("Диаграмма рассеяния размаха рук и количества результативных отклонений среди защитников")
plt.xlabel("Размах рук")
plt.ylabel("Результативные отклонения")

df_wingspan_deflections['Wingspan-in'].corr(df_wingspan_deflections['DEFLECTIONS'])

stats.linregress(df_wingspan_deflections['Wingspan-in'], df_wingspan_deflections['DEFLECTIONS'])
stats.linregress(df_wingspan_deflections_centers['Wingspan-in'], df_wingspan_deflections_centers['DEFLECTIONS'])
stats.linregress(df_wingspan_deflections_forwards['Wingspan-in'], df_wingspan_deflections_forwards['DEFLECTIONS'])
stats.linregress(df_wingspan_deflections_guards['Wingspan-in'], df_wingspan_deflections_guards['DEFLECTIONS'])


### Q->Q  regression t-test for the slope
# Windgspan steals?
df_player_wingspan = pd.read_csv('CSV datasets\\namewingspanposition.csv', sep=',')
df_player_defensive = pd.read_csv('CSV datasets\\playerdefensive.csv', sep=', ')

df_wingspan_defensive_with_nans = df_player_defensive.merge(df_player_wingspan, left_on = 'PLAYER_NAME', right_on = 'Player', how = 'left')
# weed out inconsistencies in data
df_wingspan_defensive_oneoff = df_wingspan_defensive_with_nans.dropna()
df_wingspan_defensive = df_wingspan_defensive_oneoff.query('GP > 15')

df_wingspan_defensive['STL'] = pd.to_numeric(df_wingspan_defensive['STL'], errors='coerce')

df_wingspan_defensive_centers = df_wingspan_defensive.query('Pos=="C"')
df_wingspan_defensive_forwards = df_wingspan_defensive[(df_wingspan_defensive['Pos'] == "PF") | (df_wingspan_defensive['Pos'] == "SF")]
df_wingspan_defensive_guards = df_wingspan_defensive[(df_wingspan_defensive['Pos'] == "PG") | (df_wingspan_defensive['Pos'] == "SG")]


df_wingspan_defensive.plot.scatter('Wingspan-in', 'STL')
df_wingspan_defensive_centers.plot.scatter('Wingspan-in', 'STL')
df_wingspan_defensive_forwards.plot.scatter('Wingspan-in', 'STL')
df_wingspan_defensive_guards.plot.scatter('Wingspan-in', 'STL')

# In Russian
df_wingspan_defensive_guards.plot.scatter('Wingspan-in', 'STL')
plt.title("Диаграмма рассеяния размаха рук и количества успешных перехватов среди защитников")
plt.xlabel("Размах рук")
plt.ylabel("Перехваты")

df_wingspan_defensive['Wingspan-in'].corr(df_wingspan_defensive['STL'])

stats.linregress(df_wingspan_defensive['Wingspan-in'], df_wingspan_defensive['STL'])
stats.linregress(df_wingspan_defensive_centers['Wingspan-in'], df_wingspan_defensive_centers['STL'])
stats.linregress(df_wingspan_defensive_forwards['Wingspan-in'], df_wingspan_defensive_forwards['STL'])
stats.linregress(df_wingspan_defensive_guards['Wingspan-in'], df_wingspan_defensive_guards['STL'])


