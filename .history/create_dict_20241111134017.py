import json
import bisect
from collections import defaultdict

class RevertDict: 
    def __init__(self, dictionary): 
        self.dict = dictionary # 存入的字典
        self.reverted_dict = defaultdict(list) # 倒排表
        self.create_reverted_dict() # 生成
    
    def create_reverted_dict(self):
        for key, items in self.dict.items():
            for item in items:
                key_value = int(key)
                if key_value not in self.reverted_dict[item]:
                    # ID不在关键词列表里
                    bisect.insort(self.reverted_dict[item], key_value) # 按照顺序插入

    

class SkipRevertList(RevertDict): # 继承倒排表 
    def __init__(self, dictionary): 
        super().__init__(dictionary) 
        self.length = defaultdict(int) # 键：字符串 值：倒排表长度 
        self.interval = defaultdict(int) # 键：字符串 值：跳表间隔 
        self.skip_dict = defaultdict(list) # 键：字符串 值：List，由一系列跳表节点组成的列表 
        self.list_head = defaultdict(tuple) # 键：字符串 值：skip_node对象 
        self._create_skip_dict() 
        
    def _create_skip_list(self, word): 
        self.length[word] = len(self.reverted_dict[word]) 
        self.interval[word] = max(1, int(self.length[word] ** 0.5)) # 确保间隔至少为1 
        self.list_head[word] = (self.reverted_dict[word][0], self.interval[word], 0) 
        self.skip_dict[word].append(self.list_head[word]) 
        for i in range(self.interval[word], self.length[word], self.interval[word]): 
            if i < self.length[word]:
                node = (self.reverted_dict[word][i], min(i + self.interval[word], self.length[word]), i) 
                self.skip_dict[word].append(node) 
        last = len(self.skip_dict[word]) * self.interval[word] 
        if last < self.length[word] - 1: 
            node = (self.reverted_dict[word][last], self.length[word], last) 
            self.skip_dict[word].append(node) 
                
    def _create_skip_dict(self): 
        for word in self.reverted_dict: 
            self._create_skip_list(word)

if __name__ == "__main__":
    # TODO 更改路径
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip = SkipRevertList(participle_dict)
    skip._create_skip_dict()
    # print("Reverted Dictionary:")
    # print(json.dumps(skip.reverted_dict, indent=4, ensure_ascii=False))

    # print("\nSkip List Dictionary:")
    # print(json.dumps(skip.skip_dict, indent=4, ensure_ascii=False))
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_reverted_dict.json","w",encoding="UTF-8") as fout_reverted_dict:
       json.dump(skip.reverted_dict,fout_reverted_dict, indent=4, ensure_ascii=False)
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_skip_dict.json","w",encoding="UTF-8") as fout_skip_dict:
       json.dump(skip.skip_dict,fout_skip_dict, indent=4, ensure_ascii=False)