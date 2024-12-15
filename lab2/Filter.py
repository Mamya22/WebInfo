from typing import Dict, List
import gzip


class Filter:
    def __init__(self, KG_path, entities_min, entities_max, relation_min, mode='first'):
        self.entities_min = entities_min
        self.entities_max = entities_max
        self.relation_min = relation_min
        self.KG_path = KG_path
        self.mode = mode
        self.triple_list = self.__get_triple_set()
        self.entities_count, self.relation_count = self.__get_count()

    # 从三元组文件中读取三元组
    def __get_triple_set(self) -> List:
        if self.mode == 'first':
            #文本格式
            with open(self.KG_path, 'r', encoding='utf-8') as f:
                triple_list = [line.strip().split('\t') for line in f.readlines()]
            assert triple_list
            return triple_list
        else:
            #gzip格式
            with gzip.open(self.KG_path, 'rb') as f:
                triple_list = [line.strip().decode().strip().split('\t') for line in f.readlines()]
            assert triple_list
            return triple_list

    #计算实体和关系的出现次数
    def __get_count(self) -> (Dict, Dict):
        entities_count = {}
        relation_count = {}
        for triplet in self.triple_list:
            entities_count[triplet[0]] = entities_count.get(triplet[0], 0) + 1
            entities_count[triplet[2]] = entities_count.get(triplet[2], 0) + 1
            relation_count[triplet[1]] = relation_count.get(triplet[1], 0) + 1
        return entities_count, relation_count

    #筛选出头实体和尾实体都以 <http://rdf.freebase.com/ns/ 开头的三元组。
    def __filter_prefix(self):
        prefix = '<http://rdf.freebase.com/ns/'
        triple_list_filter_prefix = [triplet for triplet in self.triple_list if
                                     triplet[0].startswith(prefix) and triplet[2].startswith(prefix)]
        return triple_list_filter_prefix

    # 根据实体出现次数的指定范围过滤三元组。
    def __filter_entities(self):
        triple_list_filter_entities = []
        for triplet in self.triple_list:
            if (self.entities_min <= self.entities_count[triplet[0]] <= self.entities_max) and (
                    self.entities_min <= self.entities_count[triplet[2]] <= self.entities_max):
                triple_list_filter_entities.append(triplet)
        return triple_list_filter_entities

    # 根据关系出现次数过滤三元组。
    def __filter_relations(self):
        triple_filter_relation = [triplet for triplet in self.triple_list if
                                  self.relation_count[triplet[1]] >= self.relation_min]
        return triple_filter_relation

    def filter(self):
        self.triple_list = self.__filter_prefix()
        self.triple_list = self.__filter_relations()
        self.triple_list = self.__filter_entities()
        return self.triple_list

    def save(self, save_path):
        with open(save_path, "w", encoding='utf-8') as f:
            for triplet in self.triple_list:
                f.write('\t'.join(triplet) + '\n')