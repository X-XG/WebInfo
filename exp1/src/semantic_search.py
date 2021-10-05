import os
import json

#for class Doc_Sparse
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from DocSparse import Doc_Sparse

import numpy as np
import math

def takeSecond(elem):
        return elem[1]

class Semantic_Search:
    def __init__(self, query_str):
        self.query_str = query_str

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
        
        self.TF_IDF_array = np.load("..\\output\\TF_IDF.npy")

    def sparse_query(self):
        doc_sparse = Doc_Sparse(self.query_str)
        self.query_words,self.query_fdist = doc_sparse.sparse()

    def tf_idf_cal(self):
        """calculate the tf-idf vector of the query"""
        self.TF_IDF = np.zeros(self.word_num + 1)
        for word in self.query_words:
            freq = self.query_fdist.freq(word)
            word_id = self.WordMap[word]
            TF = freq
            IDF = math.log(self.doc_num/(len(self.PostingList[word_id]) + 1))
            self.TF_IDF[word_id] = TF * IDF

    def similarity(self):
        """calculate the similarity between the query vector with each document"""
        self.doc_similarity =[0]
        for doc_id in range(1, self.doc_num + 1):
            #cos similarity
            sim = np.dot(self.TF_IDF_array[doc_id],self.TF_IDF)/(np.linalg.norm(self.TF_IDF_array)*np.linalg.norm(self.TF_IDF))
            self.doc_similarity.append([doc_id,sim])

    def ranking(self):
        """rank the document with similarity"""
        self.similarity()
        #sort
        self.doc_similarity[1:].sort(key=takeSecond, reverse=True)
        #pick the top10
        top10_doc_name = []
        for i in range(1, 11):
            doc_id = self.doc_similarity[i][0]
            top10_doc_name.append(self.DocMap[doc_id])
        return top10_doc_name


    def semantic_search(self):
        """run this runction"""
        """return top10_doc_name"""
        self.sparse_query()
        self.tf_idf_cal()
        res = self.ranking()
        return res 

#####words query............
S = Semantic_Search("president high")
print(S.semantic_search())
        
    