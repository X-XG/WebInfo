from gensim.models import Word2Vec
import numpy as np
import pickle

def w2vModel(data_base, output_path):
    common_texts = []
    ent_map = {}
    rel_map = {}
    f = open(data_base + 'entity_with_text.txt', 'r')
    lines = f.readlines()
    for line in lines:
        temp = line.split('\t')  
        text = temp[1].split()
        common_texts.append(text)
        ent_map[int(temp[0])] = text
    f.close()

    f = open(data_base + 'relation_with_text.txt', 'r')
    lines = f.readlines()
    for line in lines:
        temp = line.split('\t')  
        text = temp[1].split()
        common_texts.append(text)
        rel_map[int(temp[0])] = text
    f.close()

    model = Word2Vec(sentences=common_texts, vector_size=100, window=5, min_count=1, workers=4)
    model.save(output_path + "word2vec.model")

    with open(output_path + 'ent_map_text'+ '.pkl', 'wb') as f:
        pickle.dump(ent_map, f)
    
    with open(output_path +'rel_map_text'+ '.pkl', 'wb') as f:
        pickle.dump(rel_map, f)


def ent_rel_sim(ent_num, rel_num, output_path):
    model = Word2Vec.load(output_path + "word2vec.model")
    with open(output_path + 'ent_map_text' + '.pkl', 'rb') as f:
        ent_map = pickle.load(f)
    with open(output_path + 'rel_map_text' + '.pkl', 'rb') as f:
        rel_map = pickle.load(f)

    ent_rel_sim = np.zeros((ent_num, rel_num))
    for i in range(ent_num):
        if i % 100 == 0:
            print(i)
        if i not in ent_map:
            continue
        for j in range(rel_num):
            ent_rel_sim[i][j] = model.wv.n_similarity(ent_map[i], rel_map[j])
    
    np.save(output_path + 'ent_rel_sim.npy', ent_rel_sim)
    
if __name__  == '__main__':
    w2vModel('../data/', './output/')
    ent_rel_sim(14541, 237, './output/')