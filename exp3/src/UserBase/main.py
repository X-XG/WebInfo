import sys
sys.path.append('..')
from utils.getMaps import getUserMap, getMusicMap
sys.path.append('UserBase')
import numpy as np

MatSimPath = 'MatJaccardSim1.npy'
data_path = '../../data/DoubanMusic.txt'
result_path = 'UserBaseMode1.txt'
MusicNum = 21602
UserNum = 23599

def main(CarryOn = False):
    MatSim = np.load(MatSimPath)

    UserMap = getUserMap()

    MusicMap = getMusicMap()

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
            for OtherUser in MusicMap[MusicID]:
                predict += MatSim[UserID][OtherUser]
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
    main(CarryOn=True)
