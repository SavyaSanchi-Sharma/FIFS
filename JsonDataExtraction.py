import pandas as pd 
import os 
import json

class JSONExtraction:


    def MatchExtraction(files):
        matchdata = []
        
        for file in files:
            with open(file, 'r') as f:
                data = json.load(f)
                matchID = data['info'].get('match_type_number', 'N/A')
                stadium = data['info'].get('venue', 'N/A')
                teams = data['info']['teams']
                overRun=0
                date=data['info']['dates'][0]
                
                BatStats = {}
                BowlStats = {}
                FieldStats = {}
 
                for inning in data['innings']: 
                    for over in inning['overs']:  
                        for delivery in over['deliveries']:  
                            batsman = delivery['batter']
                            bowler = delivery['bowler']
                            runs = delivery['runs']['batter']
                            extras = delivery['runs'].get('extras', 0)  
                            bowlerRun = delivery['runs']['total']
                            overRun+=bowlerRun
                            if batsman not in BatStats:
                                BatStats[batsman] = {'Runs': 0, 'Balls': 0, 'Dismissals': 0, 'StrikeRate': 0,'Fours': 0, 'Sixes': 0}
                            BatStats[batsman]['Balls'] += 1
                            if runs == 4:
                                BatStats[batsman]['Fours'] += 1
                            elif runs == 6:
                                BatStats[batsman]['Sixes'] += 1
                            else:
                                BatStats[batsman]['Runs'] += runs

                            if bowler not in BowlStats:
                                BowlStats[bowler] = {'BRuns': 0, 'BBalls': 0, 'Wickets': 0, 'Economy': 0, 'Catches': 0, 'Extras': 0,'Overs':0,'Maidens': 0}
                            BowlStats[bowler]['BRuns'] += bowlerRun
                            BowlStats[bowler]['BBalls'] += 1
                            BowlStats[bowler]['Extras'] += extras

                            if 'wickets' in delivery:
                            
                                BowlStats[bowler]['Wickets'] += 1
                                for wicket in delivery['wickets']:
                                    out = wicket['player_out']
                                   
                                    if out in BatStats:
                                        BatStats[out]['Dismissals'] += 1

                                    if 'fielders' in wicket:  
                                        for fielder in wicket['fielders']:  
                                            if 'name' in fielder:
                                                fielderName = fielder['name']
                                                if fielderName not in FieldStats:
                                                    FieldStats[fielderName] = {'Catches': 0, 'Stumpings': 0, 'RunOuts': 0}
                                                if wicket['kind'] == 'caught':
                                                    FieldStats[fielderName]['Catches'] += 1
                                                elif wicket['kind'] == 'stumped':
                                                    FieldStats[fielderName]['Stumpings'] += 1
                                                elif wicket['kind'] == 'run out':
                                                    FieldStats[fielderName]['RunOuts'] += 1
                                                elif wicket['kind'] == 'caught and bowled':
                                                    BowlStats[bowler]['Catches'] += 1
                                
                            if overRun==0:
                                bowler=over['deliveries'][0]['bowler'] 
                                BowlStats[bowler]['Maidens'] += 1

                for player, stats in BatStats.items():
                    sr = (stats['Runs'] / stats['Balls']) * 100 if stats['Balls'] > 0 else 0
                    matchdata.append({
                        'MatchID': matchID,
                        'Stadium': stadium,
                        'Team': teams[0] if player in teams[0] else teams[1],
                        'Date':date,
                        'Player': player,
                        'Runs': stats['Runs'],
                        'FBalls': stats['Balls'],
                        'Dismissals': stats['Dismissals'],
                        'StrikeRate': sr,
                        'Economy': 0,
                        'Runs Conceded': 0,
                        'Balls Bowled': 0,
                        'Wickets': 0,
                        'Catches': 0,
                        'Stumpings': 0,
                        'RunOuts': 0,
                        'Extras': 0,
                        'Fours': stats['Fours'],
                        'Sixes': stats['Sixes'],
                        'Overs':0,
                        'Maidens':0
                    })

                for player, stats in BowlStats.items():
                    eco = (stats['BRuns'] / stats['BBalls']) * 6 if stats['BBalls'] > 0 else 0
                    overB = int(stats['BBalls'] / 6)  
                    matchdata.append({
                        'MatchID': matchID,
                        'Stadium': stadium,
                        'Team': teams[0] if player in teams[0] else teams[1],
                        'Date':date,
                        'Player': player,
                        'Runs': 0,
                        'FBalls': 0,
                        'Dismissals': 0,
                        'StrikeRate': 0,
                        'Economy': eco,
                        'Runs Conceded': stats['BRuns'],
                        'Balls Bowled': stats['BBalls'],
                        'Wickets': stats['Wickets'],
                        'Catches': stats['Catches'],
                        'Stumpings': 0,
                        'RunOuts': 0,
                        'Extras': stats['Extras'],
                        'Fours': 0,
                        'Sixes': 0,
                        'Overs':overB,
                        'Maidens':stats['Maidens']
                    })

                for player, stats in FieldStats.items():
                    matchdata.append({
                        'MatchID': matchID,
                        'Stadium': stadium,
                        'Team': teams[0] if player in teams[0] else teams[1],
                        'Date':date,
                        'Player': player,
                        'Runs': 0,
                        'FBalls': 0,
                        'Dismissals': 0,
                        'StrikeRate': 0,
                        'Economy': 0,
                        'Runs Conceded': 0,
                        'Balls Bowled': 0,
                        'Wickets': 0,
                        'Catches': stats['Catches'],
                        'Stumpings': stats['Stumpings'],
                        'RunOuts': stats['RunOuts'],
                        'Extras': 0,
                        'Fours': 0,
                        'Sixes': 0,
                        'Overs':0,
                        'Maidens':0
                    })

        return pd.DataFrame(matchdata)



json_files = [f for f in os.listdir('odis_json') if f.endswith('.json')]
json_files=['odis_json/'+f for f in json_files]
data=JSONExtraction.MatchExtraction(json_files).to_csv('DataToClean/int.csv')
json_files_dom=[f for f in os.listdir('odms_json') if f.endswith('.json')]
json_files_dom=['odms_json/'+f for f in json_files_dom]
dataDom=JSONExtraction.MatchExtraction(json_files_dom).to_csv('DataToClean/dom.csv')