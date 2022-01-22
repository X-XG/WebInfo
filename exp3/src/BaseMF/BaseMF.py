import numpy as np
import cmath 

class Matrix_Factorization(object):

    def __init__(self, K=10, alpha=0.01, beta=0.1, epoch=1, regularization=True, random_state=100):

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
        #print("r_index[0]",self.r_index[0].shape,"r_index[1]:",self.r_index[1].shape)
        #r是R中不为0的元素值
        self.r = self.R[self.r_index[0], self.r_index[1]]
        #print("r:",self.r.shape)
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

            self.alpha=max(0.01,self.init_alpha*pow(0.85,epoch_num))
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
            if error<1:
                break

        R_hat = self.P.dot(self.Q.T)

        return R_hat,self.P,self.Q


if __name__ == '__main__':

    user_total=23599
    item_total=21602
    sep='\t'
    comma=','
    

    f=open(".//data//DoubanMusic.txt","r")
    #read_data_path=".//data//"
    write_data_path=".//result//"
    #f=open(read_data_path+"DoubanMusic.txt","r")
    lines=f.readlines()
    f.close()

    followMap=[]
    Rating=np.zeros((user_total,item_total))
    for line in lines:
        temp=line.split()
        UserID=int(temp[0])
        for pair in temp[1:]:
            pair=pair.split(',')
            MusicID=int(pair[0])
            MusicRating=int(pair[1])
            Rating[UserID,MusicID]=1
        
    aa = Matrix_Factorization(K = 20)
    aa.fit(Rating)
    R_hat,P,Q=aa.start()

    np.save('Rating',Rating)
    np.save('P',P)
    np.save('Q',Q)