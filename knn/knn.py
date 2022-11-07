#Author: Jerry Lam z5057498
#knn.py
from sklearn import neighbors
import pandas as pd
import glob
from sklearn import metrics
import numpy as np

RSSI_all = []
BSSID_all = []
test_list = []



#allocate the data and location into a 2D array
#example: [RSSI value, location 1]
lst = [[RSSI_all_file_average[0], 1], [RSSI_all_file_average[1], 2], [RSSI_all_file_average[2], 3], [RSSI_all_file_average[3], 4], [RSSI_all_file_average[4], 5], [RSSI_all_file_average[5], 6], [RSSI_all_file_average[6], 7], [RSSI_all_file_average[7], 8], [RSSI_all_file_average[8], 9], [RSSI_all_file_average[9], 10]]
df = pd.DataFrame(lst, columns =['RSSI(dBm)', 'Location']) #use panda to form a table
#print(df)

#knn algorithm initiate
n = 1
knn = neighbors.KNeighborsClassifier(n_neighbors=n, weights='distance', algorithm= "auto", leaf_size=30, p=2, metric_params=None, n_jobs=1)

#print(np.array(df["RSSI(dBm)"]).reshape(-1, 1))
#print(df["Location"].re)

#reshape the 1D data into 2D array (requirment of knn)
test_list = np.array(test_list).reshape(-1, 1)
knn.fit(np.array(df["RSSI(dBm)"]).reshape(-1, 1), np.array(df["Location"]).reshape(-1, 1))

#predict location
predicted_y = knn.predict(test_list)
print(predicted_y)