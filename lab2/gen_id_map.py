kg_path = './data/KGfilter1.txt'
douban2fb_path = './data/douban2fb.txt'
movie_id_map_path = './data/movie_id_map.txt'
kg_final_path = './baseline/data/Douban/kg_final.txt'

# 将 Douban ID 映射到 Freebase ID
douban2fb = {}
with open(douban2fb_path, 'r') as f:
    for line in f:
        line = line.strip().split()
        douban2fb[line[0]] = line[1]

# 将电影的 Douban ID 映射到 指定范围
movie_id_map = {}
with open(movie_id_map_path, 'r') as f:
    for line in f:
        line = line.strip().split()
        movie_id_map[line[0]] = line[1]

entity2id = {}
for douban_id, fb_id in douban2fb.items():
    _id = movie_id_map[douban_id]
    entity = "<http://rdf.freebase.com/ns/{}>".format(fb_id)
    entity2id[entity] = _id

entities = set()
relations = set()
triplet_num = 0
with open(kg_path, 'r') as f:
    for line in f:
        triplet_num += 1
        triplet = line.strip().split('\t')
        entities.add(triplet[0])
        entities.add(triplet[2])
        relations.add(triplet[1])

entities2id = {}
num_of_entities = 578
for entity in entities:
    if entity in entity2id.keys():# 将电影实体的 ID 映射到[0, num of movies)范围内
        entities2id[entity] = entity2id[entity]
    else:# 将图谱中的其余实体映射到[num of movies, num of entities)范围内
        entities2id[entity] = str(num_of_entities)
        num_of_entities += 1

num_of_relations = 0
relations2id = {}
for relation in relations:#将关系映射到[0, num of relations)范围内
    relations2id[relation] = str(num_of_relations)
    num_of_relations += 1

#保存由索引值组成的三元组到文件
with open(kg_path, 'r') as fin:
    with open(kg_final_path, 'w') as fout:
        for line in fin:
            triplet = line.strip().split('\t')
            triplet[0] = entities2id[triplet[0]]
            triplet[1] = relations2id[triplet[1]]
            triplet[2] = entities2id[triplet[2]]
            fout.write('\t'.join(triplet) + '\n')

#保存实体和关系的 ID 映射到文件
entity2id_path = './data/entity2id.txt'
relation2id_path = './data/relation2id.txt'
with open(entity2id_path, 'w') as f:
    for entity, _id in entities2id.items():
        f.write(entity + '\t' + _id + '\n')

with open(relation2id_path, 'w') as f:
    for relation, _id in relations2id.items():
        f.write(relation + '\t' + _id + '\n')