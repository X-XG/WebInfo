import os
import json

#for class Doc_Sparse
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from DocSparse import Doc_Sparse as tf_idf_sparse
from word2vec_train import Doc_Sparse as w2v_sparse
from gensim.models import word2vec

import numpy as np
from scipy import sparse
import math

def takeSecond(elem):
        return elem[1]

class Semantic_Search:
    def __init__(self, query_str, max_doc = 10,synonym_tag = False,embedding_type = "tf-idf"):
        self.query_str = query_str
        self.synonym_tag = synonym_tag
        self.embedding_type = embedding_type
        self.max_doc = max_doc

    def read_file(self):
        if self.embedding_type == "tf-idf":
            print("tf-idf")
            postinglist_path = '..\\output\\PostingList.json'
            docmap_path = '..\\output\\docmap.json'
            wordmap_path = '..\\output\\wordmap.json'

            with open(postinglist_path,'r',encoding="utf-8")as fp_postinglist:
                self.PostingList = json.load(fp_postinglist)
                self.word_num = self.PostingList[0]

            with open(docmap_path,'r',encoding="utf-8")as fp_docmap:
                self.DocMap = json.load(fp_docmap)
                self.doc_num = self.DocMap[0]

            with open(wordmap_path,'r',encoding="utf-8")as fp_wordmap:
                self.WordMap = json.load(fp_wordmap)

            temp = sparse.load_npz("..\\output\\TF_IDF.npz")
            self.TF_IDF_array = temp.tolil()
        
        if self.embedding_type == "word2vec":
            print("word2vec")
            model_output_path = "..\\output\\word2vec.model"
            self.model = word2vec.Word2Vec.load(model_output_path)

            docmap_path = '..\\output\\docmap.json'
            doc_word_list_path = '..\\output\\doc_word_list.json'

            with open(docmap_path,'r',encoding="utf-8")as fp_docmap:
                self.DocMap = json.load(fp_docmap)
                self.doc_num = self.DocMap[0]

            with open(doc_word_list_path,'r',encoding="utf-8")as fp_doc_word_list:
                self.doc_word_list = json.load(fp_doc_word_list)

    def sparse_query(self):
        doc_sparse = tf_idf_sparse(self.query_str)
        query_words,self.query_fdist = doc_sparse.sparse()
        self.query_freqs = {}
        for word in query_words:
            self.query_freqs[word] = self.query_fdist.freq(word)
        if self.synonym_tag:
            self.query_words = []
            for word in query_words:
                syn_wordlist = wordnet.synsets(word)
                for syn in syn_wordlist:
                    for lemma in syn.lemmas():
                        syn_word = lemma.name()
                        if(syn_word in self.WordMap):
                            self.query_words.append(syn_word)
                            self.query_freqs[syn_word] = self.query_freqs[word]
            self.query_words += query_words
            self.query_words = list(set(self.query_words))
        else:
            self.query_words = query_words

    def tf_idf_cal(self):
        """calculate the tf-idf vector of the query"""
        """if synonym_tag = True, use synonyms to search"""
        self.TF_IDF = np.zeros(self.word_num + 1)
        for word in self.query_words:
            freq = self.query_freqs[word]
            word_id = self.WordMap[word]
            TF = freq
            IDF = math.log(self.doc_num/(len(self.PostingList[word_id]) + 1))
            self.TF_IDF[word_id] = TF * IDF

    def similarity(self):
        """calculate the similarity between the query vector with each document"""
        self.read_file()
        if self.embedding_type == "tf-idf":
            self.sparse_query()
            self.tf_idf_cal()
            self.doc_similarity =[0]
            for doc_id in range(1, self.doc_num + 1):
                #cos similarity
                array = self.TF_IDF_array.getrow(doc_id).toarray().flatten()
                sim = np.dot(array, self.TF_IDF)/(np.linalg.norm(array) * np.linalg.norm(self.TF_IDF))
                self.doc_similarity.append([doc_id,sim])

        if self.embedding_type == "word2vec":
            query_word_sparse = w2v_sparse(self.query_str)
            query_word = query_word_sparse.sparse()
            self.doc_similarity =[0]
            for doc_id in range(1,self.doc_num + 1):
                doc_word = self.doc_word_list[doc_id - 1]
                sim = self.model.n_similarity(query_word,doc_word)
                self.doc_similarity.append([doc_id,sim])


    def ranking(self):
        """run this runction"""
        """rank the document with similarity"""
        """return top10_doc_name"""
        self.similarity()
        #sort
        self.doc_similarity[1:].sort(key=takeSecond, reverse=True)
        #pick the top10
        top10_doc_name = []
        for i in range(1, min(self.doc_num, self.max_doc + 1)):
            doc_id = self.doc_similarity[i][0]
            top10_doc_name.append(self.DocMap[doc_id])
        return top10_doc_name

#####words query............
if __name__ == '__main__':
    S = Semantic_Search("president high", synonym_tag = False, embedding_type = "tf-idf")
    print(S.ranking())
        
    