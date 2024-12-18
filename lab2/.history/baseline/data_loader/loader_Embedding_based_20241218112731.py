import os
import random
import collections

import torch
import numpy as np
import pandas as pd

from data_loader.loader_base import DataLoaderBase


class DataLoader(DataLoaderBase):

    def __init__(self, args, logging):
        super().__init__(args, logging)

        self.cf_batch_size = args.cf_batch_size
        self.kg_batch_size = args.kg_batch_size
        self.test_batch_size = args.test_batch_size

        kg_data = self.load_kg(self.kg_file)
        print("loader:kg_data: ", kg_data['r'])
        self.construct_data(kg_data)
        self.print_info(logging)

    def construct_data(self, kg_data):
        '''
            kg_data 为 DataFrame 类型
        '''

        # 1. 为KG添加逆向三元组，即对于KG中任意三元组(h, r, t)，添加逆向三元组 (t, r+n_relations, h)，
        #    并将原三元组和逆向三元组拼接为新的DataFrame，保存在 self.kg_data 中。
        # 获取relation的数量
        n_relations = max(kg_data['r']) + 1
        print("n_relations: ", n_relations)
        new_kg_data = kg_data.copy()
        # 交换h和t
        new_kg_data[['h', 't']] = new_kg_data[['t', 'h']]
        # 更新关系
        new_kg_data['r'] = new_kg_data['r'] + n_relations
        self.kg_data = pd.concat([kg_data, new_kg_data], axis=0, ignore_index=True)


        # 2. 计算关系数，实体数和三元组的数量
        self.n_relations = max(self.kg_data['r']) + 1
        self.n_entities = pd.concat([self.kg_data['h'], self.kg_data['r']]).nunique()
        self.n_kg_data = len(self.kg_data)

        # 3. 根据 self.kg_data 构建字典 self.kg_dict ，其中 key 为 h，value 为 tuple(t, r)，
        #    和字典 self.relation_dict，其中 key 为 r，value 为 tuple(h, t)。
        self.kg_dict = collections.defaultdict(list)
        self.relation_dict = collections.defaultdict(list)

        # 遍历 DataFrame 的每一行
        for _, row in self.kg_data.iterrows():
            head = row['h']
            relation = row['r']
            tail = row['t']

            # 对 self.kg_dict 进行更新
            self.kg_dict[head].append((tail, relation))

            # 对 self.relation_dict 进行更新
            self.relation_dict[relation].append((head, tail))



    def print_info(self, logging):
        logging.info('n_users:      %d' % self.n_users)
        logging.info('n_items:      %d' % self.n_items)
        logging.info('n_entities:   %d' % self.n_entities)
        logging.info('n_relations:  %d' % self.n_relations)

        logging.info('n_cf_train:   %d' % self.n_cf_train)
        logging.info('n_cf_test:    %d' % self.n_cf_test)

        logging.info('n_kg_data:    %d' % self.n_kg_data)

