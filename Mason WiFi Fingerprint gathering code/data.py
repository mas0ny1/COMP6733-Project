import math
import subprocess
import sys
import json
from os.path import exists

# Written by z5316520
# Usage:
# python3 data.py -> read prompt. "r" to run the algorithm, "s" to store data
# OR
# python3 data.py r: to run the algorithm against the currently stored data
# python3 data.py s <location>: to store the current data of all APs and their signal strengths around you under "location" into the database

#PLEASE NOTE: this algorithm is not a machine learning algorithm and is purly for experiemental purposes. This is not machine learning algorithm code.



#Returns string from netsh command to parse into dictionary
def netshCommand():
    #Calls netsh wlan show networks mode=Bssid
    results = subprocess.check_output(["netsh", "wlan", "show", "network", "BSSID"])

    #Decodes to cp437 (avoiding errors from special chars) to removes all \r from output
    results = results.decode("cp437")
    results = results.replace("\r","")

    #Print sys.version
    #print(sys.version)

    #Split each string at two newlines, This only occurs when between each SSID
    string = results.split("\n\n")
    #Remove all whitespaces from each string in string array
    string = list(filter(None, string))
    arr = []
    #For SSID entry in string
    for wifi in string:
        tempArr = []
        #For each line in SSID entry (Channel, Encryption, BSSID etc)
        for line in wifi.split("\n"):

            #If line starts with BSSID
            if "BSSID" in line:
                line2 = ""
                #Remove all whitespaces from line
                line2 = "".join(line.split())
                
                #Replace : with : + space, (eg BSSID:xx:xx:xx:xx -> BSSID: xx: xx: xx: xx)
                line2 = line2.replace(":", ": ")
                
                #Split line into array [BSSID, xx, xx, xx, xx]
                temp = line2.split(":")
            
                #line3 = "BSSID" + ": ""   
                line3 = temp[0] + ": "
                line4 = ""
                
                #Add all other elements in array temp to line4
                for i in range(1, len(temp)):
                    line4 = line4 + temp[i].replace(" ", ":")
                #Result: line4 = " xx:xx:xx:xx"
                
                #Remove first char from line4 (it is a whitespace char)
                line4 = line4[1:]
                
                #Add line3 and line4
                line3 = line3 + line4
                #line3 = "BSSID: xx:xx:xx:xx"
                
                #Append BSSID to tempArr
                tempArr.append(line3)
                
            #If line starts with SSID
            elif "SSID" in line:
                #Split line at :
                line2 = line.split(": ")
                
                #line3 = "SSID" + ": " + SSID_NAME
                line3 = line2[0][:-1] + ": " + line2[1]
                
                #Append SSID to tempArr
                tempArr.append(line3)
                
                
            #If line starts with signal
            elif "Signal" in line:
                
                #Split line at :
                line2 = line.split(": ")
                
                #Remove all whitespaces from line2[0] and line2[1]
                line2[0] = "".join(line2[0].split())
                line2[1] = "".join(line2[1].split())
                
                #Convert signal percentage to float for calculates of RSS in dBm, (ignore the last char as that is "%")
                signal = float(line2[1][:-1])
                
                #Convert signal to dBm using formula given to us in lab
                if signal <= 0:
                    dbm = -100
                elif signal >= 100:
                    dbm = -50
                else:
                    dbm = (signal / 2) - 100
                
                #Append signal to line3 (Signal: x dBm)
                line3 = line2[0] + ": " + str(round(dbm)) #+" dBm"
                
                #Append line3 to tempArr
                tempArr.append(line3)
                
                
            #If line starts with channel
            elif "Channel" in line:
                #Remove all whitespaces
                line2 = "".join(line.split())
                
                #Replace colon with : + space. Channel:hello -> Channel: hello
                line2 = line2.replace(":", ": ")
                
                #Append to tempArr
                tempArr.append(line2)
            else: 
                #Ignore the other lines from netsh output
                continue
        #Append tempArr to arr, so we have a list of arrays where each array entry is the SSID entry
        arr.append(tempArr)
    return arr

#Function to get distance from freq and RSS (dBm). Formula given to us in lab spec
def getDistance(freq, RSS):
    return pow(10, ((27.55 - (20*math.log(freq, 10)) + abs(RSS))/20))


#Goes to last byte of json file ("]") and appends dictionary store replacing the 2nd last char in the json file
#Allows appending to a json file in the form of list of dictionaries [{},{}, etc]
def appendedtoJson(store, location):
    store = {location: store}
    if (exists("data.json")):
        
        #Append to json file
        with open ("data.json", mode="r+") as file:
            file.seek(0,2)
            position = file.tell() -1
            file.seek(position)
            file.write( ",\n{}]".format(json.dumps(store)) )
        print("Appended to json file")
    else:
        # Create new json file
        with open ("data.json", mode="w") as file:
            file.write("[]")
            
        #Append to json file
        with open ("data.json", mode="r+") as file:
            file.seek(0,2)
            position = file.tell() -1
            file.seek(position)
            file.write("{}]".format(json.dumps(store)) )
        print("Created new json file and appended")

def countlines():
    with open("data.json", "r") as file:
        return len(file.readlines())

#Parses string from netshCommand() to dictionary where each key = (SSID, BSSID) and value = Signal in dBm
def arrToDict(arr, toStore):
      
    ssid = ""
    bssid = ""
    signal = ""
    store = {}
    counter = 1
    for ssidEntry in arr:
        for line in ssidEntry:
            
            if (line.startswith("SSID")):
                ssid = line.split(": ")[1]
                if (ssid == ""): 
                    ssid = "Unknown" + str(counter)
                    counter += 1
            elif (line.startswith("BSSID")):
                bssid = line.split(": ")[1]

                key = f"({ssid}, {bssid})"
                
                
                # if toStore is true, key is a string (ssid, bssid) because json cannot append tuple as keys, 
                # else key is a tuple (ssid, bssid)
                # if (toStore):
                #     key = f"({ssid}, {bssid})"
                # else:
                #     key = (ssid, bssid)
            elif (line.startswith("Signal")):
                signal = line.split(": ")[1]
                store[key] = int(signal)
    return store

def getAccessPointInfo():
    dict = arrToDict(netshCommand(), True)
    return dict

def filter_live_data(database, filtered_live_data):
    # Removes any APs that are in live data not but in database
    
    # Converts temp_dict into a dictionary containing all bssids in the database
    temp_dict = {}
    for entry in database:
        for key, value in entry.items():
            temp_dict = {**temp_dict, **value}

    In_database = {i:j for i,j in live_data.items() if i in temp_dict.keys()}
    # In_database is live_data where the bssids are in the database (This removes random APs such as mobile hotspots from influencing the algorithm)
    filtered_live_data = In_database
    
    return filtered_live_data


def algorithm(database, filtered_live_data):
    closely_matching_data = {}
    best_number_of_matches = 0
    location = ""
    index = 0
    
    for location in database:
        num_matches = 0
        strength_distance = 0
        location_key, location_value = list(location.items())[0]
        
        for ap in location.values():
            for live_ap in filtered_live_data:
                ap_key, ap_value = list(ap.items())[0]

                if (live_ap == ap_key):
                    num_matches += 1
                    
                    
                    # Value attached to each location that determines how close the location's signal strengths for each matching Ap 
                    # is to the live_data's signal strengths
                    strength_distance += abs(int(database[index][location_key][ap_key]) - int(filtered_live_data[live_ap]))
                    break
                
        if (num_matches > 0):
            if (num_matches > best_number_of_matches):
                closely_matching_data.clear()             
                best_number_of_matches = num_matches
            closely_matching_data[location_key] = strength_distance
        index += 1
        
    # if not matches found, return None
    if (len(closely_matching_data) == 0):
        return "No matches found"
    # if only 1 match was found, return the location
    elif (len(closely_matching_data) == 1):
        k1, v1 = list(closely_matching_data.items())[0]
        return k1
    # if several matches were found we must check the Signal strength to determine which location is closer
    else:
        closest_difference = sys.maxsize #Large number so that the first if check is always true
        best_match = ""
        
        # Key is location, value is signal strength difference        
        for entry in closely_matching_data:
            key, value = entry, closely_matching_data[entry]
            
            if (value < closest_difference):
                closest_difference = value
                best_match = key
        return best_match
 


#Writes netsh call getting SSID, BSSID and Signal to a json in the format 
# {Location: {(SSID,1 BSSID1): Signal, (SSID1, BSSID2: Signal, ...}}
if __name__ == "__main__":
    if (len(sys.argv) == 1):
        function = input("Enter 'r' to run the algorithm, 's' to get data from surrounding APs and store the data to a json file: ")
    elif (sys.argv[1] == "r"):
        function = "r"
    elif (sys.argv[1] == "s"):
        function = "s"
    else:
        print("Invalid input")
        sys.exit()

    
    if (function == "s" and len(sys.argv) > 1):

        store = getAccessPointInfo()
        location_string = sys.argv[2]
        appendedtoJson(store, location_string)
        print(str(countlines()) + " fingerprint/s in json file")
    elif (function == "r"):
        
            
        with open('data.json') as f:
            database = json.load(f)
        
        live_data = getAccessPointInfo()
        
        #Algorithm here
        filtered_live_data = filter_live_data(database, live_data)
    
        matched_location = algorithm(database, filtered_live_data)
        print(f"You are at: {matched_location}")
   
            

        
        
        
        
        
    else:
        print("Invalid input")
        sys.exit()
    
        
    
