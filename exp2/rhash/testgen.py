ent_map = {}
f = open('refresh/ent_certain_map_3.txt', 'r')
lines = f.readlines()
for line in lines:
    temp = line.split()
    ent_map[temp[0]] = temp[1]
f.close()

ent_map_weak = {}
f = open('refresh/ent_map.txt', 'r')
lines = f.readlines()
for line in lines:
    temp = line.split()
    ent_map_weak[temp[0]] = temp[1]
f.close()

for ent in ent_map_weak:
    if ent not in ent_map:
        ent_map[ent] = ent_map_weak[ent]

error = 0
num = 20466
f1 = open('../data/test.txt' ,'r')
f2 = open('FB15k-237/test.tsv','r')
f = open('refresh/inverse_hash.txt', 'w')
for i in range(20466):
    line1 = f1.readline()
    line2 = f2.readline()
    temp1 = line1.split()
    temp2 = line2.split()
    # f.write(temp1[0])
    # f.write('\t')
    
    # f.write(temp1[1])
    # f.write('\t')

    if temp2[2] not in ent_map:
        pred = '1'
        error+=1
    else:
        pred = (ent_map[temp2[2]])
    
    f.write(pred)
    for i in range(4):
        f.write(',')
        f.write(pred)
    f.write('\n')

print(error)
    
