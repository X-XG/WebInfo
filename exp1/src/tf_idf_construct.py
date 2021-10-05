import os
import json
import numpy as np
import math

class TF_IDF_construct:
    def __init__(self):
        postinglist_path = '..\\output\\PostingList.json'
        docmap_path = '..\\output\\docmap.json'
        with open(postinglist_path,'r',encoding="utf-8")as fp_postinglist:
            self.PostingList = json.load(fp_postinglist)
            self.word_num = self.PostingList[0]

        with open(docmap_path,'r',encoding="utf-8")as fp_docmap:
            DocMap = json.load(fp_docmap)
            self.doc_num = DocMap[0]

    def tf_idf_cal(self):
        """generate the array of tf_idf_cal"""
        """TF_IDF_array[doc_id][word_id]=tf_idf"""
        TF_IDF_array = np.zeros((self.doc_num + 1,self.word_num + 1))
        for word_id in range(1, self.PostingList[0] + 1):
            for word_in_doc in self.PostingList[word_id]:
                doc_id = word_in_doc[0]
                freq = word_in_doc[1]
                TF = freq
                IDF = math.log(self.doc_num/(len(self.PostingList[word_id]) + 1))
                TF_IDF_array[doc_id][word_id] = TF * IDF
        self.TF_IDF_array = TF_IDF_array
        print(TF_IDF_array)

    def write_to_file(self):
        """run this function"""
        """write to file"""
        self.tf_idf_cal()
        np.save("..\\output\\TF_IDF.npy",self.TF_IDF_array)

T = TF_IDF_construct()
T.write_to_file()
