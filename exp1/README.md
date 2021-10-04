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

#### 倒排索引表数据结构

```
PostingList=[word,doc[]]
doc=[(id,freq)]
```

`PostingList`是倒排表，`word`是词项，`doc`是词项所在的文档列表，`id`是文档编号，`freq`是词项在文档中的频率
