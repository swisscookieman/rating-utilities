import json

# Read the original JS file content
with open('xG/threejs.js', 'r') as file:
    js_content = file.read()

# Extract the JSON part by splitting the variable assignment
json_str = js_content.split('=', 1)[1].strip().rstrip(';')

# Parse the JSON string into a Python dictionary
replay_data = json.loads(json_str)

# Save the beautified JSON to a new file
with open('xG/replayData.json', 'w') as json_file:
    json.dump(replay_data, json_file, indent=2)

print("Beautified JSON saved to replayData.json")