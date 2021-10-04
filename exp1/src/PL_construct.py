import nltk
import os
import json
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import simple

class Doc_Sparse:
    def __init__(self,text):
        self.document = text

    def document_to_sentence(self):
        # replace '\n' with blank 
        self.document = re.sub('\n',' ',self.document)
        if isinstance(self.document,str):
            self.document = self.document
        else:
            raise ValueError('DOcument is not string!')
        #delete '\n',''\r',''\t','' in the in the begining and end
        self.document = self.document.strip()
        sentences = nltk.sent_tokenize(self.document)
        self.sentences = [sentence.strip() for sentence in sentences]

    def sentence_to_tokenized(self):
        original_words = []
        for sentence in self.sentences:
            original_words += nltk.word_tokenize(sentence)
        self.original_words=[word.lower() for word in original_words if word.isalpha()]

    def stem_word(self):
        stemmer = PorterStemmer()
        self.stemmed_words = [stemmer.stem(word) for word in self.original_words]

    def stop_word(self):
        stopwords.words('english')
        clean_words = self.stemmed_words[:]
        for word in self.stemmed_words:
            if word in stopwords.words('english'):
                clean_words.remove(word)
        self.clean_words = clean_words

    def freq_word(self):
        self.fdist = nltk.FreqDist(self.clean_words)

    def simple_word(self):
        self.simple_words = list(set(self.clean_words))

    def sparse(self):
        self.document_to_sentence()
        self.sentence_to_tokenized()
        self.stem_word()
        self.stop_word()
        self.freq_word()
        self.simple_word()
        return self.simple_words,self.fdist

class add_to_PostingList:
    def __init__(self,PostingList,words,fdist,doc_id):
        self.PostingList = PostingList
        self.words = words
        self.fdist = fdist
        self.doc_id = doc_id

    def add_to_PL(self):
        for word in self.words:
            if word in self.PostingList:
            # existed word in PostingList
                self.PostingList[word].append([self.doc_id,self.fdist.freq(word)])
            else:
                self.PostingList[word]=[]
                self.PostingList[word].append([self.doc_id,self.fdist.freq(word)]) 
        return self.PostingList   
        

class PostingList_construct:
    def __init__(self):
        # initialize PostingList and DocMap
        PostingList = {}
        DocMap = []

        # read data files and construct the PostingList
        rootdir_base = '..\\dataset\\US_Financial_News_Articles\\2018_0'
        doc_id = 0
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
                        add_to_pl = add_to_PostingList(PostingList,words,fdist,doc_id)
                        PostingList = add_to_pl.add_to_PL()
                        DocMap.append(file_name)

        self.DocMap = DocMap
        self.PostingList = PostingList
                        

    def write_to_file(self):
        #run this function
        #write to json 
        jsonDocMap = json.dumps(self.DocMap)
        jsonPostingList = json.dumps(self.PostingList)
        fileObject1 = open('DocMap.json', 'w')  
        fileObject1.write(jsonDocMap)  
        fileObject1.close()  
        fileObject2 = open('PostingList.json', 'w')  
        fileObject2.write(jsonPostingList)  
        fileObject2.close() 


