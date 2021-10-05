import os
import json
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from DocSparse import Doc_Sparse

class PostingList_construct:
    """
        DocMap[0] is the number of news documents
        DocMap[1..DocMap[0]] is the name of each documents

        PostingList[0] is the number of words
        PostingList[word_id] starting from 1 is [[doc_id,word_freq_in_this_doc]]

        WordMap is the dictionary of words
        WordMap[word] = word_id
    """
    def __init__(self):
        # initialize PostingList and DocMap
        PostingList = [0]
        DocMap = [0]
        WordMap = {}
        doc_id = 0
        word_num = 0

        # read data files and construct the PostingList
        rootdir_base = '..\\dataset\\US_Financial_News_Articles\\2018_0'
        for i in range(1,6):
            rootdir = rootdir_base + str(i)
            list = os.listdir(rootdir)
            for j in range(0,len(list)):
                path = os.path.join(rootdir,list[j])
                file_name_split = path.split('\\')
                file_name = file_name_split[-1]
                if os.path.isfile(path):
                    #procedures on document
                    with open(path,'r',encoding="utf-8")as fp:
                        json_data = json.load(fp)
                        doc_id += 1

                        #convert document to word
                        title = json_data["title"]
                        text = json_data["text"]
                        doc_sparse = Doc_Sparse(text + title)
                        words,fdist = doc_sparse.sparse()

                        #construct index inverted list
                        for word in words:
                            if word in WordMap:
                            # existed word in PostingList
                                word_id = WordMap[word]
                                PostingList[word_id].append([doc_id,fdist.freq(word)])
                            else:
                                word_num += 1
                                WordMap[word] = word_num
                                PostingList.append([])
                                PostingList[word_num].append([doc_id,fdist.freq(word)])

                        DocMap.append(file_name)

        DocMap[0] = doc_id
        PostingList[0] = word_num

        self.DocMap = DocMap
        self.PostingList = PostingList
        self.WordMap = WordMap
                        

    def write_to_file(self):
        #run this function
        #write to json 
        jsonDocMap = json.dumps(self.DocMap)
        fileObject1 = open('..\\output\\DocMap.json', 'w')  
        fileObject1.write(jsonDocMap)  
        fileObject1.close()

        jsonPostingList = json.dumps(self.PostingList)
        fileObject2 = open('..\\output\\PostingList.json', 'w')  
        fileObject2.write(jsonPostingList)  
        fileObject2.close() 

        jsonWordMap = json.dumps(self.WordMap)
        fileObject3 = open('..\\output\\WordMap.json', 'w')  
        fileObject3.write(jsonWordMap)
        fileObject3.close() 

P = PostingList_construct()
P.write_to_file()