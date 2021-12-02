import numpy as np
import codecs
import operator
import json
from transE import data_loader

def dataloader(entity_file,relation_file,test_file):
    # entity_file: entity \t embedding
    entity_dict = {}
    relation_dict = {}
    test_triple = []

    with codecs.open(entity_file) as e_f:
        lines = e_f.readlines()
        for line in lines:
            entity,embedding = line.strip().split('\t')
            embedding = json.loads(embedding)
            entity_dict[entity] = embedding

    with codecs.open(relation_file) as r_f:
        lines = r_f.readlines()
        for line in lines:
            relation,embedding = line.strip().split('\t')
            embedding = json.loads(embedding)
            relation_dict[relation] = embedding

    with codecs.open(test_file) as t_f:
        lines = t_f.readlines()
        for line in lines:
            triple = line.strip().split('\t')
            if len(triple) != 3:
                continue
            h_ = triple[0]
            t_ = triple[1]
            r_ = triple[2]

            test_triple.append(tuple((h_,t_,r_)))

    return entity_dict,relation_dict,test_triple

def distance(h,r,t):
    h = np.array(h)
    r=np.array(r)
    t = np.array(t)
    s=h+r-t
    return np.linalg.norm(s)

class Test:
    def __init__(self,entity_dict,relation_dict,test_triple,train_triple,isFit = True):
        self.entity_dict = entity_dict
        self.relation_dict = relation_dict
        self.test_triple = test_triple
        self.train_triple = train_triple
        self.isFit = isFit

        self.hits5 = 0
        self.mean_rank = 0

    def rank(self, output_path):
        hits = 0
        step = 1
        f = open(output_path + 'tail_predict.txt', 'w')

        for triple in self.test_triple:
            rank_tail_dict = {}

            for entity in self.entity_dict.keys():
                corrupted_tail = [triple[0],entity,triple[2]]
                # if self.isFit:
                    # if corrupted_tail not in self.train_triple:
                        # h_emb = self.entity_dict[corrupted_tail[0]]
                        # r_emb = self.relation_dict[corrupted_tail[2]]
                        # t_emb = self.entity_dict[corrupted_tail[1]]
                        # rank_tail_dict[tuple(corrupted_tail)] = distance(h_emb, r_emb, t_emb)
                # else:
                h_emb = self.entity_dict[corrupted_tail[0]]
                r_emb = self.relation_dict[corrupted_tail[2]]
                t_emb = self.entity_dict[corrupted_tail[1]]
                rank_tail_dict[tuple(corrupted_tail)] = distance(h_emb, r_emb, t_emb)

            rank_tail_sorted = sorted(rank_tail_dict.items(),key = operator.itemgetter(1))

            #hits
            first_hit = True
            count = 0
            for i in range(10):
                if(self.isFit):
                    if rank_tail_sorted[i][0] in self.train_triple:
                        continue
                count += 1
                if count < 5:
                    f.write(rank_tail_sorted[i][0][1])
                    f.write(',')
                else:      
                    f.write(rank_tail_sorted[i][0][1])
                    f.write('\n')
                    break
                if first_hit and triple[1] == rank_tail_sorted[i][0][1]:
                    hits += 1
                    first_hit = False

            step += 1
            if step % 10 == 0:
                print("step ", step, ", hits ",hits, ', rate: ',hits/step)
                print()

        self.hits5 = hits / (2*len(self.test_triple))


if __name__ == '__main__':
    _, _, train_triple = data_loader("./data/",14541, 237)

    entity_dict, relation_dict, test_triple = \
        dataloader("./output/entity_embedding","./output/relation_embedding",
                   "data/test.txt")


    test = Test(entity_dict,relation_dict,test_triple,train_triple,isFit=True)
    test.rank('./output/')
    print("entity hits@5: ", test.hits5)


