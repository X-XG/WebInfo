def getUserMap(data_path = '../../data/DoubanMusic.txt'):
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
    return UserMap

def getMusicMap(data_path = '../../data/DoubanMusic.txt'):
    MapMusicID = {}

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
    return MapMusicID
