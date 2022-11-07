import json
from collections import defaultdict
#Written by Mason Pun z5316520
#Modified by Jerry Lam z5057498
#This removes all non-UNSW SSID+Bssid entries from the database, the list of the ssid to keep is in the array "ssid_to_keep"
#To make the format suitable for the knn algorithm entry

#Open Json File

bssid = defaultdict(dict)

def open_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

#Filter database to keep only the SSIDS we need
def filter_data():
    database = open_json_file('data.json')
    
    # Converts temp_dict into a dictionary containing all bssids in the database
    ssid_to_keep = ['eduroam', 'uniwide', 'UNSW Guest', 'Global_Students']

    #Loop through array of dictionaries
    for location in database:

        #Loop through location key (fingerprint)
        for wifi_ap_entry_items in location.items():
            wifi_ap_entry_loc = wifi_ap_entry_items[0]
            wifi_ap_entry = wifi_ap_entry_items[1]
            #If a SSID in ssid_to_keep is in the key, keep it
            for ssid_bssid in list(wifi_ap_entry.items()):
                ssid = ssid_bssid[0].split(",")[0][1:]
                mac = ssid_bssid[0].split(",")[1][1:-1]
                rssi = ssid_bssid[1]
                #A match was found, keep the key (do nothing)
                #print(ssid)
                if (ssid in ssid_to_keep):
                    if wifi_ap_entry_loc not in bssid[mac]:
                        bssid[mac][wifi_ap_entry_loc] = [rssi]
                    else:
                        bssid[mac][wifi_ap_entry_loc].append(rssi)
                    #print("keep")
                    #print(mac, rssi)
                    pass
                else:
                    #No match was found, delete the key
                    #print("REMOVING")
                    del wifi_ap_entry[ssid_bssid[0]]
                
                #print(location)
        
    print(bssid)         
    return database

if __name__ == "__main__":
    with open('filtereddata.json', 'w') as fp:
        json.dump(filter_data(), fp)