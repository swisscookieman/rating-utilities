import requests
from datetime import datetime
import json

# Configuration
API_KEY = 'MGrUlbbn5y6CXIhFdfMv8u8E13WLGFvtEjVHSBzo'  # Replace with your Ballchasing API key
REPLAY_ID = 'd43807ff-628d-4687-9d04-3cd7329707a0'  # Replace with the replay ID you want to analyze

def save_to_json(data, filename=None):
    """Save data to a JSON file with timestamp"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ballchasing_stats_{REPLAY_ID}_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def get_replay_stats(api_key, replay_id):
    headers = {
        'Authorization': f'{api_key}',
        'Accept': 'application/json'
    }
    
    url = f'https://ballchasing.com/api/replays/{replay_id}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching replay data: {e}")
        return None

def print_player_stats(stats_data):
    if not stats_data:
        return
    
    save_to_json(stats_data)
    
    # Check for teams first
    for team_color in ['blue', 'orange']:
        team = stats_data.get(team_color, {})
        players = team.get('players', [])
        
        if not players:
            continue
            
        print(f"\n=== {team.get('name', team_color.capitalize())} Team ({team_color.upper()}) ===")
        
        for player in players:
            print(f"\nPlayer: {player.get('name', 'Unknown')}")
            print(f"Team: {team_color.capitalize()}")
            print(f"Platform: {player.get('id', {}).get('platform', 'Unknown')}")
            print(f"Profile ID: {player.get('id', {}).get('id', 'N/A')}")
            print(f"Car: {player.get('car_name', 'Unknown')}")
            
            # Detailed stats
            stats = player.get('stats', {})
            print("\nCore Stats:")
            core = stats.get('core', {})
            print(f"  Goals: {core.get('goals', 0)}")
            print(f"  Assists: {core.get('assists', 0)}")
            print(f"  Saves: {core.get('saves', 0)}")
            print(f"  Shots: {core.get('shots', 0)}")
            print(f"  Score: {core.get('score', 0)}")
            print(f"  Shooting %: {core.get('shooting_percentage', 0)}")
            
            print("\nBoost Stats:")
            boost = stats.get('boost', {})
            print(f"  BPM: {boost.get('bpm', 0)}")
            print(f"  Collected: {boost.get('amount_collected', 0)}")
            print(f"  Stolen: {boost.get('amount_stolen', 0)}")
            print(f"  Overfill: {boost.get('amount_overfill', 0)}")
            
            print("\nMovement Stats:")
            movement = stats.get('movement', {})
            print(f"  Total Distance: {movement.get('total_distance', 0)}")
            print(f"  Avg Speed: {movement.get('avg_speed', 0)}")
            print(f"  Time Supersonic: {movement.get('time_supersonic_speed', 0)}")
            
            print("\nPositioning Stats:")
            positioning = stats.get('positioning', {})
            print(f"  Time Defensive Third: {positioning.get('time_defensive_third', 0)}")
            print(f"  Time Offensive Third: {positioning.get('time_offensive_third', 0)}")
            
            print("\nDemonstrations:")
            print(f"  Demolitions: {stats.get('demo', {}).get('inflicted', 0)}")
            print(f"  Demolitions Taken: {stats.get('demo', {}).get('taken', 0)}")
            
            print("\n----------------------------------------")

    if not any(stats_data.get(team) for team in ['blue', 'orange']):
        print("No team data found in the replay")

if True:
    replay_data = get_replay_stats(API_KEY, REPLAY_ID)
    if replay_data:
        print_player_stats(replay_data)
    else:
        print("Failed to retrieve replay data")