data_path = '../data/DoubanMusic.txt'
train_path = 'train.txt'
dev_path = 'dev.txt'

f = open(data_path, 'r')
lines = f.readlines()
f.close()

ftrain = open(train_path, 'w')
fdev = open(dev_path,'w')

for line in lines:
    temp = line.split()
    ftrain.write(temp[0])
    for pair in temp[1:-1]:
        ftrain.write('\t')
        ftrain.write(pair)
    ftrain.write('\n')
    pair = temp[-1].split(',')
    fdev.write(pair[0])
    fdev.write('\n')
