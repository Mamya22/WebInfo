import Extract
import Filter

# 获取第一跳过滤后的实体集合
KG_filter_path_1 = './data/KGfilter1.txt'
entities_set_2 = Extract.ExtractKG2Entity(KG_filter_path_1)
print("第一跳过滤后的实体集合提取完成。")

freebase_path = './data/freebase_douban.gz'
KG_path_2 = './data/KGpath2.txt.gz'

# 构建第二跳子图
Extract.ExtractFreebase2gzip(freebase_path, KG_path_2, entities_set_2)
print("第二跳子图构建完成。")

# 第二跳过滤
filter_2 = Filter.Filter(KG_path_2, 10, 20000, 50, 'third')
triple_list_filter_2 = filter_2.filter()
KG_filter_path_2 = './data/KGfilter2.txt'
filter_2.save(KG_filter_path_2)
print("第二跳子图过滤完成。")

# 获取第二跳过滤后的实体集合
entities_set_filter_2, relation_set_filter_2 = Extract.ExtractList2Entity(triple_list_filter_2)
print("第二跳过滤后共有三元组：", len(triple_list_filter_2))
print("第二跳过滤后共有实体：", len(entities_set_filter_2))
print("第二跳过滤后共有关系：", len(relation_set_filter_2))
