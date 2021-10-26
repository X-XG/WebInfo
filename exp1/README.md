## 文件结构

```
exp1/
|----src/
	|----bool_search.py
	|----semantic_search.py
	|----image_search.py
	|----DocSparse.py
	|----PL_construct.py
	|----tf_idf_construct.py
	|----word2vec_train.py
|----dataset/
	|----QueryVocabulary.txt
	|----US_Financial_News_Articles/
		...
|----output/
	|----README.md
	|----DocMap.json
	|----WordMap.json
	|----PostingList.json
	|----TF_IDF.npz
	|----word2vec/
		|----word2vec.model
		|----DocMap.json
		|----doc_word_list.json
|----report.pdf
|----config.yaml
|----README
```

注：`dataset`实际只包含`QueryVocabulary.txt`为查询词表，`US_Financial_News_Articles`文件夹是将`US_Financial_News_Articles.zip`在`dataset`目录下解压

关于output文件，过于大的文件并未上传，用睿客云链接的形式



## 运行环境

在conda中可以如下命令创建环境：

```
conda env create -f config.yaml
```

`python=3.7`,包含库`nltk`,`gensim`,`skimage`,`math`,`scipy`,`numpy`,`json`,`re`,`os`等。



## 构建output运行顺序

1. tf-idf 语义表征

* 运行`PL_construct.py`生成`DocMap.json`,`PostingList.json`,`WordMap.json`
* 运行`tf_idf_construct.py`生成`TF_IDF.npz`

2. word2vec语义表征及查询

* 运行`word2vec_train.py`生成`word2vec.model`



## 查询时运行方式

由于查询句子在命令行中会被拆分，所以在程序运行时通过`input`输入查询句子

1. bool查询

   运行`bool_search.py`

2. 语义查询

   * tf-idf表征查询

     运行`semantic_search.py`进行语义查询，参数`embedding_type="tf-idf"`

   * word2vec表征查询

     运行`semantic_search.py`进行语义查询，参数`embedding_type="word2vec"`

   * 使用同义词表优化

     其它同上，运行`semantic_search.py`时，参数`synonym_tag=True`

3. 图片查询

   运行`image_search.py`



## 关键函数说明

#### Doc_Sparse.py

##### class Doc_Sparse

对文档进行预处理的类

* document_to_sentence: 将文档字符串分隔成句子
* sentence_to_tokenized:将句子分割成词
* stem_word:词干化
* stop_word:停用词
* freq_word:计算词频
* simple_word:去重
* sparse:类中主要函数



#### PL_construct.py

##### class PostingList_construct

* init:生成倒排表
* write_to_file:写入output文件



#### tf_idf_construct.py

##### class TF_IDF_construct

* tf_idf_cal:计算tf-idf矩阵
* write_to_file:写入output文件



#### word2vec_train.py

##### class Doc_Sparse

区别于`Doc_Sparse.py`中的类，主要是因为要按句子为单位分词喂给word2vec模型

##### class Word2Vec_Embedding

* init: 生成sentence分词列表
* train:训练并保存模型
* write_to_file:写入output其它文件



#### semantic_search.py

##### class Semantic_Search

* read_file: 根据语义类型从output中读取文件
* sparse_query: 分割query并引入同义词
* tf_idf_cal:对query计算tf-idf向量
* similarity:计算相似度
* ranking:根据相似度排序





