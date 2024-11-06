import jieba
import json
from typing import Dict, List
import re
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

    # can choose two modes to split the words
    def split_info(self, text: str, mode="jieba") -> List:
        pattern = '[^A-Za-z0-9\u4e00-\u9fa5]'
        if mode == "jieba":
            seg_list = jieba.lcut(re.sub(pattern, '', text), cut_all=False)
            # seg_list = jieba.lcut(text, cut_all=False)
        else:
            # seg_list = pkuseg.pkuseg().cut(re.sub(pattern, '', text))
            seg_list = pkuseg.pkuseg().cut(text)
        extracted_word = []
        # print(seg_list)
        for word in seg_list:#去除停用词
            if word not in self.stop_word_list:
                extracted_word.append(word)
        print(extracted_word)
        print('开始合并近义词')
        model = SentenceTransformer("C:\\Users\\lenovo\\Downloads\\paraphrase-multilingual-MiniLM-L12-v2")
        # list1 = []
        # list2 = []
        for i in range(len(extracted_word)):#合并近义词
            if extracted_word[i] not in self.single_id_info and extracted_word[i] != ' ':#不在列表中的词加入
                print(extracted_word[i])
                self.single_id_info.append(extracted_word[i])
            for j in range(i + 1, len(extracted_word)):#如果相近，设为空格
                if len(extracted_word[j]) > 0 and len(extracted_word[i]) > 0 and extracted_word[i] != ' ' and extracted_word[j] != ' ':
                    # list1.append(extracted_word[i])
                    # list2.append(extracted_word[j])
                    embeddings1 = model.encode(extracted_word[i])
                    embeddings2 = model.encode(extracted_word[j])
                    if extracted_word[j] not in self.single_id_info and model.similarity(embeddings1,embeddings2).item() > 0.9:
                        print('合并', extracted_word[j])
                        extracted_word[j] = ' '
                # list1.clear()
                # list2.clear()
        print(self.single_id_info)
        return self.single_id_info

    def combine_single_info(self, info: dict) -> Dict:

        self.extracted_info[info['ID']] = self.single_id_info
        self.single_id_info = []
        return self.extracted_info

    def save_keyword_to_json(self):
        with open(self.result_path, 'w', encoding="UTF-8") as f:
            json.dump(self.extracted_info, f, indent=4, ensure_ascii=False)