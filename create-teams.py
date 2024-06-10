import csv
import random

MAX_TEAMS = 13
PER_TEAM = 5
r = csv.reader(open('example.csv'))
headers = next(r)
prefs = {name: [] for name in headers[2:]}
scoring = {name: 0 for name in headers[2:]}

rows = list(r)
for row in rows:
    for i, pref in enumerate(row[2:]):
        if pref:
            pref_name = row[0]
            pref_value = int(pref)
            assert pref_value > 0 and pref_value <= MAX_TEAMS
            pref_index = pref_value-1
            name = headers[i+2]
            prefs[name].insert(pref_index, pref_name)
            scoring[pref_name] = scoring[pref_name] + (MAX_TEAMS-pref_index)

scored = list(zip(scoring.keys(), scoring.values()))
random.shuffle(scored)
scored = sorted(scored, key=lambda x: x[1], reverse=True)
print(">>> All problem definition ordered by most popular to least popular")
print(scored)

participants = list(prefs.keys())
random.shuffle(participants)

teams = {name: [] for name, score in scored[0:13]}
unmatched = []
for participant in participants:
    for pref in prefs[participant]:
        if pref in teams:
            if len(teams[pref]) == 0 and participant != pref:
                teams[pref].append(pref)
                participants.remove(pref)
            if len(teams[pref]) < PER_TEAM:
                teams[pref].append(participant)
                break
    else:
        print(f"{participant} has no pref in available teams")
        unmatched.append(participant)

teams2 = zip(teams.keys(), teams.values())
teams2 = sorted(teams2, key=lambda x: len(x[1]), reverse=True)
while len(teams2[-1][1]) < PER_TEAM:
    teams2[-1][1].append(unmatched.pop())
    teams2 = sorted(teams2, key=lambda x: len(x[1]), reverse=True)
print(">>> Teams (including unmatched team members)")
print(teams2)

print(">>> Teams printout")
i = 1
for t in teams2:
    print(f"team #{i}: {t[0]}: {t[1]}")
    i = i + 1

total_participants = sum([len(t[1]) for t in teams2])
print(">>> Checking")
print(total_participants)
assert(total_participants == len(prefs.keys()))