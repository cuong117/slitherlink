from pprint import pprint

maps5 = []
maps7 = []
maps10 = []
maps15 = []
maps20 = []
maps30 = []

file = open('map/puzzle.txt')
cur_map_size = 0
cur_map = []
for line in file:
    line = line.strip()
    if len(line) <= 2 and line:
        cur_map_size = int(line)
        cur_map = []
    elif not len(line):
        if cur_map_size == 5:
            maps5.append(cur_map)
        elif cur_map_size == 7:
            maps7.append(cur_map)
        elif cur_map_size == 10:
            maps10.append(cur_map)
        elif cur_map_size == 15:
            maps15.append(cur_map)
        elif cur_map_size == 20:
            maps20.append(cur_map)
        elif cur_map_size == 30:
            maps30.append(cur_map)
        cur_map = []
    else:
        line = line.split()
        length = len(line)
        for i in range(length):
            line[i] = int(line[i])
        cur_map.append(line)

file.close()
# count = 0
# for mapi in maps30:
#     for m in mapi:
#         count += 1
#         if len(m) != 30:
#             print(count, False, "--------------------", end="\t")
#         else:
#             print(count, True, end='\t')
#     count = 0
#     print()

