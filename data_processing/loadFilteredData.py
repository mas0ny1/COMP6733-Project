# Written by Mason Pun z5316520
# This file is an example of how to load the filtered fingerprints into python (FYI the debugging menu for this gives a very nice visualisation of the data)
import json

with open("data_processing\filtereddata.json", 'r') as f:
    database = json.load(f)
    
print(database)