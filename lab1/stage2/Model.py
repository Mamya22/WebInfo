import torch
import torch.nn as nn
import data_process
# from DNN import TagFeatureExtractor
# class TagBiasSVD(nn.Module):
#     def __init__(self, user_number, item_number, embedding_dim, hidden_state, mean, dropout=0.2):
#         super(TagBiasSVD, self).__init__()
#         self.embedding_dim = embedding_dim
#         self.user_embedding = nn.Embedding(user_number, embedding_dim)
#         self.item_embedding = nn.Embedding(item_number, embedding_dim)
#         # 用户和物品偏差
#         self.user_bias = nn.Embedding(user_number, 1)
#         self.item_bias = nn.Embedding(item_number, 1)
#         # 全局偏差，通常为所有评分的均值
#         self.time_weight = nn.Parameter(torch.FloatTensor([1.0]))
#         self.tag_weight = nn.Parameter(torch.FloatTensor([1.0]))
#         self.global_bias = nn.Parameter(torch.FloatTensor([mean]))
#         self.dropout = nn.Dropout(dropout)
#         self.linear_embedding = nn.Linear(hidden_state, embedding_dim)
#         self.relu = nn.ReLU()
#         self.dnn = nn.Sequential(
#             nn.Linear(embedding_dim * 2, 128),
#             nn.ReLU(),
#             nn.Linear(128, 64),
#             nn.ReLU(),
#             nn.Linear(64, 1),
#         )

#     def forward(self, user_id, item_id, tag_embedding, time=0, Time = False, Tag=True):
#         # print(tag_embed.size())
#         # print(tag_embed.size())
#         book_embedding = self.item_embedding(item_id)
#         user_embed = self.user_embedding(user_id)
#         tag_embedding_2 = self.relu(self.linear_embedding(tag_embedding)).squeeze()
#         # print(tag_embedding_2.size())
#         # 计算用户和物品的嵌入向量之和
#         # self.linear_embedding = nn.Linear(hidden_state, embedding_dim)
#         user_embed = user_embed * tag_embedding_2
#         # if Time:
#         #     time_embed = data_process.position_encoding(time, len, self.embedding_dim)
#         #     book_intergrate = book_intergrate + self.time_weight * time_embed
#         user_embed = self.dropout(user_embed)
#         book_embedding = self.dropout(book_embedding)
#         user_bias = self.user_bias(user_id).squeeze()
#         item_bias = self.item_bias(item_id).squeeze()
#         interaction = torch.cat([user_embed, book_embedding], dim=1)
#         interaction = self.dropout(interaction)
#         # 综合评分
#         score = self.dnn(interaction).squeeze()
#         return score + user_bias + item_bias + self.global_bias

class BiasSVD(nn.Module):
    def __init__(self, user_number, item_number, embedding_dim, hidden_state, mean, dropout=0.2):
        super(BiasSVD, self).__init__()
        self.embedding_dim = embedding_dim
        self.user_embedding = nn.Embedding(user_number, embedding_dim)
        self.item_embedding = nn.Embedding(item_number, embedding_dim)
        # 用户和物品偏差
        self.user_bias = nn.Embedding(user_number, 1)
        self.item_bias = nn.Embedding(item_number, 1)
        # 全局偏差，通常为所有评分的均值
        self.time_weight = nn.Parameter(torch.FloatTensor([1.0]))
        # 应该在这里对tag进行降维
        self.linear = nn.Linear(768, 32)
        self.relu = nn.ReLU()
        self.tag_weight = nn.Parameter(torch.FloatTensor([1.0]))
        self.global_bias = nn.Parameter(torch.FloatTensor([mean]))
        self.dropout = nn.Dropout(dropout)
        self.dnn = nn.Sequential(
            nn.Linear(hidden_state, 128),
            nn.ReLU(),
            nn.Linear(128, 32)
        )

    def forward(self, user_id, item_id, tag_embedding, time=0, Time = False, Tag=False):
        item_embed = self.item_embedding(item_id)
        user_embed = self.user_embedding(user_id)
        user_bias = self.user_bias(user_id).squeeze()
        item_bias = self.item_bias(item_id).squeeze()
        if Time and not Tag:
            # print("Time")
            time_embed = data_process.position_encoding(time, self.embedding_dim)
            item_embed = item_embed + self.time_weight * time_embed
        elif Tag and not Time:
            tag_embed = self.dnn(tag_embedding).squeeze()
            # user_embed = user_embed * tag_embed
            item_embed = item_embed * tag_embed
        elif Tag and Time:
            # print("Tt")
            time_embed = data_process.position_encoding(time,self.embedding_dim)
            tag_embed = self.dnn(tag_embedding).squeeze()
            inter_embed = item_embed * tag_embed 
            item_embed = inter_embed + self.time_weight * time_embed

        item_embed = self.dropout(item_embed)
        user_embed = self.dropout(user_embed)
        return (user_embed * item_embed).sum(dim=1) + user_bias + item_bias + self.global_bias
