import numpy as np
if __name__ == '__main__':

    user_total=23599
    item_total=21602
    sep='\t'
    comma=','
    
    read_data_path=".//data//"
    f=open(read_data_path+"DoubanMusic.txt","r")
    lines=f.readlines()
    f.close()

    followMap=[]
    Rating=np.zeros((user_total,item_total),dtype="int32")
    for line in lines:
        temp=line.split()
        UserID=int(temp[0])
        for pair in temp[1:]:
            pair=pair.split(',')
            MusicID=int(pair[0])
            MusicRating=int(pair[1])
            Rating[UserID,MusicID]=1
        followMap.append([])

    f=open(read_data_path+"DoubanSocial.txt","r")
    lines=f.readlines()
    f.close()

    for line in lines:
        temp=line.split()
        UserID=int(temp[0])
        followID=int(temp[1])
        followMap[UserID].append(followID)

    for UserID in range(0,user_total): 
        outputstr="" 
        for ItemID in range(0,item_total):
            if Rating[UserID][ItemID]==0:
                for followID in followMap[UserID]:
                    if Rating[followID][ItemID]>0:
                        Rating[UserID][ItemID]=1
                        break

    np.save('Rating',Rating)