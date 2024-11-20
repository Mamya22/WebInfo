import json
from typing import AnyStr, Dict, List, Tuple
from colorama import Fore, Style

class BooleanMatch:
    def __init__(self):
        self.query = "" # 查询语句
        self.query_list = [] # 查询列表
        self.query_cachae_list = [] # 查询缓存列表
        self.mode = "" # 查询模式
        self.error = False # 错误标志
        self.keyword = "" # 信息
        self.reverted_dict = {} # 倒排表
        self.skip_dict = {} # 跳表
        self.pre_sort_list = [] # 预排序列表

        print(Fore.GREEN + "Boolean Match System" + Style.RESET_ALL)
        print("Welcome to Boolean Match System!")
        print("Please wait for initialization...")

        self.book_keyword_path = "./result/book_keyword.json"
        self.movie_keyword_path = "./result/movie_keyword.json"
        self.book_compressed_revert_dict_path = "./result/book_compressed_revert_dict.bin"
        self.movie_compressed_revert_dict_path = "./result/movie_compressed_revert_dict.bin"

        with open(self.book_keyword_path, "r", encoding="UTF-8") as f:
            self.book_keyword = json.load(f)

        with open(self.movie_keyword_path, "r", encoding="UTF-8") as f:
            self.movie_keyword = json.load(f)

        self.book_reverted_dict = self.decompress(self.book_compressed_revert_dict_path)
        self.movie_reverted_dict = self.decompress(self.movie_compressed_revert_dict_path)

        print(Fore.GREEN + "Initialization Completed! Start your travel" + Style.RESET_ALL)

    def decompress(self, compress_path) -> Dict:
        with open(compress_path, 'rb') as f_compress:
            contents_bytes = f_compress.read()
            contents_list = [] # 最终结果
            content_list = [] # 当前处理的一组字节
            for byte in contents_bytes:
                if byte >> 7 == 0: # 最高位为0
                    content_list.append(byte) # 直接追加
                else:
                    content_list.append(byte & 0x7f) # 取低7位
                    contents_list.append(content_list)
                    content_list = [] # 重置

        inverted_table = {} # 存储最终倒排索引表
        content_index = 0 # 当前处理的字节索引

        while content_index < len(contents_list):
            # 遍历content_list
            key_bytes = contents_list[content_index]
            key = ''.join([chr(b) for b in key_bytes]).strip() # 字节转换成字符串形式的key
            content_index += 1

            # 读取文档ID列表，直到找到一个特殊的终止符，如0字节
            doc_ids = [] # 当前关键词的文档ID列表
            while content_index < len(contents_list) and contents_list[content_index][0] != 0:
                id_bytes = contents_list[content_index]
                doc_id = 0
                for j in range(len(id_bytes)):
                    doc_id += id_bytes[len(id_bytes) - 1 - j] << (j * 7)
                if doc_ids:
                    doc_id += doc_ids[-1]
                doc_ids.append(doc_id)
                content_index += 1
            
            # 跳过特殊终止符
            content_index += 1
            
            inverted_table[key] = doc_ids

        return inverted_table # 返回索引表
    
    # 输出详细信息
    def print_message(self,_id: int):
        if(self.mode == 'book'):
            # book类型检索
            show_tag = "tag: " + self.book_keyword[_id]
            print(Fore.Green,show_tag)
        else:
            # movie类型检索
            show_tag = "tag: " + self.movie_keyword[_id]
            print(Fore.Green,show_tag)
        
    def SplitQuery(self) -> List:
        self.query = self.query.strip()
        self.query = self.query.replace('（', '(').replace('）', ')')
        self.query = self.query.replace('(', ' ( ').replace(')', ' ) ')
        self.query = self.query.upper()
        self.query = self.query.replace('AND', ' AND ').replace('OR', ' OR ').replace('NOT', ' NOT ')
        self.query = self.query.replace('和', ' AND ').replace('且', ' OR ').replace('非', ' NOT ')
        self.query = self.query.replace('&', ' AND ').replace('|', ' OR ').replace('！', ' NOT ').replace('!', ' NOT ')
        return self.query.split()
    
    def FindCorrespondBracket(self, index: int) -> int:
        # 括号处理
        i = index + 1
        flag = 0
        while i < len(self.query_list) and not self.error:
            if flag < 0:
                print("The right bracket overabundant!")
                self.error = True
            elif self.query_list[i] == ')':
                if flag == 0:
                    return i
                else:
                    flag -= 1
            elif self.query_list[i] == '(':
                flag += 1
            i += 1
        print("Lack of right bracket!")
        self.error = True
        return -1
    
    def CreateSkipList(self, L: List) -> List:
        if len(L) == 0:
            self.error = True
            return []
        if not self.error:
            interval = int(len(L) ** 0.5)
            skip_list = [[L[0], 0 if len(L) == 1 else interval, 0]]  # avoid len(L) == 1
            for i in range(interval, len(L) - interval, interval):
                skip_list.append([L[i], i + interval, i])
            last = len(skip_list) * interval
            if last < len(L) - 1:
                skip_list.append([(L[last]), len(L) - 1, last])
            return skip_list
        
    def Search(self,query:AnyStr,modes:AnyStr) -> List:
        self.query = query
        self.mode = modes
        self.query_list = self.SplitQuery()
        if self.error:
            return []
        if self.mode == 'book':
            self.keyword = self.book_keyword
            self.reverted_dict = self.book_reverted_dict
        else:
            self.keyword = self.movie_keyword
            self.reverted_dict = self.movie_reverted_dict
        pre_sort_id_list = list(self.keyword.keys())
        pre_sort_id_list.sort()
        self.pre_sort_list = (pre_sort_id_list, self.CreateSkipList(pre_sort_id_list))
        
        ret,ret_skip_list = self.BracketOperation(self.query_list)
        if len(ret) == 0:
            print(Fore.RED + "Sorry! But there are no results you want here.")
            # not find doesn't mean error, but doesn't need to output
        elif not self.error:
            print(Fore.BLUE + '*' * 50)
            for _id in ret:
                self.message(_id)
            print(Fore.BLUE + '*' * 50)
        return self.error
    










if __name__ == "__main__":
    bm = BooleanMatch()
    # print(bm.book_reverted_dict)
    # print(bm.movie_reverted_dict)
