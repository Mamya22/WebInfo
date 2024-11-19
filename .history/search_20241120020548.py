import json
from typing import AnyStr, Dict, List, Tuple
from colorama import Fore, Style
import tkinter as tk
class StatusWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Status & Output Window")
        self.root.geometry("1000x2000")
        # 状态标签和文本框
        self.status_label = tk.Label(self.root, text="Status", font=("Arial", 20))
        self.status_label.pack(pady=10)
        self.status_text = tk.Text(self.root, height=10, width=100)
        self.status_text.pack(pady=10)
        # 结果标签和文本框
        self.result_label = tk.Label(self.root, text="Result", font=("Arial", 20))
        self.result_label.pack(pady=10)
        self.result_text = tk.Text(self.root, height=500, width=100)
        self.result_text.pack(pady=10)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.closed = False
    def on_closing(self):
        self.closed = True
        self.root.destroy()
    def update_status(self, message: str):
        if not self.closed:
            self.status_text.insert(tk.END, message + "\n")
            self.status_text.see(tk.END)
            self.root.update_idletasks()
            self.root.update()
    def update_result(self, message: str):
        if not self.closed:
            self.result_text.insert(tk.END, message + "\n")
            self.result_text.see(tk.END)
            self.root.update_idletasks()
            self.root.update()
    
    def clear_status(self):
        if not self.closed:
            self.status_text.delete(1.0, tk.END)
            self.root.update_idletasks()
            self.root.update()
    def clear_result(self):
        if not self.closed:
            self.result_text.delete(1.0, tk.END)
            self.root.update_idletasks()
            self.root.update()
status_window = StatusWindow()
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
        self.pre_sort_ids = ()
        status_window.clear_status()
        status_window.clear_result()
        status_window.update_status("Welcome to Boolean Match System!")
        status_window.update_status("Please wait for initialization...")
        self.book_keyword_path = "./result/book_keyword_zip.json"
        self.movie_keyword_path = "./result/movie_keyword_zip.json"
        self.book_reverted_dict_path = "./result/book_reverted_dict.json"
        self.movie_reverted_dict_path = "./result/movie_reverted_dict.json"
        self.book_skip_list_path = "./result/book_skip_dict.json"
        self.movie_skip_list_path = "./result/movie_skip_dict.json"
        with open(self.book_keyword_path, "r", encoding="UTF-8") as f:
            self.book_keyword = json.load(f)
        with open(self.movie_keyword_path, "r", encoding="UTF-8") as f:
            self.movie_keyword = json.load(f)
        with open(self.book_reverted_dict_path, "r", encoding="UTF-8") as f:
            self.book_reverted_dict = json.load(f)
        with open(self.movie_reverted_dict_path, "r", encoding="UTF-8") as f:
            self.movie_reverted_dict = json.load(f)
        with open(self.book_skip_list_path, "r", encoding="UTF-8") as f:
            self.book_skip_list = json.load(f)
        with open(self.movie_skip_list_path, "r", encoding="UTF-8") as f:
            self.movie_skip_list = json.load(f)
        status_window.update_status("Initialization Completed! Start your travel")
    # 输出详细信息
    def print_message(self,_id: int,query: List):
        str_id = str(_id)
        if(self.mode == 'book'):
            # book类型检索
            show_tag = self.book_keyword.get(str_id)
            # status_window.update_result("Success! The book you want is here!")
            status_window.update_result("ID:   "+str_id)
            for tag in show_tag:
                for q in query:
                    if(tag == q):
                        status_window.update_result(tag)
            # status_window.update_result("Tag: ")
            # for tag in show_tag:
            #     status_window.update_result(tag)
            # print(Fore.GREEN,"Success! The book you want is here!")
            # print(Fore.BLACK,"ID:   ",_id)
            # print(Fore.GREEN,"Tag: ")
            # print(Fore.BLACK,show_tag)
        else:
            # movie类型检索
            show_tag = self.movie_keyword.get(str_id)
            # status_window.update_result("Success! The movie you want is here!")
            status_window.update_result("ID:   "+str_id)
            for tag in show_tag:
                for q in query:
                    if(tag == q):
                        status_window.update_result(tag)
            # status_window.update_result("Tag: ")
            # for tag in show_tag:
            #     status_window.update_result(tag)
            # print(Fore.GREEN,"Success! The movie you want is here!")
            # print(Fore.BLACK,"ID:   ",_id)
            # print(Fore.GREEN,"Tag: ")
            # print(Fore.Green,show_tag)
        
    def SplitQuery(self) -> List:
        # 划分查询语句
        self.query = self.query.strip()
        self.query = self.query.replace('（', '(').replace('）', ')')
        self.query = self.query.replace('(', ' ( ').replace(')', ' ) ')
        self.query = self.query.upper()
        self.query = self.query.replace('AND', ' AND ').replace('OR', ' OR ').replace('NOT', ' NOT ')
        self.query = self.query.replace('和', ' AND ').replace('且', ' OR ').replace('非', ' NOT ')
        self.query = self.query.replace('&', ' AND ').replace('|', ' OR ').replace('！', ' NOT ').replace('!', ' NOT ')
        status_window.update_status("Success! The query is: " + self.query)
        return self.query.split() # 用空格划分
    
    def FindCorrespondBracket(self, index: int) -> int:
        # 括号处理
        i = index + 1
        flag = 0
        while i < len(self.query_list) and not self.error:
            if flag < 0:
                status_window.update_result("The right bracket overabundant!")
                self.error = True
            elif self.query_list[i] == ')':
                if flag == 0:
                    return i
                else:
                    flag -= 1
            elif self.query_list[i] == '(':
                flag += 1
            i += 1
        status_window.update_result("Lack of right bracket!")
        self.error = True
        return -1
    
    def CreateSkipList(self, id_list: List) -> Dict:
        if len(id_list) == 0:
            self.error = True
            return []
        if not self.error:
            # 没有出错
            interval = int(len(id_list) ** 0.5) # 根号L为间隔
            # 确保跳表间隔至少为1
            skip_list = [[id_list[0]], 0 if len(id_list) == 1 else interval, 0]
            for i in range(interval, len(id_list)-interval, interval):
                # 以间隔为步长，遍历
                skip_list.append([id_list[i], i + interval, i])
            nail = len(skip_list) * interval
            if nail < len(id_list) - 1:
                # 处理结尾
                skip_list.append([id_list[nail], len(id_list)-1, nail])
            return skip_list
    def Search(self, query:AnyStr, modes:AnyStr) -> List:
        status_window.update_status("Begin Searching...")
        self.query = query
        self.mode = modes
        self.query_list = self.SplitQuery()
        if self.error:
            status_window.update_result("Sorry! But there are some errors in your query.")
            self.error = False
            return []
        if self.mode == 'book':
            status_window.update_status("You are searching for books.")
            self.keyword = self.book_keyword
            self.reverted_dict = self.book_reverted_dict
            self.skip_dict = self.book_skip_list
        else:
            status_window.update_status("You are searching for movies.")
            self.keyword = self.movie_keyword
            self.reverted_dict = self.movie_reverted_dict
            self.skip_dict = self.movie_skip_list
        pre_sort_id_list = list(self.keyword.keys())
        # print(pre_sort_id_list)
        pre_sort_id_list.sort() # 对ID进行排序
        self.pre_sort_ids = (pre_sort_id_list, self.CreateSkipList(pre_sort_id_list))
        
        ret,ret_skip_list = self.BracketOperation(self.query_list)
        if len(ret) == 0:
            status_window.update_result("Sorry! But there are no results you want here.")
            self.error = False
            # not find doesn't mean error, but doesn't need to output
        elif not self.error:
            for _id in ret:
                # status_window.update_result("Success! The ID you want is here!")
                self.print_message(_id,self.query_list)
            
        
        return self.error
    def BracketOperation(self, query_list: List) -> Tuple:
        # 处理括号表达式
        status_window.update_status("Begin Bracket Operation...")
        if not query_list:
            return [], []
        ret = []
        index = 0
        while index < len(query_list):
            item = query_list[index]
            if not self.error:
                if item == '(':
                    l_bracket = index
                    r_bracket = self.FindCorrespondBracket(l_bracket) # 找到对应的右括号
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
                    item_skip_list = self.skip_dict
                    item_id_list_and_skip_list = (item_id_list, item_skip_list)
                    ret.append(item_id_list_and_skip_list)
                    index += 1
            else:
                break
        logic_ret = self.LogicOperation(ret)
        status_window.update_status("Bracket Operation Completed!")
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
                status_window.update_result("Lack of some parameters")
                self.error = True
            elif not self.error and len(ret) > 1:
                status_window.update_result("There are some unexpected parameters")
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
            status_window.update_result("The operand 'OR' lacks parameter!")
            self.error = True
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            
            while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                # try_skip for index1
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:
                    if (L1_id_list[index1] == L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] == \
                            L2_id_list[index2]):
                        
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                        index2 += 1
                    elif (index1 // interval_1 in L1_skip_list and
                        L1_id_list[index1] < L2_id_list[index2] and
                        L1_id_list[L1_skip_list[index1 // interval_1][1]] < L2_id_list[index2]):
                        
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                    else:
                        break
                # try_skip for index2
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:
                    if (index2 // interval_2 in L2_skip_list and
                        L2_id_list[index2] == L1_id_list[index1] and
                        L2_id_list[L2_skip_list[index2 // interval_2][1]] == L1_id_list[index1]):
                        
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                        index1 += 1
                    elif (index2 // interval_2 in L2_skip_list and
                        L2_id_list[index2] < L1_id_list[index1] and
                        L2_id_list[L2_skip_list[index2 // interval_2][1]] < L1_id_list[index1]):
                        
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                    else:
                        break
                # Compare elements at index1 and index2
                if index1 < len_1 and index2 < len_2:
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
            # Append remaining elements
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
            status_window.update_status("The operand 'AND' lacks parameter!")
            self.error = True
        if not self.error:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int(len_1 ** 0.5)
            interval_2 = int(len_2 ** 0.5)
            
            while index1 < len_1 and index2 < len_2:
                # try_skip for index1
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:
                    if (L1_id_list[index1] < L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] < \
                            L2_id_list[index2]):
                        
                        index1 = L1_skip_list[index1 // interval_1][1]
                    else:
                        break
                # try_skip for index2
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:
                    if (index2 // interval_2 in L2_skip_list and
                        L2_id_list[index2] < L1_id_list[index1] and
                        L2_id_list[L2_skip_list[index2 // interval_2][1]] < L1_id_list[index1]):
                        
                        index2 = L2_skip_list[index2 // interval_2][1]
                    else:
                        break
                # Compare elements at index1 and index2
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
            status_window.update_status(Fore.RED + "The operand 'NOT' lacks parameter!")
            self.error = True
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            while index1 < len_1 and index2 < len_2:
                # try_skip for index1
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:
                    skip_index1 = index1 // interval_1
                    if (L1_id_list[index1] == L2_id_list[index2] and L1_id_list[L1_skip_list[index1 // interval_1][1]] == \
                            L2_id_list[index2]):
                        index1 += interval_1
                        index2 += 1
                    elif (skip_index1 in L1_skip_list and
                        index1 < len_1 and index2 < len_2 and
                        int(L1_id_list[index1]) < int(L2_id_list[index2]) and
                        skip_index1 < len(L1_skip_list) and
                        L1_skip_list[skip_index1][1] < len_1 and
                        L1_id_list[L1_skip_list[skip_index1][1]] < L2_id_list[index2]):
                        index1 += interval_1
                    else:
                        break
                # try_skip for index2
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:
                    skip_index2 = index2 // interval_2
                    if (skip_index2 in L2_skip_list and
                        index1 < len_1 and index2 < len_2 and
                        L2_id_list[index2] == L1_id_list[index1] and
                        skip_index2 < len(L2_skip_list) and
                        L2_skip_list[skip_index2][1] < len_2 and
                        L2_id_list[L2_skip_list[skip_index2][1]] == L1_id_list[index1]):
                        index2 += interval_2
                        index1 += 1
                    elif (skip_index2 in L2_skip_list and
                        index2 < len_2 and index1 < len_1 and
                        int(L2_id_list[index2]) < int(L1_id_list[index1]) and
                        skip_index2 < len(L2_skip_list) and
                        L2_skip_list[skip_index2][1] < len_2 and
                        L2_id_list[L2_skip_list[skip_index2][1]] < L1_id_list[index1]):
                        index2 += interval_2
                    else:
                        break
                # Compare elements at index1 and index2
                if index1 < len_1 and index2 < len_2:
                    try:
                        val1 = int(L1_id_list[index1])
                        val2 = int(L2_id_list[index2])
                    except ValueError:
                        print(f"Skipping invalid comparison: {L1_id_list[index1]}, {L2_id_list[index2]}")
                        if isinstance(L1_id_list[index1], str):
                            index1 += 1
                        if isinstance(L2_id_list[index2], str):
                            index2 += 1
                        continue
                    if val1 == val2:
                        index1 += 1
                        index2 += 1
                    elif val1 < val2:
                        ret.append(L1_id_list[index1])
                        index1 += 1
                    else:
                        index2 += 1
            # Append remaining elements from L1_id_list
            if index1 < len(L1_id_list):
                ret.extend(L1_id_list[index1:])
        return ret, self.CreateSkipList(ret)
    def NOT(self, T: Tuple) -> Tuple:
        return self.AND_NOT(self.pre_sort_ids, T)
def start_tkinter():
    bm = BooleanMatch()
    def search():
        status_window.clear_status()
        status_window.clear_result()
        user_mode = mode_entry.get()
        if(user_mode != '1' and user_mode != '2'):
            result_label.config(text="Invalid mode.", fg="red")
            return
        if(user_mode == '1'):
            user_mode = 'movie'
        else:
            user_mode = 'book'
        print(user_mode)
        user_query = query_entry.get()
        error = bm.Search(user_query, user_mode)
        print(user_query)
        if error:
            result_label.config(text="Some error occurred in your query.", fg="red")
        else:
            result_label.config(text="Search completed.", fg="green")
    root = tk.Tk()
    root.title("Boolean Match System")
    root.geometry("1000x500")
    tk.Label(root, text="Enter mode(movie——1/book——2):",font=("Arival",30)).pack()
    mode_entry = tk.Entry(root, width=100,font=("Arival",30))
    mode_entry.pack()
    tk.Label(root, text="Enter query:",font=("Arival",30)).pack()
    query_entry = tk.Entry(root, width=100,font=("Arival",30))
    query_entry.pack()
    search_button = tk.Button(root, text="Search",font=("Arival",30))
    search_button.pack()
    result_label = tk.Label(root, text="")
    result_label.pack()
    search_button.config(command=search)
    results_text = tk.Text(root, height=20, width=100, font=("Arial", 20))
    results_text.pack()
    root.mainloop()
if __name__ == "__main__":
    start_tkinter()