#### 文件结构

```
exp1/
|----src/
	|----bool_search.py
	|----semantic_search.py
|----dataset/
	|----QueryVocabulary.txt
	|----US_Financial_News_Articles
|----output/
	|----{your output files}
|----report.pdf
|----README
```

注：`dataset`实际只包含`QueryVocabulary.txt`为查询词表，`US_Financial_News_Articles`文件夹是将`US_Financial_News_Articles.zip`在`dataset`目录下解压



#### 数据结构

##### DocMap

`DocMap[0]` 是文档数量

`DocMap[1..DocMap[0]]` 是文档名字

##### PostingList

`PostingList[0]`是单词数量

`PostingList[1..PostingList[0]]`是倒排索引表

`PostingList[word_id]=[[doc_id,word_freq_in_this_doc]]`

##### WordMap

`WordMap`单词的字典

`WordMap[word]=word_id`



#### 创建环境

```
conda env create -f config.yaml
```



#### 运行顺序

* 运行`PL_construct.py`生成`DocMap.json`,`PostingList.json`,`WordMap.json`

* 运行`tf_idf_construct.py`生成`TF_IDF.npy`
* 运行`semantic_search.py`进行语义查询
