import os

train_ratio = 0.7
val_ratio = 0.15
test_ratio =0.15


def empty_label_check(directory_path, verbose=False):
    """
    Returns:
        empty_file_names=['009994.txt', '009199.txt',
        '010044.txt', '009226.txt', '010784.txt',
        '009228.txt', '010843.txt', '010443.txt',
        '003150.txt', '003104.txt', '008256.txt']
    """
    # List to store files with no entries
    empty_files = []

    # Iterate through all the files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Only check .txt files
            file_path = os.path.join(directory_path, filename)
            # print(file_path)
            with open(file_path, "r") as file:
                # Check if the file has no lines or only empty lines
                if not any(line.strip() for line in file):
                    empty_files.append(filename)

    # Print the list of empty files
    if empty_files:
        if verbose:
            print("Files with no entries: {}".format(empty_files))
            # for empty_file in empty_files:
            #     print(empty_file)
            print(
                "Files with no entries counts: {} / total {}".format(
                    len(empty_files), len(os.listdir(directory_path))
                )
            )
        else:
            print(
                "Files with no entries counts: {} / total {}".format(
                    len(empty_files), len(os.listdir(directory_path))
                )
            )
    else:
        print("No empty files found.")

    return empty_files

def get_only_numbers(data_list):
    number_list = [os.path.splitext(filename)[0] for filename in data_list]
    return number_list

if __name__ == "__main__":
    
    total_valid_ones = os.listdir("points")
    total_num = len(total_valid_ones)
    train_end = int(total_num * train_ratio)
    val_end = train_end + int(total_num * val_ratio)

    # split
    train_list = total_valid_ones[:train_end]
    valid_list = total_valid_ones[train_end:val_end]
    test_list = total_valid_ones[val_end:]

    train_set_numbers = get_only_numbers(train_list)
    valid_set_numbers = get_only_numbers(valid_list)
    test_set_numbers = get_only_numbers(test_list)

    train_set = set(train_set_numbers)
    val_set = set(valid_set_numbers)
    test_set = set(test_set_numbers)

    # ----------------------------------
    label_path = "labels"
    # labels = os.listdir(label_path)
    empty_files = empty_label_check(label_path)
    empty_file_numbers = []
    if empty_files:
        # only extract 6 digit numbers
        empty_file_numbers = [os.path.splitext(filename)[0] for filename in empty_files]
        print("empty {}".format(len(empty_file_numbers)))
    # ----------------------------------
    
    if len(empty_file_numbers):
        train_set = train_set - set(empty_file_numbers)
        val_set = val_set - set(empty_file_numbers)
        test_set = test_set - set(empty_file_numbers)

    # make it back to list
    train_set_numbers = list(train_set)
    valid_set_numbers = list(val_set)
    test_set_numbers = list(test_set)

    print("train {}".format(len(train_set_numbers)))
    print("val {}".format(len(valid_set_numbers)))
    print("tes {}".format(len(test_set_numbers)))

    output_dir = "ImageSetsCrop"
    # Save to text files
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "train.txt"), "w") as train_file:
        train_file.write("\n".join(train_set_numbers) + "\n")
    with open(os.path.join(output_dir, "val.txt"), "w") as val_file:
        val_file.write("\n".join(valid_set_numbers) + "\n")
    with open(os.path.join(output_dir, "test.txt"), "w") as test_file:
        test_file.write("\n".join(test_set_numbers) + "\n")

    print("new ImageSets as per Crop genrated...")
