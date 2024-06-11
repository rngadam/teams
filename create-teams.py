#!/usr/bin/env python3
import csv
import random

MAX_TEAMS = 13
PER_TEAM = 5
r = csv.reader(open('voting.csv'))
headers = next(r)
prefs = {name: [] for name in headers[2:]}
scoring = {name: 0 for name in headers[2:]}
descriptions = {name: 0 for name in headers[2:]}

# iterate through all rows, reading both the current person name
# and the description of its project
rows = list(r)
for row in rows:
    pref_name = row[0]
    descriptions[pref_name] = ' '.join(row[1].strip().split('\n'))
    for i, pref in enumerate(row[2:]):
        if pref:
            try:
                pref_value = int(pref)
            except ValueError:
                continue
            assert pref_value > 0 and pref_value <= MAX_TEAMS
            pref_index = pref_value-1
            name = headers[i+2]
            prefs[name].insert(pref_index, pref_name)
            scoring[pref_name] = scoring[pref_name] + (MAX_TEAMS-pref_index)

# assign a score based on popularity of subject
# based on where they rank in individual preference
scored = list(zip(scoring.keys(), scoring.values()))
random.shuffle(scored)
scored = sorted(scored, key=lambda x: x[1], reverse=True)
print(">>> All problem definition ordered by most popular to least popular")
print(scored)

print(">>> Selected top scoring teams")
top = scored[0:MAX_TEAMS]

name_to_id = {}
i = 1
for t in top:
    name = t[0]
    print(f"team #{i}: {descriptions[name]}")
    name_to_id[name] = i
    i = i + 1

# shuffle participants
participants = list(prefs.keys())
random.shuffle(participants)

# create teams based on most popular MAX_TEAMS
teams = {name: [name] for name, score in top}
for lead in teams.keys():
    participants.remove(lead)

# assign pref in order and collect participants that don't have pref
# to fill in teams later
unmatched = []
for participant in participants:
    for pref in prefs[participant]:
        if pref in teams:
            if len(teams[pref]) < PER_TEAM:
                teams[pref].append(participant)
                break
    else:
        print(f"{participant} has no pref in available teams")
        unmatched.append(participant)

total_unmatched = len(unmatched)
teams2 = zip(teams.keys(), teams.values())
teams2 = sorted(teams2, key=lambda x: len(x[1]), reverse=True)
while len(teams2[-1][1]) < PER_TEAM:
    teams2[-1][1].append(unmatched.pop())
    teams2 = sorted(teams2, key=lambda x: len(x[1]), reverse=True)
print(">>> Teams (including unmatched team members)")
print(teams2)

print(">>> Teams printout")
teams2 = sorted(teams2, key=lambda x: name_to_id[x[0]])
for t in teams2:
    name = t[0]
    i = name_to_id[name]
    print(f"team #{i}: {descriptions[name]} ({name})\n\t{t[1]}")

total_participants = sum([len(t[1]) for t in teams2])
print(">>> Checking")
print(f"Total participants: {total_participants}")
print(f"Total no prefs used: {total_unmatched}")

assert(total_participants == len(prefs.keys()))