ent_map = {}

freq_origin = {}

f_train_origin = open('FB15k-237/train.tsv' ,'r')
lines = f_train_origin.readlines()
for line in lines:
    temp = line.split()
    word = temp[0]
    if word not in freq_origin:
        freq_origin[word] = [1,0,0,0,0]
    else:
        freq_origin[word][0] += 1
    word = temp[2]
    if word not in freq_origin:
        freq_origin[word] = [0,1,0,0,0]
    else:
        freq_origin[word][1] += 1
    

f_dev_origin = open('FB15k-237/dev.tsv' ,'r')
lines = f_dev_origin.readlines()
for line in lines:
    temp = line.split()
    word = temp[0]
    if word not in freq_origin:
        freq_origin[word] = [0,0,1,0,0]
    else:
        freq_origin[word][2] += 1
    word = temp[2]
    if word not in freq_origin:
        freq_origin[word] = [0,0,0,1,0]
    else:
        freq_origin[word][3] += 1
        

f_test_origin = open('FB15k-237/test.tsv' ,'r')
lines = f_test_origin.readlines()
for line in lines:
    temp = line.split()
    word = temp[0]
    if word not in freq_origin:
        freq_origin[word] = [0,0,0,0,1]
    else:
        freq_origin[word][4] += 1
    word = temp[2]


freq_ta = {}

f_train_ta = open('data/train.txt' ,'r')
lines = f_train_ta.readlines()
for line in lines:
    temp = line.split()
    word = temp[0]
    if word not in freq_ta:
        freq_ta[word] = [1,0,0,0,0]
    else:
        freq_ta[word][0] += 1
    word = temp[2]
    if word not in freq_ta:
        freq_ta[word] = [0,1,0,0,0]
    else:
        freq_ta[word][1] += 1
    

f_dev_ta = open('data/dev.txt' ,'r')
lines = f_dev_ta.readlines()
for line in lines:
    temp = line.split()
    word = temp[0]
    if word not in freq_ta:
        freq_ta[word] = [0,0,1,0,0]
    else:
        freq_ta[word][2] += 1
    word = temp[2]
    if word not in freq_ta:
        freq_ta[word] = [0,0,0,1,0]
    else:
        freq_ta[word][3] += 1
        

f_test_ta = open('data/test.txt' ,'r')
lines = f_test_ta.readlines()
for line in lines:
    temp = line.split()
    word = temp[0]
    if word not in freq_ta:
        freq_ta[word] = [0,0,0,0,1]
    else:
        freq_ta[word][4] += 1

count = 0

for word in freq_origin:
    freq_word = freq_origin[word]
    first = True
    for id in freq_ta:
        freq_id = freq_ta[id]
        if (freq_word[0] == freq_id[0] and freq_word[1] == freq_id[1] and freq_word[2] == freq_id[2] \
        and freq_word[3] == freq_id[3] and freq_word[4] == freq_id[4]):
            if(first):
                ent_map[word] = id
                first = False
                count += 1
            else:
                # ent_map[word].append(id)
                ent_map.pop(word)
                count -= 1
                break


f = open('./refresh/ent_map.txt', 'w')
for key in ent_map:
    f.write(str(key))
    f.write('\t')
    f.write(str(ent_map[key]))
    f.write('\n')

print(count)