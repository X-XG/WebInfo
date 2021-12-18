import json
trans2res_idmap={}
entity_dict={}
entity_id = 0
entities = ['0']
with open(".//benchmarks//ljy//entity_with_text.txt", "r") as f_read:
    for line in f_read.readlines():
        entity = line.split()
        entity_dict[entity[0]]=entity_id
        trans2res_idmap[entity_id]=entity[0]
        entities.append(str(entity[0]))
        entities.append("\t")
        entities.append(str(entity_id))
        entities.append("\n")
        entity_id +=1



relation_dict={}
relation_id = 0
relations = ['0']
with open(".//benchmarks//ljy//relation_with_text.txt", "r") as f_read:
    for line in f_read.readlines():
        relation = line.split()
        relation_dict[relation[0]]=relation_id
        relations.append(str(relation[0]))
        relations.append("\t")
        relations.append(str(relation_id))
        relations.append("\n")
        relation_id +=1



l = ['0']
f_write = open(".//benchmarks//ljy//train2id.txt", 'w')
train_id = 0
with open(".//benchmarks//ljy//train.txt", "r") as f_read:
    for line in f_read.readlines():
        line = line.split()
        if line[0] in entity_dict:
            l.append(str(entity_dict[line[0]]))
        else:
            entity_dict[line[0]] = entity_id
            trans2res_idmap[entity_id]=line[0]
            entities.append(str(line[0]))
            entities.append("\t")
            entities.append(str(entity_id))
            entities.append("\n")
            l.append(str(entity_dict[line[0]]))
            entity_id +=1
        l.append(' ')
        if line[2] in entity_dict:
            l.append(str(entity_dict[line[2]]))
        else:
            entity_dict[line[2]] = entity_id
            trans2res_idmap[entity_id]=line[2]
            entities.append(str(line[2]))
            entities.append("\t")
            entities.append(str(entity_id))
            entities.append("\n")
            l.append(str(entity_dict[line[2]]))
            entity_id +=1
        l.append(' ')
        if line[1] in relation_dict:
            l.append(str(relation_dict[line[1]]))
        else:
            relation_dict[line[1]] =relation_id
            relations.append(str(line[1]))
            relations.append("\t")
            relations.append(str(relation_id))
            relations.append("\n")
            l.append(str(relation_dict[line[1]]))
            relation_id +=1
        l.append('\n')
        train_id +=1
l[0] = str(train_id) + '\n'
f_write.writelines(l)
f_write.close()

f_write = open(".//benchmarks//ljy//valid2id.txt", 'w')
l = ['0']
dev_id = 0
with open(".//benchmarks//ljy//dev.txt", "r") as f_read:
    for line in f_read.readlines():
        line = line.split()
        if line[0] in entity_dict:
            l.append(str(entity_dict[line[0]]))
        else:
            entity_dict[line[0]] = entity_id
            trans2res_idmap[entity_id]=line[0]
            entities.append(str(line[0]))
            entities.append("\t")
            entities.append(str(entity_id))
            entities.append("\n")
            l.append(str(entity_dict[line[0]]))
            entity_id +=1
        l.append(' ')
        if line[2] in entity_dict:
            l.append(str(entity_dict[line[2]]))
        else:
            entity_dict[line[2]] = entity_id
            trans2res_idmap[entity_id]=line[2]
            entities.append(str(line[2]))
            entities.append("\t")
            entities.append(str(entity_id))
            entities.append("\n")
            l.append(str(entity_dict[line[2]]))
            entity_id +=1
        l.append(' ')
        if line[1] in relation_dict:
            l.append(str(relation_dict[line[1]]))
        else:
            relation_dict[line[1]] =relation_id
            relations.append(str(line[1]))
            relations.append("\t")
            relations.append(str(relation_id))
            relations.append("\n")
            l.append(str(relation_dict[line[1]]))
            relation_id +=1
        l.append('\n')
        dev_id +=1
l[0] = str(dev_id) + '\n'
f_write.writelines(l)
f_write.close()

f_write = open(".//benchmarks//ljy//test2id.txt", 'w')
l = ['0']
test_id = 0
with open(".//benchmarks//ljy//test.txt", "r") as f_read:
    for line in f_read.readlines():
        line = line.split()
        if line[0] in entity_dict:
            l.append(str(entity_dict[line[0]]))
        else:
            entity_dict[line[0]] = entity_id
            trans2res_idmap[entity_id]=line[0]
            entities.append(str(line[0]))
            entities.append("\t")
            entities.append(str(entity_id))
            entities.append("\n")
            l.append(str(entity_dict[line[0]]))
            entity_id +=1
        l.append(' ')
        if line[1] in entity_dict:
            l.append(str(entity_dict[line[1]]))
        else:
            entity_dict[line[1]] = entity_id
            trans2res_idmap[entity_id]=line[1]
            entities.append(str(line[1]))
            entities.append("\t")
            entities.append(str(entity_id))
            entities.append("\n")
            l.append(str(entity_dict[line[1]]))
            entity_id +=1
        l.append(' ')
        if line[2] in relation_dict:
            l.append(str(relation_dict[line[2]]))
        else:
            relation_dict[line[2]] =relation_id
            relations.append(str(line[2]))
            relations.append("\t")
            relations.append(str(relation_id))
            relations.append("\n")
            l.append(str(relation_dict[line[2]]))
            relation_id +=1
        l.append('\n')
        test_id +=1
l[0] = str(test_id) + '\n'
f_write.writelines(l)
f_write.close()

f_write = open(".//benchmarks//ljy//entity2id.txt", 'w')
entities[0] = str(entity_id) +'\n'
f_write.writelines(entities)
f_write.close()

f_write = open(".//benchmarks//ljy//relation2id.txt", 'w')
relations[0] = str(relation_id) +'\n'
f_write.writelines(relations)
f_write.close()

jsonMap = json.dumps(trans2res_idmap)
fileObject = open('.//result//map.json','w')
fileObject.write(jsonMap)
fileObject.close()
