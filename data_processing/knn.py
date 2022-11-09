#Author: Jerry Lam z5057498
#knn.py
from sklearn import neighbors
import pandas as pd
import glob
from sklearn import metrics
import numpy as np
import json
from collections import defaultdict

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
    return bssid

bssid = filter_data()
for data in bssid.values():
    df = pd.DataFrame(data = data)


test_list = []


#allocate the data and location into a 2D array
#example: [RSSI value, location 1]

#lst = [[RSSI_all_file_average[0], 1], [RSSI_all_file_average[1], 2], [RSSI_all_file_average[2], 3], [RSSI_all_file_average[3], 4], [RSSI_all_file_average[4], 5], [RSSI_all_file_average[5], 6], [RSSI_all_file_average[6], 7], [RSSI_all_file_average[7], 8], [RSSI_all_file_average[8], 9], [RSSI_all_file_average[9], 10]]
#df = pd.DataFrame(lst, columns =['RSSI(dBm)', 'Location']) #use panda to form a table

#print(df)

#knn algorithm initiate
#n = 1
#knn = neighbors.KNeighborsClassifier(n_neighbors=n, weights='distance', algorithm= "auto", leaf_size=30, p=2, metric_params=None, n_jobs=1)

#print(np.array(df["RSSI(dBm)"]).reshape(-1, 1))
#print(df["Location"].re)

#reshape the 1D data into 2D array (requirment of knn)
#test_list = np.array(test_list).reshape(-1, 1)
#knn.fit(np.array(df["RSSI(dBm)"]).reshape(-1, 1), np.array(df["Location"]).reshape(-1, 1))

#predict location
#predicted_y = knn.predict(test_list)
#print(predicted_y)