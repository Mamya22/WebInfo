from data_process import *
import pandas as pd
root = "./dataset/"
# 生成向量
for item in ['Book', 'Movie']:
    loaded_data = pd.read_csv(root + 'selected_' + item.lower() + '_top_1200_data_tag.csv')
    topic_list = extract_tags(root, loaded_data['Tags'], loaded_data, item)
    trans2vec(root, topic_list, item)
# 处理时间
for item in ['Book', 'Movie']:
    loaded_data = pd.read_csv(root + item.lower() + '_score.csv')
    ret_list = trans_time(loaded_data['Time'])
    loaded_data['Time'] = ret_list
    loaded_data.to_csv(root + item.lower() + '_score.csv')
    
    
        

