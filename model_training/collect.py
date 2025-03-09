# Course: CSC525
# Sean Bohuslavsky

# Import the necessary libraries
import json
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import teams
import time
import unicodedata

# Initialize dictionaries to store NBA team rosters and player IDs
nba_teams_players = {}
nba_players_id = {}

# Get all NBA teams
all_teams = teams.get_teams()

# Iterate through each team
for team in all_teams:
    team_name = team['full_name']
    team_id = team['id']
    print(f"Team: {team_name}, ID: {team_id}")
    
    # Initialize a list to store player names for this team
    player_list = []
    time.sleep(10) 
    print(f"Fetching roster for {team_name}...")
    players_data = commonteamroster.CommonTeamRoster(team_id=team_id, season=2024)
    
    # Get the raw JSON response from the API
    team_player_string = players_data.get_json()
    
    # If the response is a string, parse it into a dictionary
    if isinstance(team_player_string, str):
        team_player_json = json.loads(team_player_string)
        row_set = team_player_json["resultSets"][0]["rowSet"]
        
        # Append the player names to the list
        for player in row_set:
            player_name = player[3]
            player_name = player_name.replace(" Jr.", "")
            player_name = player_name.replace(" III", "")
            player_name = player_name.replace(" II", "")
            player_name = player_name.replace(" IV", "")
            player_id = player[-2]
            player_name = ''.join(c for c in unicodedata.normalize('NFKD', player_name) if not unicodedata.combining(c))
            if player_name not in player_list:
                player_list.append(player_name)
            
            # Add the player name and ID to the dictionary
            nba_players_id[player_name] = player_id
    
    # Add the player list to the dictionary with the team name as the key
    nba_teams_players[team_name] = player_list

# Print the dictionary
print(json.dumps(nba_teams_players, indent=4))

# Save the nba_teams_players dictionary to a JSON file
with open('nba_teams_players.json', 'w', encoding='utf-8') as f:
    json.dump(nba_teams_players, f, ensure_ascii=False, indent=4)

# Save the nba_players_id dictionary to a JSON file
with open('nba_players_id.json', 'w', encoding='utf-8') as f:
    json.dump(nba_players_id, f, ensure_ascii=False, indent=4)










