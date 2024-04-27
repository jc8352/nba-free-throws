import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from pathlib import Path 

cwd = Path.cwd()
root = cwd.parent.absolute()


complete_stats = pd.read_csv(root / 'data' / '2023_players_complete.csv')
test_complete_stats = pd.read_csv(root / 'data' / '2022_players_complete.csv')



#filtering to only include players that played at least 200 minutes
mins_played_filtered = complete_stats[complete_stats['GP']*complete_stats['MIN'] >= 200]

#filtering test data to only include players that played at least 200 minutes
test_mins_played_filtered = test_complete_stats[test_complete_stats['GP']*test_complete_stats['MIN'] >= 200]




#converting stats to rates
rates = mins_played_filtered.iloc[:, 6: 42].div(mins_played_filtered.FGA, axis=0)
rates['name'] = mins_played_filtered['PLAYER_NAME']

#correlation of rates with free throw rate
corr_matrix_rates = rates.corr()['FTA']
print("rates matrix:")
print(corr_matrix_rates)
print("\n\n\n")

#correlation with free throw attempts
corr_matrix_avgs = mins_played_filtered.corr()['FTA']
print("averages matrix:")
print(corr_matrix_avgs)
print("\n\n")




#plotting free throw attempts vs non-catch-and-shoot attempts
plt.scatter(mins_played_filtered['FGA']-mins_played_filtered['CATCH_SHOOT_FGA'], mins_played_filtered['FTA'])
x = np.arange(0,20)
plt.xlabel('Non-Catch-and-Shoot Field Goal Attempts')
plt.ylabel('Free Throw Attempts')
plt.title('Free Throw Attempts vs Non-Catch-and-Shoot Field Goal Attempts 2022-23')
plt.show()

plt.scatter(test_mins_played_filtered['FGA']-test_mins_played_filtered['CATCH_SHOOT_FGA'], test_mins_played_filtered['FTA'])
x = np.arange(0,20)
plt.xlabel('Non-Catch-and-Shoot Field Goal Attempts')
plt.ylabel('Free Throw Attempts')
plt.title('Free Throw Attempts vs Non-Catch-and-Shoot Field Goal Attempts 2021-22')
plt.show()



#plotting free throws attempts vs attempts from inside of 5 feet
plt.scatter(mins_played_filtered['LessThan5FGA'], mins_played_filtered['FTA'])
x = np.array([0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5])
plt.xlabel('Less than 5ft Field Goal Attempts')
plt.ylabel('Free Throw Attempts')
plt.title('Free Throw Attempts vs Less than 5ft Field Goal Attempts 2022-23')
plt.show()

plt.scatter(test_mins_played_filtered['LessThan5FGA'], test_mins_played_filtered['FTA'])
x = np.array([0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5])
plt.xlabel('Less than 5ft Field Goal Attempts')
plt.ylabel('Free Throw Attempts')
plt.title('Free Throw Attempts vs Less than 5ft Field Goal Attempts 2021-22')
plt.show()



#correlation between non-catch-and-shoot attempts and free throw attempts. (.878)
print("correlation between non-catch-and-shoot attempts and free throw attempts: ", (mins_played_filtered['FGA']-mins_played_filtered['CATCH_SHOOT_FGA']).corr(mins_played_filtered['FTA']))
print("\n")

#regression 1
"""
free throw rate regression using LessThan5FGA, 20-24FGA, FG3A, and CATCH_SHOOT_FGA
score:  0.4210263761149575
slope:  [ 0.2620386  -0.1659073   0.08604438 -0.22552875]
intercept:  0.228507089709853
"""
X = rates[['LessThan5FGA', '20-24FGA', 'FG3A', 'CATCH_SHOOT_FGA']]
y = rates['FTA']

reg = LinearRegression().fit(X,y)
print('free throw rate regression using LessThan5FGA, 20-24FGA, FG3A, and CATCH_SHOOT_FGA')
print('score: ', reg.score(X,y))
print('slope: ', reg.coef_)
print('intercept: ', reg.intercept_)
print('\n\n')

predicted = reg.predict(rates[['LessThan5FGA', '20-24FGA', 'FG3A', 'CATCH_SHOOT_FGA']])
actual = rates['FTA']
names = rates['name']

games_played = mins_played_filtered['GP']
fga = mins_played_filtered['FGA']
team_abbreviations = mins_played_filtered['TEAM_ABBREVIATION']
teams = {}

ftr_pred_players = []
#predicted free throw rates vs actual for players and predicted free throw attempts vs actual for teams
for i in range(len(predicted)):
	ftr_pred_players.append([names.iloc[i], predicted[i], actual.iloc[i]])
	teams.setdefault(team_abbreviations.iloc[i], {'predicted': 0, 'actual': 0, 'fga': 0, 'diff': None})
	teams[team_abbreviations.iloc[i]]['predicted'] += predicted[i]*fga.iloc[i]*games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['actual'] += actual.iloc[i]*fga.iloc[i]*games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['fga'] += fga.iloc[i]*games_played.iloc[i]
ftr_pred_players_df = pd.DataFrame(sorted(ftr_pred_players, key = lambda x: x[1]-x[2]))
ftr_pred_players_df.columns = ['NAME', 'PREDICTED', 'ACTUAL']
ftr_pred_players_df.to_csv(root / 'data' / 'result' / 'ftr_reg' / 'ftr_pred_players.csv')

for team in teams.keys():
	teams[team]['diff'] = teams[team]['actual']-teams[team]['predicted']
fta_pred_teams_df = pd.DataFrame.from_dict(teams, orient='index')
fta_pred_teams_df.index.name = 'TEAM'
fta_pred_teams_df.reset_index(inplace=True)
fta_pred_teams_df.sort_values(by='diff', ascending=False, inplace=True)
fta_pred_teams_df.to_csv(root / 'data' / 'result' / 'ftr_reg' / 'fta_pred_teams.csv', index=False)


#predicted free throw rates teams vs actual
for key, value in teams.items():
	teams[key]['predicted'] = value['predicted']/value['fga']
	teams[key]['actual'] = value['actual']/value['fga']
	teams[key]['diff'] = teams[key]['actual']-teams[key]['predicted']
ftr_pred_teams_df = pd.DataFrame.from_dict(teams, orient='index')
ftr_pred_teams_df.index.name = 'TEAM'
ftr_pred_teams_df.reset_index(inplace=True)
ftr_pred_teams_df.sort_values(by='diff', ascending=False, inplace=True)
ftr_pred_teams_df.to_csv(root / 'data' / 'result' / 'ftr_reg' / 'ftr_pred_teams.csv', index=False)



#regression 2
"""
score:  0.7822079513481683
slope:  [0.47773399 0.14702203 0.15102734]
intercept:  -0.6459341573996888
"""
X2 = mins_played_filtered[['LessThan5FGA', 'DRIVE_FGA', 'FGA']]
y2 = mins_played_filtered['FTA']
reg = LinearRegression().fit(X2,y2)
print('free throw average regression using LessThan5FGA, DRIVE_FGA, and FGA')
print('score: ', reg.score(X2,y2))
print('slope: ', reg.coef_)
print('intercept: ', reg.intercept_)
print('\n\n')



predicted = reg.predict(mins_played_filtered[['LessThan5FGA', 'DRIVE_FGA', 'FGA']])
actual = mins_played_filtered['FTA']
names = mins_played_filtered['PLAYER_NAME']
games_played = mins_played_filtered['GP']
team_abbreviations = mins_played_filtered['TEAM_ABBREVIATION']
teams = {}

fta_pred_players = []

for i in range(len(predicted)):
	fta_pred_players.append([names.iloc[i], predicted[i], actual.iloc[i]])
	teams.setdefault(team_abbreviations.iloc[i], {'predicted': 0, 'actual': 0, 'games_played': 0, 'players': 0, 'diff': None})
	teams[team_abbreviations.iloc[i]]['predicted'] += predicted[i]*games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['actual'] += actual.iloc[i]*games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['games_played'] += games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['players'] += 1
fta_pred_players_df = pd.DataFrame(sorted(fta_pred_players, key = lambda x: x[1]-x[2]))
fta_pred_players_df.columns = ['NAME', 'PREDICTED', 'ACTUAL']
fta_pred_players_df.to_csv(root / 'data' / 'result' / 'fta_reg1' / 'fta_pred_players.csv')


for team in teams.keys():
	teams[team]['diff'] = teams[team]['actual']-teams[team]['predicted']
fta_pred_teams_df = pd.DataFrame.from_dict(teams, orient='index')
fta_pred_teams_df.index.name = 'TEAM'
fta_pred_teams_df.reset_index(inplace=True)
fta_pred_teams_df.sort_values(by='diff', ascending=False, inplace=True)
fta_pred_teams_df.to_csv(root / 'data' / 'result' / 'fta_reg1' / 'fta_pred_teams.csv', index=False)




#regression 3
"""
free throw average regression using NON_CATCH_SHOOT and LessThan5FGA
score:  0.8048129284952321
slope:  [0.29864775 0.31362132]
intercept:  -0.38782680626063826
test score:  0.743374976827901
"""
mins_played_filtered['NON_CATCH_SHOOT'] = mins_played_filtered['FGA']-mins_played_filtered['CATCH_SHOOT_FGA']
mins_played_filtered['DRIVE_RATE'] = mins_played_filtered['DRIVE_FGA']/mins_played_filtered['FGA']

X2 = mins_played_filtered[['NON_CATCH_SHOOT', 'LessThan5FGA']]
y2 = mins_played_filtered['FTA']
reg = LinearRegression().fit(X2,y2)
print('free throw average regression using NON_CATCH_SHOOT and LessThan5FGA')
print('score: ', reg.score(X2,y2))
print('slope: ', reg.coef_)
print('intercept: ', reg.intercept_)

test_mins_played_filtered['NON_CATCH_SHOOT'] = test_mins_played_filtered['FGA']-test_mins_played_filtered['CATCH_SHOOT_FGA']
X2_test = test_mins_played_filtered[['NON_CATCH_SHOOT', 'LessThan5FGA']]
y2_test = test_mins_played_filtered['FTA']
print('test score: ', reg.score(X2_test, y2_test)) #test on 2021-22 data


predicted = reg.predict(mins_played_filtered[['NON_CATCH_SHOOT', 'LessThan5FGA']])
actual = mins_played_filtered['FTA']
names = mins_played_filtered['PLAYER_NAME']
games_played = mins_played_filtered['GP']
team_abbreviations = mins_played_filtered['TEAM_ABBREVIATION']
teams = {}

fta_pred_players = []

for i in range(len(predicted)):
	fta_pred_players.append([names.iloc[i], predicted[i], actual.iloc[i]])
	teams.setdefault(team_abbreviations.iloc[i], {'predicted': 0, 'actual': 0, 'games_played': 0, 'players': 0, 'diff': None})
	teams[team_abbreviations.iloc[i]]['predicted'] += predicted[i]*games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['actual'] += actual.iloc[i]*games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['games_played'] += games_played.iloc[i]
	teams[team_abbreviations.iloc[i]]['players'] += 1
fta_pred_players_df = pd.DataFrame(sorted(fta_pred_players, key = lambda x: x[1]-x[2]))
fta_pred_players_df.columns = ['NAME', 'PREDICTED', 'ACTUAL']
fta_pred_players_df.to_csv(root / 'data' / 'result' / 'fta_reg2' / 'fta_pred_players.csv')


for team in teams.keys():
	teams[team]['diff'] = teams[team]['actual']-teams[team]['predicted']
fta_pred_teams_df = pd.DataFrame.from_dict(teams, orient='index')
fta_pred_teams_df.index.name = 'TEAM'
fta_pred_teams_df.reset_index(inplace=True)
fta_pred_teams_df.sort_values(by='diff', ascending=False, inplace=True)
fta_pred_teams_df.to_csv(root / 'data' / 'result' / 'fta_reg2' / 'fta_pred_teams.csv', index=False)







