def exchange(data_path):
    f = open(data_path, 'r')
    lines = f.readlines()
    f.close()
    f = open(data_path, 'w')
    for line in lines:
        temp = line.split()
        f.write(temp[0])
        f.write('\t')
        f.write(temp[2])
        f.write('\t')
        f.write(temp[1])
        f.write('\n')
    f.close()

def data2id(num, data_path):
    f = open(data_path, 'w')
    for i in range(0, num):
        f.write(str(i))
        f.write('\t')
        f.write(str(i))
        f.write('\n')
    f.close()

if __name__ == '__main__':
    base_path = './data/'
    ent_num = 14541
    rel_num = 237

    try:
        import os
        import shutil
        if not os.path.exists('./data/'):
            shutil.copytree('../data/', './data/')
    except:
        print('error in data gen')

    train_path = base_path + 'train.txt'
    dev_path = base_path + 'dev.txt'
    test_path = base_path + 'test.txt'
    exchange(train_path)
    exchange(dev_path)
    exchange(test_path)

    entity2id_path = base_path + 'entity2id.txt'
    relation2id_path = base_path + 'relation2id.txt'
    data2id(ent_num, entity2id_path)
    data2id(rel_num, relation2id_path)

