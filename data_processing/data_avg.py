# Raw data filtering and average code
# By Cameron McGowan (z5361406)

from collections import defaultdict
import json

unique_loc = []

def open_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

#Filter database to keep only the SSIDS we need
def filter_data(filename):
    bssid = defaultdict(list)
    database = open_json_file(filename)

    # Converts temp_dict into a dictionary containing all bssids in the database
    ssid_to_keep = ['eduroam', 'uniwide', 'UNSW Guest', 'Global_Students']

    #Loop through array of dictionaries
    for location in database:

        #Loop through location key (fingerprint)
        for wifi_ap_entry_items in location.items():
            wifi_ap_entry_loc = wifi_ap_entry_items[0]
            if wifi_ap_entry_loc not in unique_loc:
                unique_loc.append(wifi_ap_entry_loc)
            wifi_ap_entry = wifi_ap_entry_items[1]
            #If a SSID in ssid_to_keep is in the key, keep it
            for ssid_bssid in list(wifi_ap_entry.items()):
                ssid = ssid_bssid[0].split(",")[0][1:]
                mac = ssid_bssid[0].split(",")[1][1:-1]
                rssi = ssid_bssid[1]
                #A match was found, keep the key (do nothing)
                #print(ssid)
                if (ssid in ssid_to_keep):
                    bssid[mac].append(tuple((wifi_ap_entry_loc, rssi)))
                    #print("keep")
                    #print(mac, rssi)
                    pass
                else:
                    #No match was found, delete the key
                    #print("REMOVING")
                    del wifi_ap_entry[ssid_bssid[0]]

                #print(location)
    return bssid

def avg_data(database):
    bssid = defaultdict(dict)
    for mac, data in database.items():
        if (len(data) <= 0):
            break
        if not bssid[mac]:
            bssid[mac]["loc"] = list()
            bssid[mac]["rssi"] = list()
        curr_loc = data[0][0]
        count = 0
        total = 0.0
        for loc, rssi in data:
            if (loc == curr_loc):
                count += 1
                total += rssi         
            else:
                bssid[mac]["loc"].append(curr_loc)
                bssid[mac]["rssi"].append(total / count) #is rssi as a float okay?
                count = 1
                total = float(rssi)
                curr_loc = loc

        bssid[mac]["loc"].append(curr_loc)
        bssid[mac]["rssi"].append(total / count) #is rssi as a float okay?   
    return bssid

if __name__ == "__main__":
    with open('avg_data.json', 'w') as fp:
        json.dump(avg_data(filter_data("data.json")), fp)
