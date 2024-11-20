import torch
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from transformers import BertTokenizer, BertModel
import pickle
import json

# 转化时间为天数
def trans_time(data):
    time = pd.to_datetime(data).dt
    year = time.year.values
    month = time.month.values
    day = time.day.values
    combined_list = list(map(lambda a, b, c: a*365 + b*30 + c, year, month, day))
    return combined_list

#进行位置编码
def position_encoding(pos, d_model):
    # pos = torch.arange(time_step, dtype=torch.float32).unsqueeze(1)
    new_pos = pos.unsqueeze(1)
    i = torch.arange(d_model // 2, dtype=torch.float32).unsqueeze(0)
    angle_rates = 1 / torch.pow(10000, (2 * i) / d_model)
    angle_rads = new_pos * angle_rates
    pos_encoding = torch.zeros((4096, d_model))
    pos_encoding[:, 0::2] = torch.sin(angle_rads)
    pos_encoding[:, 1::2] = torch.cos(angle_rads)
    return pos_encoding

# 转化Tag
def extract_tags(root, tag, loaded_data, item):
    topic_list = dict()
    # 配置LDA模型：假设提取3个主题
    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    vectorizer = CountVectorizer()
    
    def print_top_words(i, model, feature_names, n_top_words=5):
        temp = ""
        for topic_idx, topic in enumerate(model.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
            temp = temp + " ".join(top_words)
        topic_list.update({loaded_data[item][i]:temp})
        
    for i in range(len(tag)):
        tag_bow = vectorizer.fit_transform(tag[i])
        lda.fit(tag_bow)
        print_top_words(i, lda, vectorizer.get_feature_names_out())
    with open(root + item + '_tag.json', 'w', encoding="UTF-8") as f:
        json.dumps(topic_list, indent=4, fp=f)
    return topic_list

# 生成向量, item 代表着是书还是电影
def trans2vec(root, topic_list, item):
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    model = BertModel.from_pretrained('bert-base-chinese')
    tag_embedding_dict = {}
    with torch.no_grad():
        for index, tag_str in topic_list.items():
            # 将标签列表转换为字符串
            # 使用BERT中文模型对标签进行编码
            inputs = tokenizer(tag_str, truncation=True, return_tensors='pt')
            outputs = model(inputs.input_ids, inputs.token_type_ids, inputs.attention_mask)
            # 使用最后一层的平均隐藏状态作为标签的向量表示
            tag_embedding = outputs.last_hidden_state.mean(dim=1).cpu()
            tag_embedding_dict[index] = tag_embedding
    with open(root + item + '_tag_embedding_dict.pkl', 'wb') as f:
        pickle.dump(tag_embedding_dict, f)
            
    