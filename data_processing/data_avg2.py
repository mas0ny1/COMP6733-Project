# Raw data filtering and average code
# By Cameron McGowan (z5361406)

from collections import defaultdict
import json

def open_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

#Filter database to keep only the SSIDS we need
def avg_filter_data(filename):
    locs = defaultdict(list)
    new_locs = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))
    database = open_json_file(filename)
    ssid_to_keep = ['eduroam', 'uniwide', 'UNSW Guest', 'Global_Students']

    #Loop through array of dictionaries
    for location in database:
        for wifi_ap_entry_items in location.items():
            locs[wifi_ap_entry_items[0]].append(wifi_ap_entry_items[1])

    for loc, samples in locs.items():
        for sample in samples:
            for ssid_mac, rssi in sample.items():
                if ssid_mac.split(",")[0][1:] in ssid_to_keep:
                    new_locs[loc][ssid_mac][0] += rssi
                    new_locs[loc][ssid_mac][1] += 1
            
    for loc, sample in new_locs.items():
        for ssid_mac, rssi_tuple in sample.items():
            if rssi_tuple[1] == 0:
                del sample[ssid_mac]
            else:
                new_locs[loc][ssid_mac] = rssi_tuple[0] / rssi_tuple[1]
    return new_locs


if __name__ == "__main__":
    with open('avg_filter_data3.json', 'w') as fp:
        json.dump(avg_filter_data("data2.json"), fp)
