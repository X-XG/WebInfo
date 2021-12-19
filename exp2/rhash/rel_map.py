rel_map = {}

freq_origin = {}

f_train_origin = open('FB15k-237/train.tsv' ,'r')
lines = f_train_origin.readlines()
for line in lines:
    temp = line.split()
    word = temp[1]
    if word not in freq_origin:
        freq_origin[word] = [1,0,0]
    else:
        freq_origin[word][0] += 1

f_dev_origin = open('FB15k-237/dev.tsv' ,'r')
lines = f_dev_origin.readlines()
for line in lines:
    temp = line.split()
    word = temp[1]
    if word not in freq_origin:
        print('error')
    else:
        freq_origin[word][1] += 1

f_test_origin = open('FB15k-237/test.tsv' ,'r')
lines = f_test_origin.readlines()
for line in lines:
    temp = line.split()
    word = temp[1]
    if word not in freq_origin:
        print('error')
    else:
        freq_origin[word][2] += 1


freq_ta = {}

f_train_ta = open('data/train.txt' ,'r')
lines = f_train_ta.readlines()
for line in lines:
    temp = line.split()
    word = temp[1]
    if word not in freq_ta:
        freq_ta[word] = [1,0,0]
    else:
        freq_ta[word][0] += 1

f_dev_ta = open('data/dev.txt' ,'r')
lines = f_dev_ta.readlines()
for line in lines:
    temp = line.split()
    word = temp[1]
    if word not in freq_ta:
        print('error')
    else:
        freq_ta[word][1] += 1

f_test_ta = open('data/test.txt' ,'r')
lines = f_test_ta.readlines()
for line in lines:
    temp = line.split()
    word = temp[1]
    if word not in freq_ta:
        print('error')
    else:
        freq_ta[word][2] += 1

for word in freq_origin:
    freq_word = freq_origin[word]
    first = True
    for id in freq_ta:
        freq_id = freq_ta[id]
        if(freq_word[0] == freq_id[0] and freq_word[1] == freq_id[1] and freq_word[2] == freq_id[2]):
            if(first):
                rel_map[word] = id
                first = False
            else:
                print('error')
                exit('0')


f = open('./refresh/rel_map2.txt', 'w')
for key in rel_map:
    f.write(str(key))
    f.write('\t')
    f.write(str(rel_map[key]))
    f.write('\n')


 