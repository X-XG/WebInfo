import numpy as np

MusicNum = 21602
MIN_NUM = -30000
data_path = '../../data/DoubanMusic.txt'
output_path = '../../output/'


def JaccobiSim(list1:list, list2:list):
    intersection = len(set(list1).intersection(set(list2)))
    union = len(list1) + len(list2) - intersection
    return intersection/union
    # intersection = 0
    # i = 0
    # j = 0
    # while i < len(list1) and j < len(list2):
    #     if list1[i] == list2[j]:
    #         intersection += 1
    #         i += 1
    #         j += 1
    #     elif list1[i] < list2[j]:
    #         i += 1
    #     else:
    #         j += 1
    # union = len(list1) + len(list2) - intersection
    # return intersection/union

def MatSimGen():
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
            MatSim[Music1][Music2] = JaccobiSim(MapMusicID[Music1], MapMusicID[Music2])
    np.save('MatJaccobiSim.npy', MatSim)
    
def MatDiagMinimize():
    MatSim = np.load('MatJaccobiSim.npy')
    for i in range(MusicNum):
        MatSim[i][i] = MIN_NUM
    np.save('MatJaccobiSim_DiagMinimized.npy', MatSim)
    
if __name__ == '__main__':
    MatDiagMinimize()
    # MatSimGen()


