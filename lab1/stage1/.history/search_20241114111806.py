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
        # self.book_compressed_revert_dict_path = "./result/book_compressed_revert_dict.bin"
        # self.movie_compressed_revert_dict_path = "./result/movie_compressed_revert_dict.bin"
        self.book_skip_list_path = "./result/book_skip_dict.json"
        self.movie_skip_list_path = "./result/movie_skip_dict.json"


        with open(self.book_keyword_path, "r", encoding="UTF-8") as f:
            self.book_keyword = json.load(f)

        with open(self.movie_keyword_path, "r", encoding="UTF-8") as f:
            self.movie_keyword = json.load(f)

        # self.book_reverted_dict = self.decompress(self.book_compressed_revert_dict_path)
        # self.movie_reverted_dict = self.decompress(self.movie_compressed_revert_dict_path)
        with open(self.book_skip_list_path, "r", encoding="UTF-8") as f:
            self.book_skip_list = json.load(f)
        with open(self.movie_skip_list_path, "r", encoding="UTF-8") as f:
            self.movie_skip_list = json.load(f)
        print(Fore.GREEN + "Initialization Completed! Start your travel" + Style.RESET_ALL)

    # def decompress(self, compress_path) -> Dict:
    #     with open(compress_path, 'rb') as f_compress:
    #         contents_bytes = f_compress.read()
    #         contents_list = [] # 最终结果
    #         content_list = [] # 当前处理的一组字节
    #         for byte in contents_bytes:
    #             if byte >> 7 == 0: # 最高位为0
    #                 content_list.append(byte) # 直接追加
    #             else:
    #                 content_list.append(byte & 0x7f) # 取低7位
    #                 contents_list.append(content_list)
    #                 content_list = [] # 重置

    #     inverted_table = {} # 存储最终倒排索引表
    #     content_index = 0 # 当前处理的字节索引

    #     while content_index < len(contents_list):
    #         # 遍历content_list
    #         key_bytes = contents_list[content_index]
    #         key = ''.join([chr(b) for b in key_bytes]).strip() # 字节转换成字符串形式的key
    #         content_index += 1

    #         # 读取文档ID列表，直到找到一个特殊的终止符，如0字节
    #         doc_ids = [] # 当前关键词的文档ID列表
    #         while content_index < len(contents_list) and contents_list[content_index][0] != 0:
    #             id_bytes = contents_list[content_index]
    #             doc_id = 0
    #             for j in range(len(id_bytes)):
    #                 doc_id += id_bytes[len(id_bytes) - 1 - j] << (j * 7)
    #             if doc_ids:
    #                 doc_id += doc_ids[-1]
    #             doc_ids.append(doc_id)
    #             content_index += 1
            
    #         # 跳过特殊终止符
    #         content_index += 1
            
    #         inverted_table[key] = doc_ids

    #     return inverted_table # 返回索引表
    
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
        # 划分查询语句
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
    
    # def CreateSkipList(self, L: List) -> List:
    #     if len(L) == 0:
    #         self.error = True
    #         return []
    #     if not self.error:
    #         interval = int(len(L) ** 0.5)
    #         skip_list = [[L[0], 0 if len(L) == 1 else interval, 0]]  # avoid len(L) == 1
    #         for i in range(interval, len(L) - interval, interval):
    #             skip_list.append([L[i], i + interval, i])
    #         last = len(skip_list) * interval
    #         if last < len(L) - 1:
    #             skip_list.append([(L[last]), len(L) - 1, last])
    #         return skip_list
        
    def Search(self,query:AnyStr,modes:AnyStr) -> List:
        self.query = query
        self.mode = modes
        self.query_list = self.SplitQuery()
        if self.error:
            return []
        if self.mode == 'book':
            self.keyword = self.book_keyword
            self.skip_dict = self.book_skip_list
        else:
            self.keyword = self.movie_keyword
            self.skip_dict = self.movie_skip_list
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

    def BracketOperation(self, query_list: List) -> Tuple:
        # 处理括号表达式
        if not query_list:
            return [], []
        ret = []
        index = 0
        while index < len(query_list):
            item = query_list[index]
            if not self.error:
                if item == '(':
                    l_bracket = index
                    r_bracket = self.FindCorrespondBracket(l_bracket)
                    if not self.error:
                        ret.append(self.BracketOperation(query_list[l_bracket + 1: r_bracket]))
                        index = r_bracket + 1
                    else:
                        index += 1
                elif item == 'AND' or item == 'OR' or item == 'NOT':
                    ret.append(item)
                    index += 1
                else:
                    item_id_list = self.reverted_dict[item] if item in self.reverted_dict.keys() else []
                    item_skip_list = self.CreateSkipList(item_id_list)
                    item_id_list_and_skip_list = (item_id_list, item_skip_list)
                    ret.append(item_id_list_and_skip_list)
                    index += 1
            else:
                break
        logic_ret = self.LogicOperation(ret)

        return logic_ret

    def LogicOperation(self, ret: List) -> Tuple:
        if 'OR' in ret:
            or_list = []
            for loc, val in enumerate(ret):
                if val == 'OR':
                    or_list.append(loc)
            last_or_index = or_list[-1]
            return self.OR(self.LogicOperation(ret[: last_or_index]), self.LogicOperation(ret[last_or_index + 1:]))
        elif 'AND' in ret:
            and_list = []
            for loc, val in enumerate(ret):
                if val == 'AND':
                    and_list.append(loc)
            last_and_index = and_list[-1]
            if ret[last_and_index + 1] == 'NOT':
                if ret[last_and_index + 2] != 'NOT':
                    return self.AND_NOT(self.LogicOperation(ret[: last_and_index]),
                                        self.LogicOperation(ret[last_and_index + 2:]))
            return self.AND(self.LogicOperation(ret[: last_and_index]),
                            self.LogicOperation(ret[last_and_index + 1:]))
        elif 'NOT' in ret:
            first_not_index = ret.index('NOT')
            if ret[first_not_index + 1] == 'NOT':
                if ret[first_not_index + 2] != 'NOT':
                    return self.LogicOperation(ret[first_not_index + 2:])
            else:
                return self.NOT(self.LogicOperation(ret[first_not_index + 1:]))
        else:
            if not self.error and len(ret) == 0:
                print(Fore.RED + "Lack of some parameters")
                self.error = True
            elif not self.error and len(ret) > 1:
                print(Fore.RED + "There are some unexpected parameters")
                self.error = True
            if not self.error:
                return ret[0]
            else:
                return [], []
            
        def OR(self, T1: Tuple, T2: Tuple) -> Tuple:
            ret = []
            L1_id_list = T1[0]
            L2_id_list = T2[0]
            L1_skip_list = T1[1]
            L2_skip_list = T2[1]
            if not L1_id_list or not L2_id_list:
                print(Fore.RED + "The operand 'OR' lacks parameter!")
                self.error = True
            else:
                index1 = 0
                index2 = 0
                len_1 = len(L1_id_list)
                len_2 = len(L2_id_list)
                interval_1 = int((len(L1_id_list)) ** 0.5)
                interval_2 = int((len(L2_id_list)) ** 0.5)
                while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                    while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                        if L1_id_list[index1] == L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] == \
                                L2_id_list[index2]:
                            ret.extend(L1_id_list[index1: index1 + interval_1])
                            index1 += interval_1
                            index2 += 1
                        elif L1_id_list[index1] < L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] < \
                                L2_id_list[index2]:
                            ret.extend(L1_id_list[index1: index1 + interval_1])
                            index1 += interval_1
                        else:
                            break  # fail skip
                    while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                        if L2_id_list[index2] == L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] == \
                                L1_id_list[index1]:
                            ret.extend(L2_id_list[index2: index2 + interval_2])
                            index2 += interval_2
                            index1 += 1
                        elif L2_id_list[index2] < L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] < \
                                L1_id_list[index1]:
                            ret.extend(L2_id_list[index2: index2 + interval_2])
                            index2 += interval_2
                        else:
                            break  # fail skip

                    if L1_id_list[index1] == L2_id_list[index2]:
                        ret.append(L1_id_list[index1])
                        index1 += 1
                        index2 += 1
                    elif L1_id_list[index1] < L2_id_list[index2]:
                        ret.append(L1_id_list[index1])
                        index1 += 1
                    else:
                        ret.append(L2_id_list[index2])
                        index2 += 1

                if index1 < len(L1_id_list):
                    ret.extend(L1_id_list[index1:])
                if index2 < len(L2_id_list):
                    ret.extend(L2_id_list[index2:])

            return ret, self.CreateSkipList(ret)
        
        def AND(self, T1: Tuple, T2: Tuple) -> Tuple:
            ret = []
            L1_id_list = T1[0]
            L1_skip_list = T1[1]
            L2_id_list = T2[0]
            L2_skip_list = T2[1]
            if not L1_id_list or not L2_id_list:
                print(Fore.RED + "The operand 'AND' lacks parameter!")
                self.error = True
            if not self.error:
                index1 = 0
                index2 = 0
                len_1 = len(L1_id_list)
                len_2 = len(L2_id_list)
                interval_1 = int((len(L1_id_list)) ** 0.5)
                interval_2 = int((len(L2_id_list)) ** 0.5)
                while index1 < len_1 and index2 < len_2:
                    # try_skip
                    while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                        if L1_id_list[index1] < L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] < \
                                L2_id_list[index2]:
                            index1 = L1_skip_list[index1 // interval_1][1]
                        else:
                            break
                    while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                        if L2_id_list[index2] < L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] < \
                                L1_id_list[index1]:
                            index2 = L2_skip_list[index2 // interval_2][1]
                        else:
                            break

                    if L1_id_list[index1] == L2_id_list[index2]:
                        ret.append(L1_id_list[index1])
                        index1 += 1
                        index2 += 1
                    elif L1_id_list[index1] < L2_id_list[index2]:
                        index1 += 1
                    else:
                        index2 += 1

            return ret, self.CreateSkipList(ret)
        
        def AND_NOT(self, T1: Tuple, T2: Tuple) -> Tuple:
            ret = []
            L1_id_list = T1[0]
            L2_id_list = T2[0]
            L1_skip_list = T1[1]
            L2_skip_list = T2[1]
            if not L1_id_list or not L2_id_list:
                print(Fore.RED + "The operand 'NOT' lacks parameter!")
                self.error = True
            else:
                index1 = 0
                index2 = 0
                len_1 = len(L1_id_list)
                len_2 = len(L2_id_list)
                interval_1 = int((len(L1_id_list)) ** 0.5)
                interval_2 = int((len(L2_id_list)) ** 0.5)
                while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                    while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                        if L1_id_list[index1] == L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] == \
                                L2_id_list[index2]:
                            index1 += interval_1
                            index2 += 1
                        elif L1_id_list[index1] < L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] < \
                                L2_id_list[index2]:
                            index1 += interval_1
                        else:
                            break  # fail skip
                    while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                        if L2_id_list[index2] == L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] == \
                                L1_id_list[index1]:
                            index2 += interval_2
                            index1 += 1
                        elif L2_id_list[index2] < L1_id_list[index1] and L2_id_list[L2_skip_list[index2 // interval_2][1]] < \
                                L1_id_list[index1]:
                            index2 += interval_2
                        else:
                            break  # fail skip

                    if L1_id_list[index1] == L2_id_list[index2]:
                        index1 += 1
                        index2 += 1
                    elif L1_id_list[index1] < L2_id_list[index2]:
                        ret.append(L1_id_list[index1])
                        index1 += 1
                    else:
                        index2 += 1

                if index1 < len(L1_id_list):
                    ret.extend(L1_id_list[index1:])

            return ret, self.CreateSkipList(ret)

    def NOT(self, T: Tuple) -> Tuple:
        return self.AND_NOT(self.pre_sort_ids, T)

    

if __name__ == "__main__":
    bm = BooleanMatch()
    # print(bm.book_reverted_dict)
    # print(bm.movie_reverted_dict)
    while True:
        while True:
            user_mode = input(Fore.BLACK +
                              "Please input which mode you'll search: " + Fore.GREEN + "book / movie? ")
            if user_mode == 'book' or user_mode == 'movie':
                break
            else:
                print(Fore.RED + "Some error! Please be care that you can only choose 'book' or 'movie'!")

        user_query = input(Fore.BLACK + "Please input the sequence you'll search: ")

        error = bm.Search(user_query, user_mode)

        if error:
            next_choice = input(Fore.BLACK + "Maybe search for something else?" + Fore.GREEN + "[Y/n] ")
        else:
            next_choice = input(Fore.BLACK + "Continue?" + Fore.GREEN + "[Y/n] ")

        if next_choice == 'n':
            print(
                Fore.BLUE + "Thank you for using this searching engine! Welcome your next travel!")
            break
