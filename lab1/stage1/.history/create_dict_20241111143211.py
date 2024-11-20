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
        length = len(self.reverted_dict[keyword])
        self.length[keyword] = length # 记录倒排表长度 
        # 取跳表间隔为关键词长度的平方根
        length_sqrt = int(length ** 0.5)
        self.interval[keyword] = max(1, length_sqrt) # 确保间隔至少为1 
        # 设置头节点
        if self.length[keyword] > 1:
            skip_length = self.interval[keyword]
        else:
            skip_length = 0
        self.list_head[keyword] = ((self.reverted_dict[keyword][0]), skip_length , 0) # 文档ID;跳表间隔；初始索引值
        self.skip_dict[keyword] = [self.list_head[keyword]]
        
        for i in range(self.interval[keyword], self.length[keyword] - self.interval[keyword], self.interval[keyword]):
            # 以跳表间隔为步长，遍历倒排表
            # 元组赋值为对应ID;下一个节点索引值；当前节点索引值   
            node = ((self.reverted_dict[keyword][i]), i + self.interval[keyword], i)
            # 添加到序列
            self.skip_dict[keyword].append(node)
        
        # 当前最后一个节点索引值
        cur_last_index = len(self.skip_dict[keyword])*self.interval[keyword]
        if cur_last_index < len(self.reverted_dict[keyword])-1:
            # 未到最后一个节点
            node = ((self.reverted_dict[keyword][cur_last_index]),len(self.reverted_dict[keyword])-1,cur_last_index)
            # 添加尾节点
            self.skip_dict[keyword].append(node)
            
    def _create_skip_structure(self): 
        for keyword in self.reverted_dict.keys(): 
            self._create_skip_list(keyword)

if __name__ == "__main__":
    # TODO 更改路径
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip1 = SkipRevertList(participle_dict)
    skip1._create_skip_structure()
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\movie_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip2 = SkipRevertList(participle_dict)
    skip2._create_skip_structure()
    # 输出调试
    # print("Reverted Dictionary:")
    # print(json.dumps(skip.reverted_dict, indent=4, ensure_ascii=False))
    # print("\nSkip List Dictionary:")
    # print(json.dumps(skip.skip_dict, indent=4, ensure_ascii=False))
    # 输出倒排表，倒排表路径
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_reverted_dict.json","w",encoding="UTF-8") as fout_reverted_dict:
       json.dump(skip.reverted_dict,fout_reverted_dict, indent=4, ensure_ascii=False)
    # 输出跳表，跳表路径
    with open(r"C:\Users\28932\OneDrive\桌面\Web\lab\lab1\WebInfo\result\book_skip_dict.json","w",encoding="UTF-8") as fout_skip_dict:
       json.dump(skip.skip_dict,fout_skip_dict, indent=4, ensure_ascii=False)