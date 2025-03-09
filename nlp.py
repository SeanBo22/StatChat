# Course: CSC525
# Sean Bohuslavsky

# Import the necessary libraries
import spacy
import data
import json
import random

# Load the custom NLP model
nlp = spacy.load("./nba_model")

# Define a list of suggestions
suggestions = ["How many points did LeBron James average in 2024?", "How many rebounds did the Lakers average in 2024?", "How many assists did Stephen Curry average in 2024?", "What was the total wins for the Denver Nuggets this season?", \
                "How many losses did the Hornets have in 2024?", "What was the total minutes played for Gary Payton?", "What was the field goal attempts for Jimmy Butler this season?", "What is Stephen Curry's three point percentage?", \
                "Did the Los Angeles Clippers have a good field goal percentage?", "What was the number of threes made for the Knicks in 2024?", "For the current season, what is the attempted three pointers for the Brooklyn Nets?", \
                "How many threes attempted did the Lakers have in 2024?", "What was the free throw percentage for OG Anunoby in 2024?", "Give me the three pointer attempts for Josh Hart?", "How many free throws made did Tyrese Maxey have in 2024?", \
                "This season, how many offensive rebounds did the Pacers have?", "What is Robert Williams's total defensive rebounds in 2024?", "Give me the Kings win percentage."]

# Load the stats abbreviation dictionary
with open("data/stats_abbr.json", "r", encoding="utf-8") as file:
    stats_abbr = json.load(file)

# Function to get suggestions
def get_sugges():
    return random.sample(suggestions,3)

# Function to classify the question
def classify(entities):
    
    goal = None
    name = None
    stat = None
    stat_name = None
    if "PLAYER" in entities and "STAT" in entities:
        name = entities["PLAYER"].lower()
        stat_name = entities["STAT"].lower()
        stat = stats_abbr[stat_name]
        goal = "P_STATS"
    if "TEAM" in entities and "STAT" in entities and "PLAYER" not in entities:
        name = entities["TEAM"].lower()
        stat_name = entities["STAT"].lower()
        stat = stats_abbr[stat_name]
        goal = "T_STATS"
    
    return goal, name, stat, stat_name
    
# Function to process the question
def proc(txt: str):
    doc = nlp(txt)
    
    # Extract entities
    player_entites = [ent.text for ent in doc.ents if ent.label_ == "PLAYER"]
    team_entites = [ent.text for ent in doc.ents if ent.label_ == "TEAM"]
    stat_entites = [ent.text for ent in doc.ents if ent.label_ == "STAT"]
    
    # Check for multiple entities
    if len(stat_entites) > 1:
        sug1, sug2, sug3 = get_sugges()
        return "I'm sorry, I identified that you are asking about multiple stats. I am only able to process one stat at a time. Please ask a similar question to these: \n\n {} \n\n {} \n\n {}".format(sug1, sug2, sug3)
    if len(player_entites) > 1:
        sug1, sug2, sug3 = get_sugges()
        return "I'm sorry, I identified that you are asking about multiple players. I am only able to process one Player at a time. Please ask a similar question to these: \n\n {} \n\n {} \n\n {}".format(sug1, sug2, sug3)
    if len(team_entites) > 1:
        sug1, sug2, sug3 = get_sugges()
        return "I'm sorry, I identified that you are asking about multiple teams. I am only able to process one team at a time. Please ask a similar question to these: \n\n {} \n\n {} \n\n {}".format(sug1, sug2, sug3)
    
    # Make a dictionary of entities
    entities = {ent.label_: ent.text for ent in doc.ents}
    
    # Check if all entities are present
    response = ""
    if "PLAYER" not in entities and "TEAM" not in entities:
        sug1, sug2, sug3 = get_sugges()
        return "I'm sorry, I was unable to identify the player or team in your question. Please ask a statistical question containing a player or team name in the 2024 NBA season. Also, please ensure to use the player's or teams full name. Please ask a similar question to these: \n\n {} \n\n {} \n\n {}".format(sug1, sug2, sug3)
    if "STAT" not in entities:
        if "PLAYER" in entities:
            return "I'm sorry, I was unable to identify the statistic in your question. Please ask a question containing a statistic for {}. \n\n Check the Info tab for supported statistics.".format(entities["PLAYER"])
        if "TEAM" in entities:
            return "I'm sorry, I was unable to identify the statistic in your question. Please ask a question containing a statistic for {}.".format(entities["TEAM"])
    
    # If DATE is present, check if it is valid
    if "DATE" in entities:
        if entities["DATE"] not in ["2024", "2024-25", "this season", "current season", "in 2024", "in 2024-25", "This Season", "Current Season", "In 2024", "In 2024-25", "the current season", "the 2024 season", "This season", "The 2024 season", "For the current season"]:
           response += "I can only provide statistics for the 2024 NBA season. Here is the information for the 2024 season. "
           
    # Classify the question
    goal, name, stat, stat_name = classify(entities)

    # If the question is classified, process it
    if goal != None:
        
        # If the goal is to get player stats
        if goal == "P_STATS":
            season = "2024-25"
            player_name = name
            player_id = data.get_player_id(player_name)
            if player_id:
                if stat:
                    try:
                        season_stat = data.p_stats_season(player_id, season, stat)
                        if stat not in ["FG_PCT", "FT_PCT", "FG3_PCT"]:
                            pergame_stat = data.p_stats_per_game(player_id, season, stat)
                            response += "In the 2024 season, {} averages {:.2f} {} per game. His current total {} for the season is {}.".format(player_name.title(), float(pergame_stat), stat_name, stat_name, season_stat)
                        else:
                            season_stat = season_stat * 100
                            response += "{} currently has a {:.2f}% {} on the season.".format(player_name.title(), float(season_stat), stat_name)
                    except:
                        return "It looks like your question for {} and the statistic {} is not supported. \n\n Check the Info tab for supported statistics. Player Statistics have a P label".format(player_name.title(), stat_name)
            return response

        # If the goal is to get team stats
        elif goal == "T_STATS":
            season = "2024-25"
            team_name = name
            team_id = data.get_team_id(team_name)
            if team_id:
                if stat:
                    try:
                        season_stat = data.t_stats_season(team_id, season, stat)
                        if stat in ["WINS", "LOSSES"]:
                            response += "In the 2024 season the {} have {} {}.".format(team_name.title(), season_stat, stat_name)
                        elif stat == "WIN_PCT":
                            season_stat = season_stat * 100
                            response += "The {} currently have a {:.2f}% win percentage.".format(team_name.title(), season_stat)
                        elif stat not in ["FG_PCT", "FT_PCT", "FG3_PCT"]:
                            season_stat_total = data.t_stats_total(team_id, season, stat)
                            response += "In the 2024 season the {} are currently averaging {:.2f} {} per game. With that average, they have a total of {} {} on the season.".format(team_name.title(), season_stat, stat_name, int(season_stat_total), stat_name)
                        else:
                            season_stat = season_stat * 100
                            response += "The {} currently have a {:.2f}% {} on the season.".format(team_name.title(), season_stat, stat_name)
                    except:
                        return "It looks like your question for {} and the statistic {} is not supported. \n\n Check the Info tab for supported statistics. Team Statistics have a T label".format(team_name.title(), stat_name)
            return response
                    
            
    else:
        sug1, sug2, sug3 = get_sugges()
        return "I'm sorry, I don't understand your input. Please ask me similar questions like: \n\n {} \n\n {} \n\n {}".format(sug1, sug2, sug3)