import pickle
import faiss
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain_community.llms import Tongyi
from langchain.chains import LLMChain
import os

# 配置API Key
DASHSCOPE_API_KEY = "sk-2a1edd2f72954a7c8775fde803a7d610"
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY

# 初始化LLM
llm = Tongyi()

# 创建prompt模板
template = """你是专业的法律知识问答助手。你需要回答下面的法律问题，如果你不知道答案，直接回答“未找到相关答案”。
Question: {question}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template=template)

# 创建LLM链
llm_chain = LLMChain(prompt=prompt, llm=llm)

# 循环提问直到输入 "exit"
while True:
    # 获取用户输入
    query = input("请输入你的搜索查询（输入 'exit' 退出）：")
    
    # 检查是否退出
    if query.lower() == "exit":
        print("程序已退出")
        break

    answer = llm_chain.run(question=query)
    # print(template.format(question=query, context=context, answer=answer))
    print(answer)
    print("*" * 50)
