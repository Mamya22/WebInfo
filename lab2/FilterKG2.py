import Filter
import Extract

base_entities = set()
with open('./data/douban2fb.txt', 'r') as f:
    for i in f.readlines():
        _id, entity = i.strip().split()
        base_entities.add("<http://rdf.freebase.com/ns/{}>".format(entity))
print("获取基础数据完成。")

KG_path_2 = './data/KGpath2.txt.gz'

filter_2 = Filter.Filter(KG_path_2, 10, 20000, 50, 'second')

entities_set_filter_2, relation_set_filter_2 = Extract.ExtractList2Entity(
    filter_2.triple_list)
for i in base_entities:
    assert (i in entities_set_filter_2)
print("第二跳子图验证完成。")
print("第二跳共有三元组：", len(filter_2.triple_list))
print("第二跳共有实体：", len(entities_set_filter_2))
print("第二跳共有关系：", len(relation_set_filter_2))

triple_list_2 = filter_2.filter()
KG_filter_path_2 = './data/KGfilter2.txt'
filter_2.save(KG_filter_path_2)
print("第二跳子图过滤完成。")

entities_set_filter_2, relation_set_filter_2 = Extract.ExtractList2Entity(
    triple_list_2)
print("第二跳过滤后共有三元组：", len(triple_list_2))
print("第二跳过滤后共有实体：", len(entities_set_filter_2))
print("第二跳过滤后共有关系：", len(relation_set_filter_2))