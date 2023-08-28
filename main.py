import json
from litemapy import Schematic, Region, BlockState

schem_name = "target"

with open(f'filtered/{schem_name}.json') as f:
    data = json.load(f)
    f.close()

with open('blocks.json') as b:
    blocks = json.load(b)
    b.close()

types = []
typesDict = {}
coords = []

# Lists location of blocks

blockchanges = []
for i in data:
    if i["meta"]["name"] == "block_change":
        position = i["data"]["location"]
        coords.append(list(position.values()))
        blockchanges.append(i)
        types.append(i["data"]["type"])

# Normalizing coords
itmin = [min(point[i] for point in coords) for i in range(3)]
coords = []

for block in blockchanges:
    position = block["data"]["location"]
    position["x"] -= itmin[0]
    position["y"] -= itmin[1]
    position["z"] -= itmin[2]
    coords.append(list(position.values()))

itmax = [max(point[i] for point in coords) for i in range(3)]

# Mapping state ids to block id

types = set(types)
blocks = blocks["blocks"]["block"]

for block in blocks:
    ids = set([*range(blocks[block]["min_state_id"], blocks[block]["max_state_id"]+1)])
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

# Create schematic

reg = Region(0, 0, 0, itmax[0]+1, itmax[1]+1, itmax[2]+1)
print(itmax)
schem = reg.as_schematic(name="Garage", author="FourMC", description="GTB Dataset")

# Settings blocks

for j in blockchanges:
    position = j["data"]["location"]
    reg.setblock(position["x"], position["y"], position["z"], BlockState("minecraft:"+typesDict[str(j["data"]["type"])]))
        
schem.save(f"schematics/{schem_name}.litematic")
