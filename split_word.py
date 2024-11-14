import jieba
import json
from typing import Dict, List
import re
from snownlp import SnowNLP
# import pkuseg
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers.models.cvt.convert_cvt_original_pytorch_checkpoint_to_pytorch import embeddings



class Split:
    def __init__(self, path, stop_word_path, result_path):
        self.path = path
        self.stop_word_path = stop_word_path
        self.result_path = result_path
        self.info = {}
        self.single_id_info = []
        self.stop_word_list = []
        self.extracted_info = {}


    def get_info(self) -> List:
        data = pd.read_csv(self.path)  # 读取文件中所有数据
        self.info = data.to_dict(orient='records')
        # print(self.info)
        return self.info

    def get_stop_word_list(self) -> List:
        with open(self.stop_word_path, 'r', encoding="UTF-8") as f:
            self.stop_word_list = [word.strip('\n') for word in f.readlines()]
        return self.stop_word_list

    def split_info(self, text: str, mode: str):
        #分词，可以选择两种模式
        pattern = '[^A-Za-z0-9\u4e00-\u9fa5]'
        #re.sub用于把text中不属于字母（大小写）、数字以及汉字的字符替换成空格
        if mode == "jieba":
            seg_list = jieba.lcut(re.sub(pattern, '', text), cut_all=False)#精简模式
            # seg_list = jieba.lcut_for_search(text)#搜索引擎模式，有时会保留多种分词结果
            # seg_list = jieba.lcut(text, cut_all=False)
        elif mode == "snowNLP":
            seg_list = SnowNLP(re.sub(pattern, '', text)).words

        #去除停用词
        extracted_word = []
        for word in seg_list:
            if word not in self.stop_word_list:
                extracted_word.append(word)
        print(extracted_word)

        #合并近义词
        l = 0
        print('开始合并近义词')
        model = SentenceTransformer("C:\\Users\\lenovo\\Downloads\\paraphrase-multilingual-MiniLM-L12-v2")
        for i in range(len(extracted_word)):
            if extracted_word[i] not in self.single_id_info and extracted_word[i] != ' ':#不在列表中的词加入
                flag = 0
                for j in range(l):#若和列表中的词词意相近则删除，否则加入
                    embeddings1 = model.encode(extracted_word[i])
                    embeddings2 = model.encode(self.single_id_info[j])
                    if model.similarity(embeddings1,embeddings2).item() > 0.9:
                        flag = 1
                        print('合并', extracted_word[i])
                        break
                if flag == 0:
                    self.single_id_info.append(extracted_word[i])
                    print('添加', extracted_word[i])
                    l += 1
        print(self.single_id_info)


    def combine_single_info(self, info: dict):
        self.extracted_info[info['ID']] = self.single_id_info
        self.single_id_info = []

    def save_to_json(self):
        with open(self.result_path, 'w', encoding="UTF-8") as f:
            json.dump(self.extracted_info, f, indent=4, ensure_ascii=False)