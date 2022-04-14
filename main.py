import math
import os.path
import time


def get_size(start_path):
    if os.path.isfile(start_path):
        return os.path.getsize(start_path)
    total_size = 0
    for directory_path, directory_names, filenames in os.walk(start_path):
        print("Scanning: " + str(directory_path))
        try:
            for f in filenames:
                fp = os.path.join(directory_path, f)
                # skip if link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        except:
            pass

    return total_size


def create_hash(path):
    hashmap = {}
    for item in os.listdir(path):
        hashmap[item] = get_size(os.path.join(path, item))

    return hashmap


def sort_hash(hashmap):
    sorted_hashmap = {key: value for key, value in sorted(
        hashmap.items(), key=lambda value: value[1],
        reverse=True)}

    return sorted_hashmap


def convert_size(hashmap):
    for key, value in hashmap.items():
        if hashmap[key] == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(hashmap[key], 1024)))
        p = math.pow(1024, i)
        s = round(hashmap[key] / p, 2)
        hashmap[key] = "%s %s" % (s, size_name[i])
    return hashmap


def print_hash(hashmap):
    print("----------\nSorted file structure: \n----------")
    for key, value in hashmap.items():
        print("{}: {}\n".format(key, value))


def print_time(time_total):
    print("Operation completed in: ")
    if round(time_total) == 1:
        print("1 second")
    elif time_total <= 60:
        print(int(round(time_total)), " seconds")
    elif 60 < time_total <= 3600:
        time_minutes = divmod(time_total, 60)
        print(int(time_minutes[0]), " minutes ", int(round(time_minutes[1])), " seconds")
    elif time_total > 3600:
        time_hours = divmod(time_total, 3600)
        time_minutes = divmod(time_hours[1], 60)
        print(int(time_hours[0]), " hours ", int(time_minutes[0]), " minutes ", int(round(time_minutes[1])), " seconds")


def write_file(hashmap, path, time_total):
    with open(path + '\\Drive Scan.txt', 'w') as f:
        f.write("Scan for " + str(path) + "\n \n")
        for key, value in hashmap.items():
            f.write("{}: {}\n\n".format(key, value))
        f.write("Operation completed in " + str(time_total) + " seconds")
        f.close()


def main():
    path = input("Enter root folder: ")

    time_start = time.time()

    # create hashmap
    item_name_size = create_hash(path)
    # sort hash map
    sorted_value = sort_hash(item_name_size)
    # convert values
    convert_size(sorted_value)
    # print hash map
    print_hash(sorted_value)
    # end timer and print total time
    time_end = time.time()
    time_total = time_end - time_start
    print_time(time_total)

    # write file
    write_user_pref = input("Write file? (y/n)")

    if write_user_pref.casefold() == "y":
        write_file(sorted_value, path, time_total)
        print("File written to: " + str(path))
    else:
        pass


if __name__ == '__main__':
    main()
