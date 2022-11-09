#Author: Jerry Lam z5057498
#knn.py
from sklearn import neighbors
import pandas as pd
import glob
from sklearn import metrics
import numpy as np
import json
from collections import defaultdict
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

unique_loc = []

def open_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

#Filter database to keep only the SSIDS we need
def filter_data(filename):
    bssid = defaultdict(dict)
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
                    if not bssid[mac]:
                        bssid[mac]["loc"] = list()
                        bssid[mac]["rssi"] = list()
                    bssid[mac]["loc"].append(wifi_ap_entry_loc)
                    bssid[mac]["rssi"].append(rssi)
                    #print("keep")
                    #print(mac, rssi)
                    pass
                else:
                    #No match was found, delete the key
                    #print("REMOVING")
                    del wifi_ap_entry[ssid_bssid[0]]
                
                #print(location)        
    return bssid

bssid = filter_data("data.json")
test_bssid = filter_data("testing_sample.json")

    #print(df)

#X_train, X_test, y_train, y_test = train_test_split(df["rssi"], df["loc"], test_size = 0.2)

#allocate the data and location into a 2D array
#example: [RSSI value, location 1]

#knn algorithm initiate
n = 3
knn = neighbors.KNeighborsClassifier(n_neighbors=n, weights='distance', algorithm= "auto", leaf_size=30, p=2, metric_params=None, n_jobs=1)

#print(np.array(df["RSSI(dBm)"]).reshape(-1, 1))
#print(df["Location"].re)
le = preprocessing.LabelEncoder()
le.fit(unique_loc)

result_list = []

for e in test_bssid.items():
    df = pd.DataFrame(data = bssid[e[0]]["rssi"])
#reshape the 1D data into 2D array (requirment of knn)
#test_list = np.array(test_lisst).reshape(-1, 1)
    knn.fit(np.array(bssid[e[0]]["rssi"]).reshape(-1, 1), le.transform(bssid[e[0]]["loc"]))
    print(e[0])
    predicted_y = knn.predict(np.array(e[1]["rssi"]).reshape(-1, 1))
    print(le.inverse_transform(predicted_y))
    result_list.append(le.inverse_transform(predicted_y))
    for location in sorted(unique_loc, key=lambda x: int(x.split("_")[-1])):
        percentage = ((result_list.count(location)) / len(result_list))*100
        
        print(location, str(percentage)+"%")
#predicted_y = knn.predict(test_bssid.values())
#print(test_bssid)
#print(predicted_y)


#predict location
#predicted_y = knn.predict(test_list)
#print(predicted_y)

