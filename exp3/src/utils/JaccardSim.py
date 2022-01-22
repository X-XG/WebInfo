from math import sqrt

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