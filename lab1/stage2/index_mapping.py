"""
借鉴示例代码，进行编号的映射
"""
from torch.utils.data import Dataset

class IndexMapping(Dataset):
    def __init__(self, data, user_list, item_list, user, item, tag_embedding_dict):
        self.data = data
        self.user = user  # 定义user列的表头
        self.item = item  # 定义item的属性
        self.user_to_index, self.index_to_id = self.create_id_mapping(user_list)
        self.item_to_index, self.index_to_item = self.create_id_mapping(item_list)
        self.tag_embedding_dict = tag_embedding_dict
        # self.time_to_index, self.index_to_time = self.create_id_mapping(data['Time'])
        

    def create_id_mapping(self, id_list):
        unique_ids = sorted(set(id_list))
    
        # 创建将原始ID映射到连续索引的字典
        id_to_idx = {id: idx for idx, id in enumerate(unique_ids)}
    
    # 创建将连续索引映射回原始ID的字典
        idx_to_id = {idx: id for id, idx in id_to_idx.items()}
    
        return id_to_idx, idx_to_id
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        row = self.data.iloc[index]
        user = self.user_to_index[row[self.user]]
        book = self.item_to_index[row[self.item]]
        rating = row['Rate'].astype('float32')
        time = row['Time'].astype('float32')
        tag_embed = self.tag_embedding_dict.get(row[self.item])
        return user, book, rating, time, tag_embed
        