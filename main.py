import json
from nbtschematic import SchematicFile

size = (0, 0, 0)

with open('earth_unfiltered.json') as f:
    data = json.load(f)
    f.close()

with open('blocks.json') as b:
    blocks = json.load(b)
    b.close()

blockchanges = []
for i in data:
    if i["meta"]["name"] == "block_change":
        position = i["data"]["location"]
        position["x"] = position["x"]-150
        position["y"] = position["y"]
        position["z"] = position["z"]-150
        blockchanges.append(i)
        size = (max(size[0], position["x"]+1), max(size[1], position["y"]+1), max(size[2], position["z"]+1))

with open('earth.json', 'w') as jsonfile:
    json.dump(blockchanges, jsonfile)

sf = SchematicFile(shape=size)

for j in blockchanges:
    position = j["data"]["location"]
    sf.blocks[position["x"], position["y"], position["z"]] = j["data"]["type"]
        
sf.save('earth.schematic')