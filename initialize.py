import tableCreationScript
from world import World
from location import Settlement
from location import Dungeon

# Load tables from JSONs into memory
tableCreationScript.main()

# Commit test change
print("Hello world!")