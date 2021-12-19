rel_map = {}
f = open('refresh/rel_map.txt', 'r')
lines = f.readlines()
for line in lines:
    temp = line.split()
    rel_map[temp[0]] = temp[1]
f.close()

ent_map = {}
f = open('refresh/ent_certain_map_3.txt', 'r')
lines = f.readlines()
for line in lines:
    temp = line.split()
    ent_map[temp[0]] = temp[1]
f.close()

##########################################
# num = 20466
# f1 = open('data/test.txt' ,'r')
# f2 = open('FB15k-237/test.tsv','r')
# for i in range(20466):
#     line1 = f1.readline()
#     line2 = f2.readline()
#     temp1 = line1.split()
#     temp2 = line2.split()
#     if temp2[0] not in ent_map:
#         ent_map[temp2[0]] = temp1[0]

###################################\

f = open('FB15k-237/train.tsv' ,'r')
f1 = open('data/train.txt' ,'r')
lines = f.readlines()
lines_ta = f1.readlines()

count = 0
for line in lines:
    count += 1
    if(count % 100 == 0):
        print(count)
    temp = line.split()
    if(temp[1] not in rel_map):
        print('error')
        exit(-1)
    if(temp[0] in ent_map and temp[2] in ent_map):
        continue
    if(temp[0] in ent_map):
        ent1 = ent_map[temp[0]]
        rel = rel_map[temp[1]]
        first = True
        for line_ta in lines_ta:
            temp_ta = line_ta.split()
            if(ent1 == temp_ta[0] and rel == temp_ta[1]):
                if(first):
                    ent_map[temp[2]] = temp_ta[2]
                    first = False
                else:
                    ent_map.pop(temp[2])
                    break

    elif(temp[2] in ent_map):
        ent2 = ent_map[temp[2]]
        rel = rel_map[temp[1]]
        first = True
        for line_ta in lines_ta:
            temp_ta = line_ta.split()
            if(ent2 == temp_ta[2] and rel == temp_ta[1]):
                if(first):
                    ent_map[temp[0]] = temp_ta[0]
                    first = False
                else:
                    ent_map.pop(temp[0])
                    break


f = open('./refresh/ent_certain_map_3.txt', 'w')
for key in ent_map:
    f.write(str(key))
    f.write('\t')
    f.write(str(ent_map[key]))
    f.write('\n')