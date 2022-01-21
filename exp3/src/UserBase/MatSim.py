import sys
sys.path.append('..')
from utils.getMaps import getUserMap
from utils.JacoobiSim import JaccobiSim
sys.path.append('UserBase')
import numpy as np

UserNum = 23599
data_path = '../../data/DoubanMusic.txt'
output_path = '../../output/'

def MatSimGen(mode = 1):
    UserMap = getUserMap()

    MatSim = np.zeros((UserNum, UserNum))
    
    num = 0
    for User1 in UserMap:
        num += 1
        if num %10 == 0:
            print(num)
        for User2 in UserMap:
            MatSim[User1][User2] = JaccobiSim(UserMap[User1], UserMap[User2], mode)
    np.save('MatJaccobiSim'+str(mode) +'.npy', MatSim)
    
if __name__ == '__main__':
    MatSimGen(mode = 1)
