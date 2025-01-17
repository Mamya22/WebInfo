import pickle
import faiss
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain_community.llms import Tongyi
from langchain.chains import LLMChain
import os

# 配置API Key
DASHSCOPE_API_KEY = "sk-2a1edd2f72954a7c8775fde803a7d610"
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY

# 初始化嵌入模型
embeddings = HuggingFaceBgeEmbeddings(model_name="moka-ai/m3e-base")

# 加载 `db` 对象
with open('./data/faiss_db.pkl', 'rb') as f:
    db = pickle.load(f)

# 加载 `faiss_index` 文件
faiss_index_path = "./data/faiss_index.faiss"
index = faiss.read_index(faiss_index_path)

# 更新 `db` 对象的向量索引
db.index = index

# 初始化LLM
llm = Tongyi()

# 创建prompt模板
template = """你是专业的法律知识问答助手。你需要使用以下检索到的上下文片段来回答问题，禁止根据常识和已知信息回答问题。如果你不知道答案，直接回答“未找到相关答案”。为了提高回答的准确性，请使用逐步推理的方式，通过以下步骤得出答案：  
1. 问题理解：清晰地解析用户的问题，并提取关键信息。  
2. 上下文分析：从检索到的内容中找到与问题相关的片段。  
3. 推理过程：基于上下文片段，分析并逻辑推导答案。  
4. 最终回答：根据推理总结出简洁、准确的回答。如果未找到相关答案，直接回答“未找到相关答案”。  

请严格按照以上步骤进行回答，并禁止根据常识或已有知识回答问题。  

Question: {question}  
Context: {context}  
Answer:
1. 问题理解:  
2. 上下文分析:  
3. 推理过程:  
4. 最终回答:  
"""
prompt = ChatPromptTemplate.from_template(template=template)

# 创建LLM链
# llm_chain = LLMChain(prompt=prompt, llm=llm)

# 循环提问直到输入 "exit"
while True:
    # 获取用户输入
    query = input("请输入你的搜索查询（输入 'exit' 退出）：")
    
    # 检查是否退出
    if query.lower() == "exit":
        print("程序已退出")
        break

    # 将用户的提问向量化
    # query_vector = embeddings.embed_query(query)

    # 使用加载的 `db` 对象进行相似性检索
    # docs = db.similarity_search_by_vector(query_vector)
    retriever = db.as_retriever()
    # 整合检索结果以生成回答
    # context = "\n".join([doc.page_content for doc in docs])
    # answer = llm_chain.run(question=query, context=context)
    rag_chain = (
    {"context": retriever,  "question": RunnablePassthrough()} 
    | prompt 
    | llm
    | StrOutputParser() 
    )
    answer = rag_chain.invoke(query)
    # 整合检索结果以生成回答
    # context = "\n".join([doc.page_content for doc in docs])
    # answer = llm_chain.run(question=query, context=context)
    # print(template.format(question=query, context=context, answer=answer))
    print(answer)
    print("*" * 50)
