This README is for data.py. Written by Mason Pun z5316520 for this for COMP6773, Semester 3, 2022.

How to use data.py:

python3 data.py -> Produce a prompt that explains: "r" to run the algorithm, "s" to store data

You can input r or s directly as an argument to the code in the run call.

Examples:
python3 data.py r: to run the algorithm against the currently stored data. Gets current surrounding APs and runs the algorithm on it, it prints to terminal: "You are at <location>", if no matches found it will print to terminal: "no matches found"

python3 data.py s "location": stored the current data of all APs and their signal strengths around you under "location" into the database (data.json)
for example python3 data.py s "UNSW library": would store the current APs to data.json under UNSW library as the location name

You need to create a data.json file that contains "[]" before running this program