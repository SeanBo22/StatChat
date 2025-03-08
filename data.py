# Course: CSC525
# Sean Bohuslavsky

# Import the necessary libraries
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamyearbyyearstats
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Sample player data for testing
# PLAYER STATS FROM NBA_API
''''
    PLAYER_ID SEASON_ID LEAGUE_ID     TEAM_ID TEAM_ABBREVIATION  PLAYER_AGE  GP  GS     MIN  FGM   FGA  FG_PCT  FG3M  FG3A  FG3_PCT  FTM  FTA  FT_PCT  OREB  DREB  REB  AST  STL  BLK  TOV   PF   PTS
0      203076   2012-13        00  1610612740               NOH        20.0  64  60  1846.0  349   676   0.516     0     6    0.000  169  225   0.751   165   357  522   63   75  112   89  158   867
1      203076   2013-14        00  1610612740               NOP        21.0  67  66  2358.0  522  1005   0.519     2     9    0.222  348  440   0.791   207   466  673  105   89  189  109  200  1394
2      203076   2014-15        00  1610612740               NOP        22.0  68  68  2455.0  642  1199   0.535     1    12    0.083  371  461   0.805   173   523  696  149  100  200   95  141  1656
3      203076   2015-16        00  1610612740               NOP        23.0  61  61  2164.0  560  1136   0.493    35   108    0.324  326  430   0.758   130   497  627  116   78  125  121  148  1481
4      203076   2016-17        00  1610612740               NOP        24.0  75  75  2708.0  770  1526   0.505    40   134    0.299  519  647   0.802   172   712  884  157   94  167  181  168  2099
5      203076   2017-18        00  1610612740               NOP        25.0  75  75  2727.0  780  1462   0.534    55   162    0.340  495  598   0.828   187   644  831  174  115  193  162  159  2110
6      203076   2018-19        00  1610612740               NOP        26.0  56  56  1850.0  530  1026   0.517    48   145    0.331  344  433   0.794   174   498  672  218   88  135  112  132  1452
7      203076   2019-20        00  1610612747               LAL        27.0  62  62  2131.0  551  1096   0.503    72   218    0.330  444  525   0.846   142   435  577  200   91  143  154  156  1618
8      203076   2020-21        00  1610612747               LAL        28.0  36  36  1162.0  301   613   0.491    26   100    0.260  158  214   0.738    62   224  286  110   45   59   74   60   786
9      203076   2021-22        00  1610612747               LAL        29.0  40  40  1404.0  370   695   0.532    13    70    0.186  174  244   0.713   106   288  394  122   49   90   82   97   927
10     203076   2022-23        00  1610612747               LAL        30.0  56  54  1905.0  542   962   0.563    19    74    0.257  348  444   0.784   195   507  702  148   59  114  122  146  1451
11     203076   2023-24        00  1610612747               LAL        31.0  76  76  2700.0  713  1283   0.556    29   107    0.271  421  516   0.816   239   722  961  266   91  178  159  177  1876
12     203076   2024-25        00  1610612747               LAL        31.0  42  42  1439.0  400   758   0.528    28    94    0.298  253  321   0.788   119   380  499  141   54   90   93   82  1081
'''

# Sample team data for testing
# TEAM STATS FROM NBA_API
'''
       TEAM_ID    TEAM_CITY TEAM_NAME     YEAR  GP  WINS  LOSSES  WIN_PCT  CONF_RANK  DIV_RANK  PO_WINS  PO_LOSSES  CONF_COUNT  DIV_COUNT NBA_FINALS_APPEARANCE   FGM   FGA  FG_PCT  FG3M  FG3A  FG3_PCT   FTM   FTA  FT_PCT  OREB  DREB   REB   AST    PF  STL   TOV  BLK    PTS  PTS_RANK
0   1610612747  Minneapolis    Lakers  1948-49  60    44      16    0.733          0         2        8          2         NaN          6       LEAGUE CHAMPION  31.4   0.0   0.000   0.0   0.0    0.000  21.2   0.0   0.000   0.0   0.0   0.0  18.9  23.1  0.0   0.0  0.0   84.0         1
1   1610612747  Minneapolis    Lakers  1949-50  68    51      17    0.750          0         1       10          2         NaN          5       LEAGUE CHAMPION  31.5   0.0   0.000   0.0   0.0    0.000  21.2   0.0   0.000   0.0   0.0   0.0  20.7  24.6  0.0   0.0  0.0   84.1         4
2   1610612747  Minneapolis    Lakers  1950-51  68    44      24    0.647          0         1        3          4         NaN          5                   N/A  30.6   0.0   0.000   0.0   0.0    0.000  21.5   0.0   0.000   0.0   0.0   0.0  20.7  26.5  0.0   0.0  0.0   82.8         8
3   1610612747  Minneapolis    Lakers  1951-52  66    40      26    0.606          0         2        9          4         NaN          6       LEAGUE CHAMPION  31.9   0.0   0.000   0.0   0.0    0.000  21.8   0.0   0.000   0.0   0.0   0.0  21.0  26.7  0.0   0.0  0.0   85.6         5
4   1610612747  Minneapolis    Lakers  1952-53  70    48      22    0.686          0         1        9          3         NaN          5       LEAGUE CHAMPION  30.9   0.0   0.000   0.0   0.0    0.000  23.0   0.0   0.000   0.0   0.0   0.0  19.3  27.4  0.0   0.0  0.0   84.9         5
..         ...          ...       ...      ...  ..   ...     ...      ...        ...       ...      ...        ...         ...        ...                   ...   ...   ...     ...   ...   ...      ...   ...   ...     ...   ...   ...   ...   ...   ...  ...   ...  ...    ...       ...
72  1610612747  Los Angeles    Lakers  2020-21  72    42      30    0.583          0         0        2          4        15.0          5                   N/A  40.6  86.1   0.472  11.1  31.2    0.354  17.2  23.3   0.739   9.7  34.6  44.2  24.7  19.1  7.8  15.2  5.4  109.5        22
73  1610612747  Los Angeles    Lakers  2021-22  82    33      49    0.402         11         4        0          0        15.0          5                   N/A  41.6  88.8   0.469  12.0  34.5    0.347  16.8  23.0   0.732   9.5  34.5  44.0  24.0  20.2  7.6  14.5  5.2  112.1        11
74  1610612747  Los Angeles    Lakers  2022-23  82    43      39    0.524          7         5        8          8        15.0          5                   N/A  42.9  89.0   0.482  10.8  31.2    0.346  20.6  26.6   0.775  10.0  35.7  45.7  25.3  17.9  6.4  14.1  4.6  117.2         6
75  1610612747  Los Angeles    Lakers  2023-24  82    47      35    0.573          8         3        1          4        15.0          5                   N/A  43.7  87.5   0.499  11.8  31.4    0.377  18.9  24.2   0.782   8.2  34.9  43.1  28.5  15.6  7.4  14.0  5.5  118.0         6
76  1610612747  Los Angeles    Lakers  2024-25  56    35      21    0.625          4         1        0          0        15.0          5                   N/A  41.2  85.5   0.482  12.3  34.7    0.355  18.2  23.0   0.792   9.3  33.1  42.4  26.6  16.7  7.7  13.8  4.9  113.0        15
'''

# Load player IDs from JSON file
with open("data/player_ids.json", "r", encoding="utf-8") as file:
        player_ids = json.load(file)

# Load team IDs from JSON file
with open("data/team_ids.json", "r", encoding="utf-8") as file:
        team_ids = json.load(file)

# Function to get the player ID
def get_player_id(player_name: str):
    # Get a list of player names from the player_ids JSON
    player_names = list(player_ids.keys())
    
    # Find the best match using fuzzy matching
    best_match, score = process.extractOne(player_name, player_names, scorer=fuzz.token_sort_ratio)
    
    # If the match score is above 80, return the player ID
    if score >= 80:
        return player_ids[best_match]
    else:
        return None

# Function to get the team ID
def get_team_id(team_name: str):
    # Get a list of player names from the team_ids JSON
    team_names = list(team_ids.keys())
    
    # Find the best match using fuzzy matching
    best_match, score = process.extractOne(team_name, team_names, scorer=fuzz.token_sort_ratio)
    
    # If the match score is above 30, return the team ID
    if score >= 30:
        return team_ids[best_match]
    else:
        return None

# Function to get stats per game
def p_stats_per_game(player_id, season, stat):
    
    # Fetch player career stats
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)

    # Get the JSON response and parse it
    career_stats = career_stats.get_json()
    career_stats = json.loads(career_stats)

    # Extract column headers and data
    headers = career_stats["resultSets"][0]["headers"]
    row_set = career_stats["resultSets"][0]["rowSet"]

    # Create a DataFrame
    df = pd.DataFrame(row_set, columns=headers)

    # Make a copy of the DataFrame to avoid the warning
    season_stats = df[df["SEASON_ID"] == season].copy()

    # Calculate the stats per game
    season_stats[stat] = season_stats[stat] / season_stats["GP"]

    # Return the requested stat
    return season_stats[stat].values[0]

# Function to get stats per season
def p_stats_season(player_id, season, stat):
    # Fetch Anthony Davis' career stats 203076
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)

    # Get the JSON response and parse it
    career_stats = career_stats.get_json()
    career_stats = json.loads(career_stats)

    # Extract column headers and data
    headers = career_stats["resultSets"][0]["headers"]
    row_set = career_stats["resultSets"][0]["rowSet"]

    # Create a DataFrame
    df = pd.DataFrame(row_set, columns=headers)

    # Make a copy of the DataFrame to avoid the warning
    season_stats = df[df["SEASON_ID"] == season].copy()

    # Return the requested stat
    return season_stats[stat].values[0]

# Function to get team stats
def t_stats_season(team_id, season, stat):
    
    # Fetch team stats 
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id, season_type_all_star="Regular Season", per_mode_simple="PerGame", league_id="00")

    # Get the JSON response and parse it
    team_stats = team_stats.get_json()
    team_stats = json.loads(team_stats)

    # Extract column headers and data
    headers = team_stats["resultSets"][0]["headers"]
    row_set = team_stats["resultSets"][0]["rowSet"]

    # Create a DataFrame
    df = pd.DataFrame(row_set, columns=headers)

    # Make a copy of the DataFrame to avoid the warning
    season_stats = df[df["YEAR"] == season].copy()

    # Return the requested stat
    return season_stats[stat].values[0]

def t_stats_total(team_id, season, stat):
    
    # Fetch team stats 
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id, season_type_all_star="Regular Season", per_mode_simple="PerGame", league_id="00")

    # Get the JSON response and parse it
    team_stats = team_stats.get_json()
    team_stats = json.loads(team_stats)

    # Extract column headers and data
    headers = team_stats["resultSets"][0]["headers"]
    row_set = team_stats["resultSets"][0]["rowSet"]

    # Create a DataFrame
    df = pd.DataFrame(row_set, columns=headers)

    # Make a copy of the DataFrame to avoid the warning
    season_stats = df[df["YEAR"] == season].copy()

    # Return the requested stat
    return season_stats[stat].values[0] * season_stats["GP"].values[0]

# team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id="1610612747", season_type_all_star="Regular Season", per_mode_simple="PerGame", league_id="00")
# team_stats = team_stats.get_json()
# team_stats = json.loads(team_stats)

# # Extract column headers and data
# headers = team_stats["resultSets"][0]["headers"]
# row_set = team_stats["resultSets"][0]["rowSet"]

# # Create a DataFrame
# df = pd.DataFrame(row_set, columns=headers)

# print(df)


# t_stats_per_season("1610612747", "2024-25", "GP")
# stats_per_game("203076", "2024-25", "REB")
# stats_season("203076", "2024-25", "REB")