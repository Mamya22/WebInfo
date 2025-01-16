# <center>Web信息处理与应用 实验三</center>

## 实验简介

​	利用公开法律相关知识数据库，并基于 langchain 开发框架，实现一种简单的 RAG 问答应用示例。本次实验的主要目的是比较大模型的生成式检索与普通检索的区别，以及引入 RAG 之后大模型在专业搜索上是否做得更好。

### 实验环境

+ System：Win 11
+ 开发工具：Vscode，Pycharm community
+ 编程语言：python
+ 编程环境：Anaconda
+ Repository：[Github仓库](https://github.com/Mamya22/WebInfo.git)

### 实验成员

+ 组长：方馨   PB22111656
+ 组员：马筱雅 PB22111639
+ 组员：陈昕琪 PB22111711

### 代码目录
```

```

## 实验内容


### 1. 数据准备阶段：主要是将私域数据向量化后构建索引并存入数据库的过程，主要包括：数据提取、文本分割、向量化、数据入库等环节。

+ 把csv文集转换成gbk编码后，使用 langchain.document_loaders 中的 CSVLoader 加载数据。
```python
file_path = "./data/law_data_3k_gbk.csv"#gbk编码
loader = CSVLoader(file_path=file_path)
data = loader.load()
```

+ 使用 CharacterTextSplitter 对数据进行文本分割
```python
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.split_documents(data)
```

+ 使用m3e-base模型对文本向量化，加载模型
```python
embeddings = HuggingFaceBgeEmbeddings(model_name="./model")
```

+ 数据向量化后构建索引，并写入数据库FAISS
```python
db = FAISS.from_documents(texts, embeddings)
```

### 2. 数据检索阶段：我们根据用户的提问，通过高效的检索方法，召回与提问最相关的知识，并融入 Prompt，才能使得大模型参考当前提问和相关知识，生成相应的答案。常见的数据检索方法包括：相似性检索、全文检索等。本次实验中，将向量入库后，我们可以直接调用 db.similarity_search 语句进行问题的相似性检索，可将得到结果与后续大模型生成结果进行对比。（选做：可探索其他检索方式，并与最终大模型生成结果进行对比）



### 3. LLM 生成阶段：将检索得到的相关知识注入 prompt，大模型参考当前提问和相关知识，生成相应的答案。

### 4. 需要实现的 question
