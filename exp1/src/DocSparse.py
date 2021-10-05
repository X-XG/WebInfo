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