# GTB-dataset
trying to build a dataset using guess the build builds from hypixel

you can load `pakkit-script.js` in pakkit to detect when a person starts building and finishes building and then it just saves a json file with the `block_change` packets

then u can use `main.py` to convert the json file into a `.litematic` file. then u can use Lite2Edit (https://github.com/GoldenDelicios/Lite2Edit) to convert to `.schem` file. there are also tools like https://puregero.github.io/SchemToSchematic/ to convert `.schem` to `.schematic`

"block_change" packets are weird af, they use the block state ids instead of the block id itself lmao.

the block_change packets pakkit gives u uses block state ids. each block has a range of state ids. block stats (like the block state id range) can be found on https://pokechu22.github.io/Burger/1.9.html

example:
wool has a state id ranging from 560 to 575
so if given an id of 565, it will be a wool block.
To find the color of the wool, u would look at the list of values available in the color state:

WHITE
ORANGE
MAGENTA
LIGHT_BLUE
YELLOW
LIME
PINK
GRAY
SILVER
CYAN
PURPLE
BLUE
BROWN
GREEN
RED
BLACK

given an id of 565, 560 being first color, 565 would be lime. So we know a block with a state of 565 would be lime wool.

this system is cringe
