import json
import csv

with open("data/world_cup_2018.json", encoding="utf8") as world_cup_file:
    world_cup_data = json.load(world_cup_file)

with open("data/country_populations.csv") as population_file:
    population_data = list(csv.DictReader(population_file))

rounds = world_cup_data["rounds"]

matches = []
for round_ in rounds:
    round_matches = round_["matches"]
    matches.extend(round_matches)

teams_set = set()
for match in matches:
    teams_set.add(match["team1"]["name"])
    teams_set.add(match["team2"]["name"])

teams = sorted(list(teams_set))
combined_data = {team: {"wins": 0} for team in teams}

def find_winner(match):
    if match["score1"] > match["score2"]:
        return match["team1"]["name"]
    elif match["score2"] > match["score1"]:
        return match["team2"]["name"]
    return None

for match in matches:
    winner = find_winner(match)
    if winner:
        combined_data[winner]["wins"] += 1

def normalize_location(country_name):
    name_sub_dict = {
        "Russian Federation": "Russia",
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
        "Korea, Rep.": "South Korea",
        "United Kingdom": "England",
    }
    return name_sub_dict.get(country_name, country_name)

population_data_filtered = []
for record in population_data:
    country = normalize_location(record["Country Name"])
    if country in teams and record["Year"] == "2018":
        record["Country Name"] = country
        population_data_filtered.append(record)

for record in population_data_filtered:
    record["Value"] = int(record["Value"])

for record in population_data_filtered:
    country = record["Country Name"]
    population = record["Value"]
    combined_data[country]["population"] = population

if __name__ == "__main__":
    print(combined_data)
