import json
import bisect
from collections import defaultdict

class RevertDict: 
    def __init__(self, dictionary): 
        self.dict = dictionary 
        self.reverted_dict = defaultdict(list) 
        self._revert() 
    
    def _revert(self): 
        for key, items in self.dict.items(): 
            for item in items: # key: id, item: str(name) 
                key_int = int(key) 
                if key_int not in self.reverted_dict[item]: 
                    bisect.insort(self.reverted_dict[item], key_int) # 将key有序插入到列表中

    

class Skip_revert_list(RevertDict):            #继承倒排表

    def __init__(self,dict):
        self.dict = dict
        RevertDict.__init__(self,dict)
        self.length = {}            #键：字符串     值：倒排表长度
        self.interval = {}          #键：字符串     值：跳表间隔
        self.skip_dict = {}         #键：字符串     值：List，由一系列跳表节点组成的列表
        self.list_head = {}         #键：字符串     值：skip_node对象
        self.create_skip_dict()
    
    def create_skip_list(self,word):
        self.length[word] = len(self.reverted_dict[word])
        self.interval[word] = int((self.length[word]) ** 0.5)
        self.list_head[word] = ((self.reverted_dict[word][0]), self.interval[word] if self.length[word]>1 else 0 , 0)
        self.skip_dict[word] = [self.list_head[word]]
        for i in range(self.interval[word], self.length[word] - self.interval[word], self.interval[word]):
            node = ((self.reverted_dict[word][i]), i + self.interval[word], i)       #(value,next,down)
            self.skip_dict[word].append(node)
        last = len(self.skip_dict[word])*self.interval[word]
        if last < len(self.reverted_dict[word])-1:
            node = ((self.reverted_dict[word][last]),len(self.reverted_dict[word])-1,last)
            self.skip_dict[word].append(node)
    def create_skip_dict(self):
        for key in self.reverted_dict.keys():
            self.create_skip_list(key)

if __name__ == "__main__":
    # TODO 更改路径
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip = Skip_revert_list(participle_dict)
    skip.create_skip_dict()
    print("Reverted Dictionary:")
    print(json.dumps(skip.reverted_dict, indent=4, ensure_ascii=False))

    # print("\nSkip List Dictionary:")
    # print(json.dumps(skip.skip_dict, indent=4, ensure_ascii=False))
    # with open(r".\result\book_reverted_dict.json","w",encoding="UTF-8") as fout_reverted_dict:
    #    json.dump(skip.reverted_dict,fout_reverted_dict, indent=4, ensure_ascii=False)
    # with open(r".\result\book_skip_dict.json","w",encoding="UTF-8") as fout_skip_dict:
    #    json.dump(skip.skip_dict,fout_skip_dict, indent=4, ensure_ascii=False)