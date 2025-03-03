import os
import json

input_replay = "xG/27fd6a6d-e6fb-4c50-ba97-226fa491054a.replay"
output_json = "xG/output.json"

#os.system(f"rattletrap --input {input_replay} --output {output_json}")

with open(output_json, 'r') as json_file:
    data = json.load(json_file)

header = data["header"]
content = data["content"]["body"]
frames = content["frames"]

properties = header["body"]["properties"]
elements = properties["elements"]

team0score = elements[2][1]["value"]["int"]
team1score = elements[3][1]["value"]["int"]
totsecplayed = elements[4][1]["value"]["float"]
goalsarray = elements[7][1]["value"]["array"]
highlightsarray = elements[8]

print(f"Team0 {team0score} - {team1score} Team 1")
print(f"Match lasted {totsecplayed} seconds.")

allgoals = []

for i in range(len(goalsarray)):
    elements = goalsarray[i]["elements"]
    frame = elements[0][1]["value"]["int"]
    playername = elements[1][1]["value"]["str"]
    playerteam = elements[2][1]["value"]["int"]
    print(f"Player {playername} of team {playerteam} scored at frame {frame}")
    dict = {"frame": frame, "name": playername,"team": playerteam}
    allgoals.append(dict)

def getFrame(frame):
    print(frames[frame])


getFrame(1500)
