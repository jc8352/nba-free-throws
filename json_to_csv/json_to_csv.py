import csv
import json


with open('2023_players_shooting.json') as file1:
	data = json.loads(file1.read())

with open('2023_players_traditional.json') as file3:
	data2 = json.loads(file3.read())

with open('2023_players_drives.json') as file4:
	data3 = json.loads(file4.read())

with open('2023_players_cs.json') as file5:
	data4 = json.loads(file5.read())

col_names = data['resultSets']['headers'][1]['columnNames']
player_stats = data['resultSets']['rowSet']

for i in range(data['resultSets']['headers'][0]['columnsToSkip'], len(col_names), data['resultSets']['headers'][0]['columnSpan']):
	#print(i)
	#print(int((i-data['resultSets']['headers'][0]['columnsToSkip'])/data['resultSets']['headers'][0]['columnSpan']))
	shot_distance_index = int((i-data['resultSets']['headers'][0]['columnsToSkip'])/data['resultSets']['headers'][0]['columnSpan'])
	shot_distance = data['resultSets']['headers'][0]['columnNames'][shot_distance_index]
	shot_distance = shot_distance.split(" ")
	shot_distance.pop()
	shot_distance = "".join(shot_distance)
	#print(shot_distance)
	col_names[i] = shot_distance+col_names[i]
	col_names[i+1] = shot_distance+col_names[i+1]
	col_names[i+2] = shot_distance+col_names[i+2]

col_names = col_names+data2['resultSets'][0]['headers'][12:16:3]+data2['resultSets'][0]['headers'][17:20]+data2['resultSets'][0]['headers'][6:11:4]+[data3['resultSets'][0]['headers'][10]]+[data4['resultSets'][0]['headers'][9]]
fts = sorted(data2['resultSets'][0]['rowSet'], key=lambda x:x[1])
drives = sorted(data3['resultSets'][0]['rowSet'], key=lambda x:x[1])
catch_and_shoot = sorted(data4['resultSets'][0]['rowSet'], key=lambda x:x[1])
#print(player_stats[0:5]+[x[17:20] for x in fts[0:5]])
player_stats = [player_stats[i]+fts[i][12:16:3]+fts[i][17:20]+fts[i][6:11:4]+[drives[i][10]]+[catch_and_shoot[i][9]] for i in range(len(player_stats))]
#print([player_stats[i]+fts[i][17:20] for i in range(5)])
#player_stats = player_stats+[x[17:20] for x in fts]

#print(fts[0:5])

#print(col_names)
#print(player_stats[0:5])
with open('2023_players_complete.csv', 'w') as file2:
	writer = csv.writer(file2)
	writer.writerow(col_names)
	for entry in player_stats:
		writer.writerow(entry)
