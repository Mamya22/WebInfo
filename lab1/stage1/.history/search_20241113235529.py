# 布尔查询优化
# 优先查询较小频率的词条
# ID升序排列

import json
from typing import AnyStr, Dict, List, Tuple
from colorama import Fore, Style

class BooleanMatch:
    def __init__(self):
        self.query = "" # 查询语句
        self.query
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

        self.book_keyword+path = "./result/book_keyword.json"
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
