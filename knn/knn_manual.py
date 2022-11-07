from collections import defaultdict
import json 

#Open Json File
def open_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def lam():
    RSSI_RANGE = 47
    return [[]] * RSSI_RANGE

def generate_prob(file_path, out_path, k):
    #Assume RSSI is from -50 to -96
    RSSI_RANGE = 47
    RSSI_IDX = 96
    #k = 5 #as an example value
    
    samples = []
    APs = defaultdict(lam)
    
    data = open_json_file(file_path)
    # Process raw data so that each AP contains a mapping of RSSI values and
    # locations it mapped to.
    for location in data:
        for loc_name, samples in location.items():
            for id_pair, rssi in samples.items():
                bssid = id_pair.split(',')[1][1:-1]
                idx = int(rssi) + RSSI_IDX
                APs[bssid][idx].append(loc_name)
    
    out_dict = defaultdict(lam)
    for bssid, ap in APs.items():
        idx = 0
        for rssi in ap:
            weights = dict()
            total = 0.0
            for location in rssi: # Count each locations for the given rssi
                weights[location] = weights.get(location, 0) + 1
                total += 1
            i = idx - 1
            j = 0
            q = idx + 1
            r = 0
            # Count up to k locations from the rssi values on each side
            while total < k and (i >= 0 or q < RSSI_RANGE):
                if i >= 0: # Left side
                    if len(ap[i]) > j:
                        weights[ap[i][j]] = weights.get(ap[i][j], 0) + 1
                        j += 1
                        total += 1
                        continue
                    else:
                        i -= 1
                        j = 0
                if q < RSSI_RANGE: # Right side
                    if len(ap[q]) > r:
                        weights[ap[q][r]] = weights.get(ap[q][r], 0) + 1
                        r += 1
                        total += 1
                    else:
                        q += 1
                        r = 0
            probs = list()
            for location, count in weights.items(): #Store as a probability
                probs.append((count / total, location))
                
            probs.sort (reverse = True) # Sort from most likely to least
            out_dict[bssid][idx] = probs # Save back into the dict
            
            idx += 1
    with open(out_path, "w") as out_file:
        json.dump(out_dict, out_file)
