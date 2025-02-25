import json
import math
from datetime import datetime

DATA_FILE = 'team_ratings.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'teams': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def initialize_team():
    return {
        'rating': 1000.0,
        'matches': []
    }

def process_match(team_data, matches):
    """Recalculate rating based on match history"""
    current_rating = 1000.0
    streak = 0
    breakdown = []
    
    for match in matches:
        opponent_rating = match['opponent_rating']
        result = match['result']
        margin = match['margin']
        weight = match['event_weight']
        
        # Calculate expected outcome
        expected = 1 / (1 + 10**((opponent_rating - current_rating)/400))
        
        # Calculate components
        momentum = 1 + 0.2 * streak
        margin_mult = 1 + math.log(1 + margin)
        delta = 32 * momentum * margin_mult * weight * (result - expected)
        
        # Update rating and streak
        new_rating = current_rating + delta
        breakdown.append({
            'opponent': match['opponent'],
            'opponent_rating': opponent_rating,
            'result': 'Win' if result == 1 else 'Loss',
            'score_diff': margin,
            'weight': weight,
            'expected': round(expected, 3),
            'momentum': round(momentum, 2),
            'margin_impact': round(margin_mult, 2),
            'delta': round(delta, 1),
            'new_rating': round(new_rating, 1)
        })
        current_rating = new_rating
        streak = streak + 1 if result == 1 else 0
    
    team_data['rating'] = round(current_rating, 1)
    return breakdown

def add_match_to_history(history, new_match, max_matches=5):
    """Maintain match history with max length"""
    updated = history + [new_match]
    return updated[-max_matches:]

def print_breakdown(team_name, breakdown, new_rating):
    """Print detailed rating change analysis"""
    print(f"\n{'='*40}\n{team_name} Rating Update\n{'='*40}")
    print(f"{'Match':<6}{'Opponent':<12}{'Result':<8}{'Weight':<6}{'Expected':<9}{'Momentum':<9}{'Margin':<7}{'Δ Rating':<10}New Rating")
    
    for i, match in enumerate(breakdown, 1):
        print(f"{i:<6}{match['opponent'][:10]:<12}{match['result']:<8}"
              f"{match['weight']:<6}{match['expected']:<9.3f}"
              f"{match['momentum']:<9.2f}{match['margin_impact']:<7.2f}"
              f"{match['delta']:>+7.1f}{match['new_rating']:>12.1f}")
    
    print(f"\nFinal Rating: {new_rating:.1f}")
    print(f"{'='*40}\n")

def main():
    data = load_data()
    
    # Get user input
    team1 = input("Enter first team name: ").strip()
    team2 = input("Enter second team name: ").strip()
    #event_weight = float(input("Enter event weight (1.8=Major, 1.3=Regional, 0.7=Showmatch): "))
    event_weight = 1.3
    score = input("Enter match score (format '2-1'): ").strip()
    
    # Parse score
    t1_score, t2_score = map(int, score.split('-'))
    if t1_score > t2_score:
        t1_result, t2_result = 1, 0
        margin = t1_score - t2_score
    else:
        t1_result, t2_result = 0, 1
        margin = t2_score - t1_score

    # Initialize teams if needed
    for team in [team1, team2]:
        if team not in data['teams']:
            data['teams'][team] = initialize_team()

    # Store current ratings for match records
    t1_rating_before = data['teams'][team1]['rating']
    t2_rating_before = data['teams'][team2]['rating']

    # Create match records
    t1_match = {
        'opponent': team2,
        'opponent_rating': t2_rating_before,
        'result': t1_result,
        'margin': margin,
        'event_weight': event_weight,
        'date': datetime.now().isoformat()
    }
    
    t2_match = {
        'opponent': team1,
        'opponent_rating': t1_rating_before,
        'result': t2_result,
        'margin': margin,
        'event_weight': event_weight,
        'date': datetime.now().isoformat()
    }

    # Update both teams
    for team, opponent, match in [(team1, team2, t1_match),
                                  (team2, team1, t2_match)]:
        # Add match to history
        data['teams'][team]['matches'] = add_match_to_history(
            data['teams'][team]['matches'], match
        )
        
        # Process matches and get breakdown
        breakdown = process_match(
            data['teams'][team],
            data['teams'][team]['matches']
        )
        
        # Print breakdown
        print_breakdown(team, breakdown, data['teams'][team]['rating'])

    # Save updated data
    save_data(data)
    print("Data successfully saved to", DATA_FILE)

def show_rankings():
    """Displays all teams sorted by their current rating yeah yeha """
    data = load_data()
    teams = data['teams']
    
    # Sort teams by rating descending
    sorted_teams = sorted(teams.items(), 
                         key=lambda x: x[1]['rating'], 
                         reverse=True)
    
    print("\nCurrent Team Rankings:")
    print(f"{'Rank':<5}{'Team':<20}{'Rating':<10}Recent Form")
    for idx, (team_name, team_data) in enumerate(sorted_teams, 1):
        # Show last 3 results as form indicator
        form = ' '.join(['W' if m['result'] == 1 else 'L' 
                        for m in team_data['matches'][-3:]])
        print(f"{idx:<5}{team_name:<20}{team_data['rating']:<10.1f} {form or '-'}")

if __name__ == "__main__":
    show_rankings()
    #main()