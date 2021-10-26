import os
import json
from gensim.models import word2vec
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

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

    def sparse(self):
        self.document_to_sentence()
        self.sentence_to_tokenized()
        self.stem_word()
        self.stop_word()
        return self.clean_words

class Word2Vec_Embedding:
    def __init__(self):
        doc_id = 0 
        self.Doc_Word_List = [0]
        self.DocMap = [0]
        rootdir_base = '..\\dataset\\US_Financial_News_Articles\\2018_0'
        for i in range(1,6):
            rootdir = rootdir_base + str(i)
            list = os.listdir(rootdir)
            for j in range(0,len(list)):
                path = os.path.join(rootdir,list[j])
                file_name_split = path.split('\\')
                file_name = "2018_0"+str(i)+"\\"+file_name_split[-1]
                if os.path.isfile(path):
                    #procedures on document
                    with open(path,'r',encoding="utf-8")as fp:
                        json_data = json.load(fp)
                        doc_id += 1

                        #convert document to word
                        title = json_data["title"]
                        text = json_data["text"]
                        doc_sparse = Doc_Sparse(title + text)
                        self.Doc_Word_List.append(doc_sparse.sparse())
                        
                        self.DocMap.append(file_name)
        self.DocMap[0] = doc_id
        self.sentences = []
        for doc_id in range(1,self.DocMap[0]+1):
            self.sentences.append(self.Doc_Word_List[doc_id])

    def train(self,model_output_path):
        """run this"""
        model = word2vec.Word2Vec(sentences=self.sentences,size=100,window=5,min_count=0)
        model.save(model_output_path)

    def write_to_file(self):
        jsonDocMap = json.dumps(self.DocMap)
        fileObject1 = open('..\\output\\word2vec\\DocMap.json', 'w')  
        fileObject1.write(jsonDocMap)  
        fileObject1.close()

        jsonDocMap = json.dumps(self.sentences)
        fileObject2 = open('..\\output\\word2vec\\doc_word_list.json', 'w')  
        fileObject2.write(jsonDocMap)  
        fileObject2.close()

if __name__ == '__main__':
    w2v = Word2Vec_Embedding()
    w2v.train("..\\output\\word2vec\\word2vec.model")
    w2v.write_to_file()
