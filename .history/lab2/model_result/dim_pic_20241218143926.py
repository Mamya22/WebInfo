import matplotlib.pyplot as plt

# 数据
dims = [16, 24, 32, 48, 64]
recall_at_5 = [0.0685, 0.0682, 0.0641, 0.0654, 0.0639]
ndcg_at_5 = [0.3030, 0.3146, 0.3070, 0.2960, 0.1085]
recall_at_10 = [0.1132, 0.1151, 0.1053, 0.1092, 0.2904]
ndcg_at_10 = [0.2774, 0.2852, 0.2763, 0.2735, 0.2687]

# Recall@5
plt.figure()
plt.plot(dims, recall_at_5, marker='o')
plt.title('Recall@5')
plt.xlabel('Dimension')
plt.ylabel('Recall@5')
plt.savefig('Recall_at_5.png')

# NDCG@5
plt.figure()
plt.plot(dims, ndcg_at_5, marker='o')
plt.title('NDCG@5')
plt.xlabel('Dimension')
plt.ylabel('NDCG@5')
plt.savefig('NDCG_at_5.png')

# Recall@10
plt.figure()
plt.plot(dims, recall_at_10, marker='o')
plt.title('Recall@10')
plt.xlabel('Dimension')
plt.ylabel('Recall@10')
plt.savefig('Recall_at_10.png')

# NDCG@10
plt.figure()
plt.plot(dims, ndcg_at_10, marker='o')
plt.title('NDCG@10')
plt.xlabel('Dimension')
plt.ylabel('NDCG@10')
plt.savefig('NDCG_at_10.png')
