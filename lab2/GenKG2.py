import Extract
import Filter

# 读取基础实体数据
base_entities = set()
with open('./data/douban2fb.txt', 'r') as f:
    for line in f.readlines():
        _id, entity = line.strip().split()
        base_entities.add("<http://rdf.freebase.com/ns/{}>".format(entity))
print("获取基础数据完成。")

# 定义文件路径
freebase_path = './data/freebase_douban.gz'
print("开始构建第一跳子图。")
KG_filter_path_1 = './data/KGfilter1.txt'
print("第一跳子图构建完成。")
KG_path_2 = './data/KGpath2.txt.gz'
print("开始构建第二跳子图。")

# 构建第二跳子图
entities_set_2 = Extract.ExtractKG2Entity(KG_filter_path_1)
Extract.ExtractFreebase2gzip(freebase_path, KG_path_2, entities_set_2)
print("第二跳子图构建完成。")
