#Program to combine Wi-Fi Fingerprint percentage of accurcy and Image Classification percentage of accuracy.

#The index of the array is the location number and the value is the percentage of accuracy.
#These arrays are hardcoded/empty for an example as image classification and Wi-Fi fingerprint algorithms are not yet complete. Obviously these arrays must be the same length.
wifi_percentages = []
image_percentages = []

def apply_formula(wifi_arr, image_arr):
    #The formula is: a x Percentage(Wifi) + b x Percentage(Image)
    a = 0.5
    b = 0.5
    result = []
    for i in range(0, len(wifi_arr)):
        result.append((a * wifi_arr[i]) + (b * image_arr[i]))
    return result

#Finds best match (highest percentage) in the array
def find_max(arr):
    max = 0
    index = 0
    for i in range(0, len(arr)):
        if arr[i] > max:
            max = arr[i]
            index = i
    return index

def find_best_match(wifi_arr, image_arr):
    result = apply_formula(wifi_arr, image_arr)
    return find_max(result)

if __name__ == "__main__":
    pass