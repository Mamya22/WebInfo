import faiss
import pickle
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
#数据提取
file_path = "./data/law_data_3k_gbk.csv"#gbk编码

loader = CSVLoader(file_path=file_path)
data = loader.load()

# for record in data[:2]:
#     print(record)

#文本分割：将法律文献分割成段落、章节或案例，以便于后续检索和匹配。
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

texts = text_splitter.split_documents(data)

# for text in texts[:2]:
#     print(text)

#转换成向量
embeddings = HuggingFaceBgeEmbeddings(model_name="./model")
# for record in texts[:2]:
#     embedding_vector = embeddings.embed_query(record.page_content)
#     print(embedding_vector)

#数据入库
db = FAISS.from_documents(texts, embeddings)
faiss_index_path = "./data/faiss_index.faiss"
faiss.write_index(db.index, faiss_index_path)
print("数据入库完成")

# query = "业务范围"
query = "个人独资企业"
docs = db.similarity_search(query)
print(docs[0].page_content)

with open("./data/faiss_db.pkl", "wb") as f:
    pickle.dump(db, f)

print("数据保存完成")
