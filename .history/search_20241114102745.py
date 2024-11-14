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

        return inverted_table

if __name__ == "__main__":
    bm = BooleanMatch()
    print(bm.book_reverted_dict)
    print(bm.movie_reverted_dict)
