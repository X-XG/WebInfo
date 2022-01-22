import numpy as np

MatSimPath = 'MatJaccardSim1.npy'
data_path = '../../data/DoubanMusic.txt'
result_path = 'MusicBaseMode1.txt'
MusicNum = 21602

def main(CarryOn = False):
    MatSim = np.load(MatSimPath)
    UserMap = {}

    f = open(data_path, 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        temp = line.split()
        UserID = int(temp[0])
        for pair in temp[1:]:
            MusicID = int(pair.split(',')[0])
            if UserID not in UserMap:
                UserMap[UserID] = [MusicID]
            else:
                UserMap[UserID].append(MusicID)

    if CarryOn:
        f = open(result_path, 'r')
        count = len(f.readlines())
        f.close()
        f = open(result_path, 'a')
    else:
        f = open(result_path, 'w')
        count = 0

    for UserID in UserMap:
        if UserID < count:
            continue
        predict_list = []
        for MusicID in range(MusicNum):
            if MusicID in UserMap[UserID]:
                continue
            predict = 0
            for UserMusic in UserMap[UserID]:
                predict += MatSim[UserMusic][MusicID]
            predict_list.append((predict,MusicID))
        predict_list.sort(reverse=True)
        f.write(str(UserID))
        f.write('\t')
        f.write(str(predict_list[0][1]))
        for i in range(1,100):
            f.write(',')
            f.write(str(predict_list[i][1]))
        f.write('\n')
        count += 1
        if count % 1 == 0:
            print(count)

if __name__ == '__main__':
    main(CarryOn=False)
