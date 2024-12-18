import matplotlib.pyplot as plt

# 数据
dims = [16, 24, 32, 48, 64]
recall_at_5 = [0.0685, 0.0682, 0.0641, 0.0654, 0.0639]
ndcg_at_5 = [0.3030, 0.3146, 0.3070, 0.2960, 0.1085]
recall_at_10 = [0.1132, 0.1151, 0.1053, 0.1092, 0.2904]
ndcg_at_10 = [0.2774, 0.2852, 0.2763, 0.2735, 0.2687]

# 创建图像
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Recall@5
axs[0, 0].plot(dims, recall_at_5, marker='o')
axs[0, 0].set_title('Recall@5')
axs[0, 0].set_xlabel('Dimension')
axs[0, 0].set_ylabel('Recall@5')

# NDCG@5
axs[0, 1].plot(dims, ndcg_at_5, marker='o')
axs[0, 1].set_title('NDCG@5')
axs[0, 1].set_xlabel('Dimension')
axs[0, 1].set_ylabel('NDCG@5')

# Recall@10
axs[1, 0].plot(dims, recall_at_10, marker='o')
axs[1, 0].set_title('Recall@10')
axs[1, 0].set_xlabel('Dimension')
axs[1, 0].set_ylabel('Recall@10')

# NDCG@10
axs[1, 1].plot(dims, ndcg_at_10, marker='o')
axs[1, 1].set_title('NDCG@10')
axs[1, 1].set_xlabel('Dimension')
axs[1, 1].set_ylabel('NDCG@10')

# 调整布局
plt.tight_layout()
plt.show()
