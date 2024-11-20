import pandas as pd
from tqdm import tqdm
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import torch.nn as nn
import torch
import numpy as np
from sklearn.metrics import ndcg_score
import argparse
from data_process import *
import pickle
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from index_mapping import IndexMapping
from Model import BiasSVD

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 计算ndcg
def compute_ndcg(group):
    true_ratings = group['true'].tolist()
    pred_ratings = group['pred'].tolist()
    return ndcg_score([true_ratings], [pred_ratings], k = 50)

def split_dataset(loaded_data, tag_embedding_dict, item, mean):
    num_users = loaded_data['User'].nunique()
    num_items = loaded_data[item].nunique()
    # TagModel = TagBiasSVD(num_users, num_items, embedding_dim=32, hidden_state=768, mean=mean)
    BiasModel = BiasSVD(num_users, num_items, embedding_dim=32, hidden_state=768, mean= mean)
    user_ids = loaded_data['User'].unique()
    item_ids = loaded_data[item].unique()
    train_data, test_data = train_test_split(loaded_data, test_size=0.4, random_state=42)
    train_dataset = IndexMapping(train_data, user_ids, item_ids, 'User', item , tag_embedding_dict)
    test_dataset = IndexMapping(test_data, user_ids, item_ids, 'User', item , tag_embedding_dict)
    # 创建训练集和测试集的数据加载器
    train_dataloader = DataLoader(train_dataset, batch_size=4096, shuffle=True, drop_last = True)
    test_dataloader = DataLoader(test_dataset, batch_size=4096, shuffle=False, drop_last = True)
    return train_dataloader, test_dataloader,  BiasModel



root = "./dataset/"
parser = argparse.ArgumentParser()
parser.add_argument("--item", type=str, default="Book", help="choose Book or Movie")
parser.add_argument("--mode", type=str, default="None", help="Time Tag or None or Both")
# parser.add_argument("--vector", type=bool, default="False", help="根据Tag生成向量 True/False")
args = parser.parse_args()

item = ""
if args.item == "Movie":
    item = "Movie"
else:
    item = "Book"

tag_embedding_dict = {}
with open(root + item.lower() + '_tag_embedding_dict.pkl', 'rb') as f:
    tag_embedding_dict = pickle.load(f)
# 读取数据 
loaded_data = pd.read_csv(root + item.lower() + "_score.csv")
scores = np.array(list(loaded_data.loc[:,'Rate']))
mean = np.mean(scores)
train_dataloader, test_dataloader, BiasModel = split_dataset(loaded_data, tag_embedding_dict, item, mean)

model = BiasModel
lr = 0.005
Time = False
Tag = False
if args.mode == "Time":
    Time = True
elif args.mode == "Tag":
    Tag = True
elif args.mode == "Both":
    Time = True
    Tag = True

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = lr)
num_epochs = 20
lambda_u, lambda_b = 0.001, 0.001
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    total_loss_train, total_loss_test = 0.0, 0.0
    for idx, (user_ids, item_ids, ratings, time, tag_embedding) in tqdm(enumerate(train_dataloader)):
        # print(ratings.size())
        predictions = model(user_ids.to(device), item_ids.to(device),tag_embedding.to(device), time.to(device), Time, Tag)
        # 计算损失，需要加上偏置项
        loss = criterion(predictions, ratings.to(device)) + lambda_u * model.user_embedding.weight.norm(2) + lambda_u * model.user_bias.weight.norm(2) + lambda_b * model.item_embedding.weight.norm(2) + lambda_b * model.item_bias.weight.norm(2)
        loss.backward()
        optimizer.step()
        total_loss_train += loss.item()
    output_loss_train = total_loss_train / (idx + 1) 
    results = []
    model.eval()
    # 进行预测
    with torch.no_grad():
        for idx, (user_ids, item_ids, ratings, time, tag_embedding) in enumerate(test_dataloader):
            pred_ratings = model(user_ids.to(device), item_ids.to(device), tag_embedding.to(device) ,time.to(device), Time, Tag)
            loss = criterion(pred_ratings, ratings.to(device))
            total_loss_test += loss.item()
            # 将结果转换为 numpy arrays
            user_ids_np = user_ids.long().cpu().numpy().reshape(-1, 1)
            pred_ratings_np = pred_ratings.cpu().numpy().reshape(-1, 1)
            true_ratings_np = ratings.numpy().reshape(-1, 1)
            # 将这三个 arrays 合并成一个 2D array
            batch_results = np.column_stack((user_ids_np, pred_ratings_np, true_ratings_np))
            # 将这个 2D array 添加到 results
            results.append(batch_results)
        # 将结果的 list 转换为一个大的 numpy array
        results = np.vstack(results)
        # 将结果转换为DataFrame
        results_df = pd.DataFrame(results, columns=['user', 'pred', 'true'])
        results_df['user'] = results_df['user'].astype(int)
        ndcg_scores = results_df.groupby('user').apply(compute_ndcg)
        # 计算平均NDCG
        avg_ndcg = ndcg_scores.mean()
        print(f'Epoch {epoch}, Train loss: {output_loss_train}, Test loss:, {total_loss_test / (idx + 1)}, Average NDCG: {avg_ndcg}')
