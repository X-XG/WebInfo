from math import sqrt
import numpy as np

MusicNum = 21602
MIN_NUM = -30000
data_path = '../../data/DoubanMusic.txt'
output_path = '../../output/'


def JaccardSim(list1:list, list2:list, mode = 1):
    intersection = len(set(list1).intersection(set(list2)))
    union = len(list1) + len(list2) - intersection
    if mode == 0:
        return intersection
    elif mode == 0.5:
        return intersection/sqrt(union)
    elif mode == 1:
        return intersection/union
    else:
        exit(-1)

def MatSimGen(mode = 1):
    MapMusicID = {}
    MatSim = np.zeros((MusicNum, MusicNum))

    f = open(data_path, 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        temp = line.split()
        UserID = int(temp[0])
        for pair in temp[1:]:
            MusicID = int(pair.split(',')[0])
            if MusicID not in MapMusicID:
                MapMusicID[MusicID] = [UserID]
            else:
                MapMusicID[MusicID].append(UserID)
    
    num = 0
    for Music1 in MapMusicID:
        num += 1
        if num %10 == 0:
            print(num)
        for Music2 in MapMusicID:
            MatSim[Music1][Music2] = JaccardSim(MapMusicID[Music1], MapMusicID[Music2], mode)
    np.save('MatJaccardSim'+str(mode) +'.npy', MatSim)
    
def MatDiagMinimize():
    MatSim = np.load('MatJaccardSim.npy')
    for i in range(MusicNum):
        MatSim[i][i] = MIN_NUM
    np.save('MatJaccardSim_DiagMinimized.npy', MatSim)
    
if __name__ == '__main__':
    # MatDiagMinimize()
    MatSimGen(mode = 1)
