import pickle
import faiss
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS

# 加载 `db` 对象
with open('./data/faiss_db.pkl', 'rb') as f:
    db = pickle.load(f)

# 加载 `faiss_index` 文件
faiss_index_path = "./data/faiss_index.faiss"
index = faiss.read_index(faiss_index_path)

# 更新 `db` 对象的向量索引
db.index = index

# 初始化嵌入模型
embeddings = HuggingFaceBgeEmbeddings(model_name="./model")

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

    # 只输出 `page_content`
    for doc in docs:
        print(doc.page_content)
