from gensim.models import Word2Vec

common_texts = []
map = {}
f = open('./data/entity_with_text.txt', 'r')
lines = f.readlines()
for line in lines:
    temp = line.split('\t')
    ent = temp[0]
    temp = temp[1].split()
    common_texts.append(temp)
    map[ent] = temp


model = Word2Vec(sentences=common_texts, vector_size=100, window=5, min_count=1, workers=4)
model.save("word2vec.model")
wv = model.wv

f.close()
del lines
del common_texts
del model

count = 0
rel_base = 237
rel_max = 237
total_append = 0
f = open('./data/train.txt', 'a')
for sig in map: 
    rel = rel_base
    for ent in map:
        if int(sig) >= int(ent):
            continue
        s = wv.n_similarity(map[sig], map[ent])
        if s > 0.975:
            rel += 1
            if rel > rel_max:
                rel_max = rel
            f.write(sig + '\t'+ str(rel) + '\t' + ent + '\n')
            f.write(ent + '\t'+ str(rel) + '\t' + sig + '\n')
    
    count += 1
    total_append += 2*(rel - rel_base)
    print(str(count) + '\t' +'cur: ' + str(rel-rel_base) +'\t' +'total: ' + str(total_append))

print(rel_max)
