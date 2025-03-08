import spacy
import json
import re
import random
from spacy.training import Example


# Load a blank English NLP model
nlp = spacy.load("en_core_web_sm")

# Create an EntityRuler and add it to the pipeline
ruler = nlp.add_pipe("entity_ruler", before="ner")

# Load NBA team data from JSON
with open("data/nba_teams_players.json", "r", encoding="utf-8") as file:
    nba_data = json.load(file)

# Create entity patterns for teams (handling case and partial names)
team_patterns = []
player_patterns = []

# Add team patterns
for team, players in nba_data.items():
    # Add full team name
    team_patterns.append({"label": "TEAM", "pattern": team})
    team_patterns.append({"label": "TEAM", "pattern": team.lower()})
    
    # Optionally, add the last word of the team name as a pattern
    words = team.split()
    if len(words) > 1:
        team_patterns.append({"label": "TEAM", "pattern": words[-1]})
        team_patterns.append({"label": "TEAM", "pattern": words[-1].lower()})
    
    # Add player patterns for each team
    for player in players:
        player_patterns.append({"label": "PLAYER", "pattern": player})
        player_patterns.append({"label": "PLAYER", "pattern": player.lower()})
        player_patterns.append({"label": "PLAYER", "pattern": player.title()})
        cl_player = re.sub(r'[^\w\s]', '', player)
        player_patterns.append({"label": "PLAYER", "pattern": cl_player})
        player_patterns.append({"label": "PLAYER", "pattern": cl_player.lower()})
        player_patterns.append({"label": "PLAYER", "pattern": cl_player.title()})
        

# Load NBA team data from JSON
with open("data/stats.json", "r", encoding="utf-8") as file:
    player_stats_data = json.load(file)

# Create entity patterns for teams (handling case and partial names)
stats_patterns = []

# Add team patterns
for type, stat_names in player_stats_data.items():
    
    # Add player patterns for each team
    for stat_name in stat_names:
        # Add full team name
        stats_patterns.append({"label": "STAT", "pattern": stat_name})
        stats_patterns.append({"label": "STAT", "pattern": stat_name.lower()})
        
      
# Add team and player patterns to the EntityRuler
ruler.add_patterns(team_patterns + player_patterns + stats_patterns)


# Create training data with labeled entities
TRAIN_DATA = [
    ("How many points did Lebron James average in 2024?", [(20, 33, "PLAYER"), (9, 15, "STAT"), (41, 48, "DATE")]),
    ("What was the rebound count for Kevin Durant in 2024?", [(31, 43, "PLAYER"), (10, 16, "STAT"), (44, 50, "DATE")]),
    ("How many assists did Stephen Curry get this season?", [(22, 37, "PLAYER"), (7, 13, "STAT"), (39, 50, "DATE")]),
    ("In 2024, how many block did Anthony Davis average?", [(28, 41, "PLAYER"), (18, 23, "STAT"), (0, 7, "DATE")]),
    ("This season, what was derrick white turnover count?", [(22, 35, "PLAYER"), (36, 45, "STAT"), (0, 11, "DATE")]),
    ("What was the total wins for the Denver Nuggets this season?", [(32, 46, "TEAM"), (19, 23, "STAT"), (47, 58, "DATE")]),
    ("How many losses did the Hornets have in 2024?", [(25, 32, "TEAM"), (10, 16, "STAT"), (38, 45, "DATE")]),
    ("What was the total minutes played for gary payton?", [(39, 50, "PLAYER"), (20, 27, "STAT")]),
    ("What was the field goal attempts for jimmy butler this season?", [(37, 49, "PLAYER"), (13, 32, "STAT"), (50, 61, "DATE")]),
    ("What is Stephen Curry's three point percentage?", [(9, 22, "PLAYER"), (25, 47, "STAT")]),
    ("For three point percentage, what was the number for patty Mills?", [(53, 64, "PLAYER"), (5, 27, "STAT")]),
    ("Did the Los Angles Clippers have a good field goal percentage?", [(8, 28, "TEAM"), (41, 62, "STAT")]),
    ("The number of threes made for the Knicks in 2024?", [(35, 41, "TEAM"), (14, 26, "STAT"), (42, 49, "DATE")]),
    ("For the current season, what is the attempted three pointers for the Brooklyn nets?", [(69, 83, "TEAM"), (36, 60, "STAT"), (8, 22, "DATE")]),
    ("How many threes attempted did the Lakers have in 2024?", [(34, 41, "TEAM"), (9, 25, "STAT"), (47, 54, "DATE")]),
    ("Og anunoby's free throw percentage in 2024?", [(0, 10, "PLAYER"), (13, 35, "STAT"), (36, 44, "DATE")]),
    ("Give me the three pointer attempts for josh hart?", [(40, 49, "PLAYER"), (12, 34, "STAT")]),
    ("How many free throws made did Tyrese Maxey have in 2024?", [(31, 43, "PLAYER"), (9, 26, "STAT"), (49, 56, "DATE")]),
    ("This seasons, how many offensive rebounds did the Pacers have?", [(50, 56, "TEAM"), (23, 41, "STAT"), (0, 12, "DATE")]),
    ("What is Robert Williams's total defensive rebounds in 2024?", [(8, 23, "PLAYER"), (32, 50, "STAT"), (51, 58, "DATE")]),
    ("Give me the Kings win percentage.", [(12, 17, "TEAM"), (18, 32, "STAT")]),
      
]

examples = []
for text, annotations in TRAIN_DATA:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, {"entities": annotations})
    examples.append(example)

# Enable training for NER only
optimizer = nlp.resume_training()
ner = nlp.get_pipe("ner")

# Add new entity labels
for _, annotations in TRAIN_DATA:
    for ent in annotations:
        ner.add_label(ent[2])

# Train the model
for iteration in range(10):  # 10 epochs
    random.shuffle(examples)
    losses = {}
    nlp.update(examples, drop=0.2, losses=losses)
    print(f"Iteration {iteration + 1}, Losses: {losses}")

# Save the trained model
nlp.to_disk("nba_model")

### WORKING
# Test sentences
test_sentences = [
    "In 2024, how many Points did Lebron James average?",
    "What was the rebound count for Kevin Durant in 2024?",
    "How many assists did Stephen Curry get this season?",
    "How many points did Lebron James average in 2024?",
    "What was the rebound count for Kevin Durant in 2024?",
    "How many wins did the Lakers have in 2024?",
    "What is jimmy butler's three point percentage?",
    "How many games did the Lakers win in 2024?",
    "How many threes did the Nuggets and Jamal Murray make in 2024?",
    "How many three attempts did the Lakers have in 2016?"
]

# Process each sentence
for sentence in test_sentences:
    doc = nlp(sentence)

    # Print detected entities
    print(f"Sentence: {sentence}")
    print("Entities detected:")
    
    # Print spaCy detected entities
    for ent in doc.ents:
        print(f"{ent.text} -> {ent.label_}")

    
    print("-" * 40)  # Separator for readability
