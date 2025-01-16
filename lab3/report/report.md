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


### 1. 数据准备阶段
主要是将私域数据向量化后构建索引并存入数据库的过程，主要包括：数据提取、文本分割、向量化、数据入库等环节。

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
### 2. 数据检索阶段
#### 2.1 具体步骤
- 根据向量相似度，首先向量化提问，检索出与提问最相关的知识
```python
# 将用户的提问向量化
query_vector = embeddings.embed_query(query)
# 使用加载的 `db` 对象进行相似性检索
docs = db.similarity_search_by_vector(query_vector)
```

- 创造`rag`链
``` python
# 创建prompt模板
template = """你是专业的法律知识问答助手。你需要使用以下检索到的上下文片段来回答问题，禁止根据常识和已知信息回答问题。如果你不知道答案，直接回答“未找到相关答案”。
Question: {question}
Context: {context}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template=template)

# 创建LLM链
llm_chain = LLMChain(prompt=prompt, llm=llm)
```

- 将检索文档融入`prompt`，并生成回答，采用`Qwen`模型
```python
context = "\n".join([doc.page_content for doc in docs])
answer = llm_chain.run(question=query, context=context)
```

#### 2.2 问题检索

##### 问题1：如何通过法律手段应对民间借贷纠纷？
**RAG**
![alt text](<屏幕截图 2025-01-16 162431(1).png>)

**无RAG**
![alt text](<屏幕截图 2025-01-16 164218-1.png>)

通过对两种方式分析，可以看出，在使用`RAG`进行问答时，得到的结果更加精简和具体，例如使用`RAG`的问答结果直接给出了最符合情况的三种方式，而不是笼统的将所有处理问题的方式全盘托出。

##### 问题2： 借款人去世，继承人是否应履行偿还义务？
**RAG**
![alt text](<屏幕截图 2025-01-16 162431-2.png>)
**无RAG**
![alt text](<屏幕截图 2025-01-16 164218-2.png>)

两种方式对比，使用`RAG`的结果给出了更直接的结果：继承人仅在继承遗产时承担偿还义务，而不使用`RAG`仅给出了常见的情况以及建议，如责任范围、债务清偿顺序，仅给出了条例，具体的处理方式需要用户自己定夺，并没有根据问题直接进行回答。
##### 问题3：没有赡养老人就无法继承遗产吗？
**RAG**
![alt text](<屏幕截图 2025-01-16 162431-3.png>)
**无RAG**
![alt text](<屏幕截图 2025-01-16 164240.png>)

该问题在知识库中没有相关答案，所以使用`RAG`的检索考虑到上下文，结果稍微局限，仅给出相关的讯息，但未给出具体的结果，而对于未采用`RAG`的情况，回答受上下文限制少，更依赖于`LLM`自身的知识库，给出了通常情况下的结果。
##### 问题4：你现在是一个精通中国法律的法官，请对以下案件做出分析：2012 年 5月 1 日，原告 xxx 在被告 xxxx 购买“玉兔牌”香肠 15 包，其中价值 558.6 元的 14 包香肠已过保质期。xxx 到收银台结账后，即径直到服务台索赔，后因协商未果诉至法院，要求 xxxx 店支付 14 包香肠售价十倍的赔偿金 5586 元。
**RAG**
![alt text](<屏幕截图 2025-01-16 162810.png>)
**无RAG**
![alt text](<屏幕截图 2025-01-16 164306.png>)
在该问题中，使用`RAG`的检索结果根据已有专业知识库，检索出相关法律法规，以此为依据得出可能的处理结果。而未使用`RAG`的问答结果更为全面，包含处理的整个流程，并给出可能的反驳思路（被告可能的抗辩理由），最终得到结果。
#### 2.3 引入 RAG 前后大模型在专业搜索上的区别
通过以上4个案例及其问答结果对比，可以得到引入`RAG`前后大模型在专业搜索上的区别如下：
- 引入`RAG`后，对于专业知识的
#### 2.3 RAG检索与普通检索的区别

