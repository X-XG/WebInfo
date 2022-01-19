import numpy as np
import cmath


class Matrix_Factorization(object):

    def __init__(self, K=10, alpha=0.05, beta=0.02, epoch=500, regularization=True, random_state=100):

        self.R = None
        self.K = K
        self.P = None
        self.Q = None
        self.r_index = None
        self.r = None
        self.length = None
        self.init_alpha=alpha
        self.alpha = alpha
        self.beta = beta
        self.epoch = epoch
        self.regularization = regularization
        self.random_state = random_state


    def fit(self, R):
        #将矩阵R分解为M*K和K*N

        np.random.seed(self.random_state)
        self.R = R
        M, N = self.R.shape
        #P是M*K的随机矩阵，Q是K*N的随机矩阵
        self.P = np.random.rand(M, self.K)
        self.Q = np.random.rand(N, self.K)

        #r_index是R中不为0的元素的数组下标
        self.r_index = self.R.nonzero()
        #r是R中不为0的元素值
        self.r = self.R[self.r_index[0], self.r_index[1]]
        self.length = len(self.r)


    def _comp_descent(self, index):
        #r中第index个元素
        r_i = self.r_index[0][index]
        r_j = self.r_index[1][index]

        p_i = self.P[r_i]
        q_j = self.Q[r_j]

        r_ij_hat = p_i.dot(q_j)
        e_ij = self.R[r_i, r_j] - r_ij_hat

        #正则化？？？？？？？？？
        if self.regularization == True:
            descent_p_i = -2 * e_ij * q_j + self.beta * p_i
            descent_q_j = -2 * e_ij * p_i + self.beta * q_j
        else:
            descent_p_i = -2 * e_ij * q_j
            descent_q_j = -2 * e_ij * p_i

        return r_i, r_j, p_i, q_j, descent_p_i, descent_q_j


    def _update(self, p_i, q_j, descent_p_i, descent_q_j):

        p_i_new = p_i - self.alpha * descent_p_i
        q_j_new = q_j - self.alpha * descent_q_j

        return p_i_new, q_j_new


    def _estimate_r_hat(self):

        r_hat = self.P.dot(self.Q.T)[self.r_index[0], self.r_index[1]]

        return r_hat


    def start(self):

        epoch_num = 1
        #epoch_cnt = 0
        while epoch_num <= self.epoch:
            for index in range(0, self.length):

                r_i, r_j, p_i, q_j, descent_p_i, descent_q_j = self._comp_descent(index)
                p_i_new, q_j_new = self._update(p_i, q_j, descent_p_i, descent_q_j)

                self.P[r_i] = p_i_new
                self.Q[r_j] = q_j_new

            self.alpha=max(0.01,self.init_alpha*pow(0.98,epoch_num))
            #if epoch_num%10==0:
            #    epoch_cnt+=1
            #    self.alpha=self.init_alpha/cmath.sqrt(epoch_cnt)
            r_hat = self._estimate_r_hat()
            e = r_hat - self.r
            error = e.dot(e)
            #if epoch_num%10==0:
            #    print ('The error is %s=================Epoch:%s' %(error, epoch_num))
            print ('The error is %s=================Epoch:%s' %(error, epoch_num))
            epoch_num += 1

        R_hat = self.P.dot(self.Q.T)
        return R_hat


if __name__ == '__main__':

    read_data_path=".//data//DoubanMusic.txt"
    write_data_path=".//result//"
    f=open(read_data_path,"r")
    lines=f.readlines()
    f.close()

    user_total=23599
    item_total=21602
    sep='\t'
    comma=','

    #R=np.zeros((user_total,item_total),dtype=np.int32)
    R=np.zeros((user_total,item_total))
    for line in lines:
        temp=line.split()
        UserID=int(temp[0])
        pos_cnt=0
        pos_total=0
        music_list=[]
        for pair in temp[1:]:
            pair=pair.split(',')
            MusicID=int(pair[0])
            MusicRating=int(pair[1])
            R[UserID,MusicID]=MusicRating
            if MusicRating>0:
                pos_cnt+=1
                pos_total+=MusicRating
            music_list.append(MusicID)
        if pos_cnt:
            MeanRating=pos_total/pos_cnt
        else:
            MeanRating=2.5
        for musicID in music_list:
            #if R[UserID,musicID]>0:
            #    R[UserID,musicID]-=MeanRating
            #    #########+1
            #    R[UserID,musicID]+=1
            #else:
            #    if R[UserID,musicID]<0:
            #        ########+1
            #        R[UserID,musicID]=MeanRating+1
            if R[UserID,musicID]<0:
                R[UserID,musicID]=(R[UserID,musicID]+1)/5
            if R[UserID,musicID]<0:
                R[UserID,musicID]=(MeanRating+1)/5
    np.save("Rarray",R)

    aa = Matrix_Factorization(K = 5)
    aa.fit(R)
    R_hat=aa.start()

    RatingRank=np.argsort(R_hat)

    with open(write_data_path+"res.txt","w") as f:
        for userID in range(0,user_total):
            output_str=str(userID)+sep
            for music_index in range(item_total-100,item_total):
                output_str+=str(RatingRank[userID][music_index])+comma
            f.write(output_str[:-1]+'\n')
        

    
