import pickle
import faiss
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
import os
from openai import OpenAI

# 配置API Key
DASHSCOPE_API_KEY = "sk-710beb4af35843cb9c0a726d38267cea"
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY

# 初始化嵌入模型
embeddings = HuggingFaceBgeEmbeddings(model_name="./model")

# 加载 `db` 对象
with open('./data/faiss_db.pkl', 'rb') as f:
    db = pickle.load(f)

# 加载 `faiss_index` 文件
faiss_index_path = "./data/faiss_index.faiss"
index = faiss.read_index(faiss_index_path)

# 更新 `db` 对象的向量索引
db.index = index

# 初始化MT-Turbo客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 创建prompt模板
template = """你是专业的法律知识问答助手。你需要使用以下检索到的上下文片段来回答问题，禁止根据常识和已知信息回答问题。如果你不知道答案，直接回答“未找到相关答案”。
Question: {question}
Context: {context}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template=template)

# 循环提问直到输入 "exit"
while True:
    # 获取用户输入
    query = input("请输入你的搜索查询（输入 'exit' 退出）：")
    
    # 检查是否退出
    if query.lower() == "exit":
        print("程序已退出")
        break

    # 将用户的提问向量化
    query_vector = embeddings.embed_query(query)

    # 使用加载的 `db` 对象进行相似性检索
    docs = db.similarity_search_by_vector(query_vector)

    # 整合检索结果以生成回答
    context = "\n".join([doc.page_content for doc in docs])
    
    # 构建MT-Turbo请求消息
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': f"Question: {query}\nContext: {context}\nAnswer:"}
    ]
    # print(messages)
    
    # 调用MT-Turbo模型
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
    )
    
    # 输出答案
    answer = completion.choices[0].message.content
    print(answer)
    print("*" * 50)
