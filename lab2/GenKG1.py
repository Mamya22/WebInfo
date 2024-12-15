import Extract
import Filter


freebasepath = './data/freebase_douban.gz'
douban2fbpath = './data/douban2fb.txt'
KGpath = './data/KGpath1.txt.gz'
entities_set = Extract.ExtractId2Entity(douban2fbpath)
Extract.ExtractFreebase2gzip(freebasepath, KGpath, entities_set)
print("第一跳子图构建完成。")

filter = Filter.Filter(KGpath, 10, 20000, 50, 'second')

entities_set, relation_set = Extract.ExtractList2Entity(filter.triple_list)
print("第一跳共有三元组：", len(filter.triple_list))
print("第一跳共有实体：", len(entities_set))
print("第一跳共有关系：", len(relation_set))

triple_list_filter = filter.filter()
KG_filter_path = './data/KGfilter1.txt'
filter.save(KG_filter_path)
print("第一跳子图过滤完成。")

entities_set_filter, relation_set_filter = Extract.ExtractList2Entity(triple_list_filter)
print("第一跳过滤后共有三元组：", len(triple_list_filter))
print("第一跳过滤后共有实体：", len(entities_set_filter))
print("第一跳过滤后共有关系：", len(relation_set_filter))

# 第一跳子图构建完成。
# 第一跳共有三元组： 502128
# 第一跳共有实体： 308789
# 第一跳共有关系： 452
# 第一跳子图过滤完成。
# 第一跳过滤后共有三元组： 47457
# 第一跳过滤后共有实体： 1352
# 第一跳过滤后共有关系： 64