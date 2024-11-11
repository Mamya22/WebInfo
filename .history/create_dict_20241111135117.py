import json
import bisect
from collections import defaultdict

# 生成倒排表
class RevertDict: 
    def __init__(self, dictionary): 
        self.dict = dictionary # 存入的字典
        self.reverted_dict = defaultdict(list) # 倒排表
        self._create_reverted_dict() # 生成
    
    def _create_reverted_dict(self):
        for key, items in self.dict.items():
            for item in items:
                key_value = int(key)
                if key_value not in self.reverted_dict[item]:
                    # ID不在关键词列表里
                    bisect.insort(self.reverted_dict[item], key_value) # 按照顺序插入

    
# 生成跳表
class SkipRevertList(RevertDict): 
    def __init__(self, dictionary): 
        super().__init__(dictionary) 
        self.length = defaultdict(int) # 关键词的倒排表长度
        self.interval = defaultdict(int) # 跳表间隔
        self.skip_dict = defaultdict(list) # 跳表字典
        self.list_head = defaultdict(tuple) # 跳表头
        self._create_skip_structure() # 创建跳表
        
    def _create_skip_list(self, keyword): 
        self.length[keyword] = len(self.reverted_dict[keyword]) 
        # 取跳表间隔为关键词长度的平方根
        self.interval[keyword] = max(1, int(self.length[keyword] ** 0.5)) # 确保间隔至少为1 
        head_node = (self.reverted_dict[keyword][0], self.interval[keyword], 0) 
        self.skip_dict[keyword].append(head_node) 

        for idx in range(self.interval[keyword], self.length[keyword], self.interval[keyword]): 
            if idx < self.length[keyword]: 
                next_index = min(idx + self.interval[keyword], self.length[keyword]) 
                node = (self.reverted_dict[keyword][idx], next_index, idx) 
                self.skip_dict[keyword].append(node) 
        
        last_index = len(self.skip_dict[keyword]) * self.interval[keyword] 
        if last_index < self.length[keyword] - 1: 
            node = (self.reverted_dict[keyword][last_index], self.length[keyword], last_index) 
            self.skip_dict[keyword].append(node) 
            
    def _create_skip_structure(self): 
        for keyword in self.reverted_dict.keys(): 
            self._create_skip_list(keyword)

if __name__ == "__main__":
    # TODO 更改路径
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip = SkipRevertList(participle_dict)
    skip._create_skip_structure()
    # print("Reverted Dictionary:")
    # print(json.dumps(skip.reverted_dict, indent=4, ensure_ascii=False))

    # print("\nSkip List Dictionary:")
    # print(json.dumps(skip.skip_dict, indent=4, ensure_ascii=False))
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_reverted_dict.json","w",encoding="UTF-8") as fout_reverted_dict:
       json.dump(skip.reverted_dict,fout_reverted_dict, indent=4, ensure_ascii=False)
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_skip_dict.json","w",encoding="UTF-8") as fout_skip_dict:
       json.dump(skip.skip_dict,fout_skip_dict, indent=4, ensure_ascii=False)