import config
from models import *
import json
import os 
con = config.Config()
con.set_use_gpu(True)
#Input training files from benchmarks/FB15K/ folder.
con.set_in_path("./benchmarks/ljy/")
#True: Input test files from the same folder.
con.set_result_dir("./result")
con.init()
con.set_test_model(TransE)
h = []
r = []
k = 5
l = []
with open(".//benchmarks//ljy//test2id.txt","r") as f_read:
    NotFirst = False
    for line in f_read.readlines():
        line = line.split()
        if NotFirst:    
            h.append(int(line[0]))
            r.append(int(line[2]))
        NotFirst = True
tail_predict_list = con.predict_tail(h,r,k)

with open(".//result//map.json",'r') as f_map:
    json_map=json.load(f_map)
    for tail5 in tail_predict_list:
        flag = False
        print(tail5)
        for t in tail5:
            if flag:
                l.append(',')
            flag = True
            l.append(json_map[str(t)])
        l.append("\n")
f_write = open(".//result//res.txt","w")
f_write.writelines(l)
f_write.close()

