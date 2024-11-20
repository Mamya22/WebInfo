import json
root = "./result/"
# 按块存储

def compress_block(dict_list, block=4):
    dict_string = ""
    # 生成词项字符串
    i = 0
    # 记录生成字典字符串的指针位置
    dict_ptr = []
    for dict in dict_list:
        if i == 0:
            dict_ptr.append(len(dict_string))
        dict_string = dict_string + str(len(dict)) + ''.join(map(str, dict))
        i = (i + 1) % block
    return dict_ptr, dict_string

# 可变长度编码
def compress_encode(doc_ids) -> bytes:
    # 计算文档id间距
    size = len(doc_ids)
    for i in range(size-1,0,-1):
        doc_ids[i] = doc_ids[i] - doc_ids[i-1]
    # 将数据转化为bit
    encode_doc = []
    for i in range(size):
        bit = []
        while doc_ids[i] >= 128: # 7位划分
            low7bit = doc_ids[i] % 128
            bit.insert(0, low7bit)
            doc_ids[i] = doc_ids[i] // 128
        if doc_ids[i] > 0:
            bit.insert(0, doc_ids[i])
        bit[-1] = bit[-1] + 128
        for k in range(len(bit)):
            encode_doc.append(bit[k])
    result = bytes(encode_doc)
    return result

if __name__ == "__main__":
    with open(root + "book_reverted_dict.json", "r", encoding="UTF-8") as f:
        revert_dict = json.load(f)
    with open(root + "compressed_revert_dict.bin", "wb") as f:
        for key in revert_dict:
            f.write(compress_encode(list(revert_dict[key])))
        dict_list = [list(revert_dict[key]) for key in revert_dict]
    dict_ptr, dict_string = compress_block(dict_list, 4)
    with open(root + 'block_compressed.json', "w") as f:
        f.write(dict_string)
    




    

