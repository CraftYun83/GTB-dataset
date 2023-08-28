import json
from litemapy import Schematic, Region, BlockState

size = (0, 0, 0)

with open('earth_unfiltered.json') as f:
    data = json.load(f)
    f.close()

with open('blocks.json') as b:
    blocks = json.load(b)
    b.close()

types = []
typesDict = {}

blockchanges = []
for i in data:
    if i["meta"]["name"] == "block_change":
        position = i["data"]["location"]
        position["x"] = position["x"]-150
        position["y"] = position["y"]
        position["z"] = position["z"]-150
        blockchanges.append(i)
        types.append(i["data"]["type"])
        size = (max(size[0], position["x"]+1), max(size[1], position["y"]+1), max(size[2], position["z"]+1))

with open('earth.json', 'w') as jsonfile:
    json.dump(blockchanges, jsonfile)

types = set(types)
blocks = blocks["blocks"]["block"]

for block in blocks:
    ids = set([*range(blocks[block]["min_state_id"], blocks[block]["max_state_id"]+1)])
    _id = blocks[block]["numeric_id"]
    intersections = list(ids.intersection(types))
    for i in intersections:
        if len(blocks[block]["states"]) != 0:
            s = False
            for state in blocks[block]["states"]:
                if state["name"] == "color":
                    typesDict[str(i)] = state["values"][i-blocks[block]["min_state_id"]].lower()+"_"+blocks[block]["text_id"]
                    s = True
            if not s:
                typesDict[str(i)] = blocks[block]["text_id"]
        else:
            typesDict[str(i)] = blocks[block]["text_id"]

reg = Region(0, 0, 0, size[0], size[1], size[2])
schem = reg.as_schematic(name="Earth", author="FourMC", description="GTB Dataset")

for j in blockchanges:
    position = j["data"]["location"]
    reg.setblock(position["x"], position["y"], position["z"], BlockState("minecraft:"+typesDict[str(j["data"]["type"])]))
        
schem.save("earth.litematic")
