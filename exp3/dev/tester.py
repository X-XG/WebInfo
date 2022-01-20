dev_path = 'dev.txt'
result_path = ''
UserNum = 23599

dev_list = []
f = open(dev_path)
lines = f.readlines()
f.close()
for dev in lines:
    dev_list.append(int(dev))

f = open(result_path)
lines = f.readlines()
f.close()

hit100 = 0
hit20 = 0
i = 0

for line in lines:
    pred_list = []
    pred_20_list = []
    temp = line.split()[1].split(',')
    for music in temp:
        pred_list.append(int(music))
    for music in temp[0:20]:
        pred_20_list.append(int(music))
    if dev_list[i] in pred_list:
        hit100 += 1
    if dev_list[i] in pred_20_list:
        hit20 += 1
    i += 1

print('hit@20 = ' + str(hit20/UserNum))
print('hit@100 = ' + str(hit100/UserNum))
