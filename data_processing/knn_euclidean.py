# knn matching algorithm without machine learning
# Written by Cameron McGowan (z5361406)

import json

def open_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def match(database, fingerprint):
    finger_size = len(database)
    if finger_size == 2:
        finger_size = 1
    matches = list()
    for loc, sample in database.items():
        dist = 0.0
        count = 0
        for ssid_mac, rssi in sample.items():
            if ssid_mac in fingerprint:
                dist += pow(abs(rssi), 2)
                count += 1
        if count > finger_size / 2:
            matches.append(tuple((dist / count, loc)))
    matches.sort()
    return matches       
            
# Returns true if top floor, else bottom floor
def localise(matches):
    k = 5
    length = len(matches)
    length = min(length, k)
    if length > 0 and length % 2 == 0:
        length -= 1
    floor3 = 0
    floor2 = 0
    for i in range(length):
        if int(matches[i][1].split("_")[1]) <= 15:
            floor3 += 1
        else:
            floor2 += 1
    return floor3 > floor2

def test():
    database = open_json_file("filtered_avg_day.json")
    fingerprints = open_json_file("filtered_avg_night.json")
    correct = 0
    count = 0
    k = 5
    for loc, fingerprint in fingerprints.items():
        matches = match(database, fingerprint)
        length = len(matches)
        length = min(length, k)
        if length > 0 and length % 2 == 0:
            length -= 1
        floor3 = 0
        floor2 = 0
        for i in range(length):
            if int(matches[i][1].split("_")[1]) <= 15:
                floor3 += 1
            else:
                floor2 += 1
        if floor3 > floor2 and int(loc.split("_")[1]) <= 15 or floor3 < floor2 and int(loc.split("_")[1]) > 15:
            correct += 1
        count += 1
    print(correct, count)

if __name__ == "__main__":
    test()
    
    

        
    
    
