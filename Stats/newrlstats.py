import pandas as pd
import sys

def process_file(input_file, output_file):
    df = pd.read_csv(input_file, sep=';')
    
    required_columns = [
        'team name', 'player name', 'win percentage', 'score per game', 'goals per game',
        'assists per game', 'saves per game', 'shots per game',
        'shooting percentage', 'demos inflicted per game'
    ]
    df = df[required_columns]
    
    numeric_columns = required_columns[2:]
    #numeric_columns.remove('score per game')
    #numeric_columns.remove('demos inflicted per game')
    averages = df[numeric_columns].mean()
    
    new_df = pd.DataFrame()
    new_df['team name'] = df['team name']
    new_df['player name'] = df['player name']
    
    for col in numeric_columns:
        avg = averages[col]
        rating_col = f"r{col.split(' ', 1)[0].capitalize()}"
        new_df[rating_col] = round(df[col] / avg,3)
        new_df[col] = df[col]
    
    rating_columns = [f"r{col.split(' ', 1)[0].capitalize()}" for col in numeric_columns]
    weights = {'rWin': 1.5, 'rScore': 0.0, 'rGoals': 1.0, 'rAssists': 1.0, 'rSaves': 1.0, 'rShots': 1.0, 'rShooting': 1.0, 'rDemos': 0.0}
    total_weight = sum(weights.values())
    
    weighted_sum = (new_df[rating_columns] * pd.Series(weights)).sum(axis=1)
    new_df['rating'] = (weighted_sum / total_weight).round(3)

    # Move rating column to 3rd position
    cols = new_df.columns.tolist()
    cols = cols[:2] + ['rating'] + [c for c in cols[2:] if c != 'rating']
    new_df = new_df[cols]
    
    averages_dict = {'team name': 'Average', 'player name': ''}
    
    for col in numeric_columns:
        averages_dict[col] = averages[col].round(3)
    
    for col in numeric_columns:
        rating_col = f"{col} rating"
        averages_dict[rating_col] = 1.0
    
    averages_dict['rating'] = new_df['rating'].mean().round(3)
    
    averages_df = pd.DataFrame([averages_dict], columns=new_df.columns)
    new_df = pd.concat([new_df, averages_df], ignore_index=True)
    new_df.to_csv(output_file, index=False)
    with open(output_file) as f:
            lines = f.readlines()
            last = len(lines) - 1
            lines[last] = lines[last].replace('\r','').replace('\n','')
    with open(output_file, 'w') as wr:
        wr.writelines(lines)
if True:
    filename = "Stats/europe-bizraz5v3p-players (1).csv"
    process_file(filename, "Stats/processed-"+filename[6:])