This script:

* reads in the csv export from the matrix of proposed problems (rows) and participants (columns) including problem from stakeholder
* scores problems on the number of participants selecting that problem as their preferences (weighted on rank of preference)
* selects the top number of teams (example: 13), setting first member of the team to the stakeholder originator
* shuffle list of participants
* iterate participants
  * assign to the team for which preference exists
  * if no team within preference exists (no preferences stated or no teams for which preferences stated selected), keep on unmatched
* sort teams by numbe of members
  * iterate through unmatched members and add them to teams with lowest number of members
  * resort
* print out final list of teams, description, originator and members
