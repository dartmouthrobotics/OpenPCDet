from pathlib import Path
import numpy as np
import sys
import json
import os

# e.g.,
# python print_min_max.py ./ '[[-70.4, -70.4, -4], [70.4, 70.4, 4]]'

print(sys.argv[2])
# INPUT
root_path = sys.argv[1]
min_max_threshold = np.array(json.loads(sys.argv[2]))


pathlist = Path(root_path).rglob('*.npy')
min_max = [[np.inf]*3, [-np.inf]*3]
valid = []
total = 0

for path in pathlist:
    total += 1
    # because path is object not string
    arr = np.load(path)
    if arr.shape[0] == 0:
        print("shape,{}:{}".format(path, arr.shape))
        continue

    tmp_min_max = [[np.inf]*3, [-np.inf]*3]
    for i in range(3):
        tmp_min_max[0][i] = min(arr[:,i])
        tmp_min_max[1][i] = max(arr[:,i])

    tmp_min_max = np.array(tmp_min_max)

    if np.any(tmp_min_max[0, :] < min_max_threshold[0, :]) or np.any(tmp_min_max[1, :] > min_max_threshold[1, :]):
        print("minmax,{}:{}".format(path, tmp_min_max))
        continue

    for i in range(3):
        min_max[0][i] = min(min_max[0][i], tmp_min_max[0][i])
        min_max[1][i] = max(min_max[1][i], tmp_min_max[1][i])
    valid.append(path)

print("Valid {}/{}".format(len(valid), total))
print(min_max)
# print(valid)

for valid_one in valid:
    #path, file_name = os.path.split(valid_one)
    #new_output_folder = path.replace("points", "cropped_points")
    if not os.path.exists("cropped_points"):
        os.makedirs("cropped_points")
    new_output_path = os.path.join("cropped_points", valid_one)
    # print(valid_one)
    #if not os.path.exists(new_output_folder):
    #    os.makedirs(new_output_folder)
    #output_file_name = os.path.join(new_output_folder, file_name)
    valid_arr = np.load(valid_one)
    np.save(new_output_path, valid_arr)
    print("saving ... {}".format(new_output_path))
print("complete saving valid ones !!")
