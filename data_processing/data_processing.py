import json
#Written by Mason Pun z5316520
#This removes all non-UNSW SSID+Bssid entries from the database, the list of the ssid to keep is in the array "ssid_to_keep"

#Open Json File
def open_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

#Filter database to keep only the SSIDS we need
def filter_data():
    database = open_json_file('data_processing\data.json')
    
    # Converts temp_dict into a dictionary containing all bssids in the database
    ssid_to_keep = ['eduroam', 'uniwide', 'UNSW Guest', 'Global_Students']

    #Loop through array of dictionaries
    for location in database:
        #Loop through location key (fingerprint)
        for wifi_ap_entry in location.values():
            #If a SSID in ssid_to_keep is in the key, keep it
            for ssid_bssid in list(wifi_ap_entry):
                
                
                ssid = ssid_bssid[1:-1].split(",")[0]
                #A match was found, keep the key (do nothing)
                #print(ssid)
                if (ssid in ssid_to_keep):
                    #print("keep")
                    pass
                else:
                    #No match was found, delete the key
                    #print("REMOVING")
                    del wifi_ap_entry[ssid_bssid]
    
    return database

if __name__ == "__main__":
    with open('filtereddata.json', 'w') as fp:
        json.dump(filter_data(), fp)

