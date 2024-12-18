import os
import matplotlib.pyplot as plt

# 创建保存图像的文件夹
output_dir = "output_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 数据
learning_rates = ['1e-2', '1e-4', '1e-3']
l2_values = ['1e-4', '1e-5', '1e-3', '5e-5', '2e-4']
results = {
    'Recall@5': [
        [0.0504, 0.0497, 0.0523, 0.0500, 0.0501],
        [0.0686, 0.0682, 0.0687, 0.0682, 0.0687],
        [0.0641, 0.0656, 0.0654, 0.0658, 0.0656]
    ],
    'NDCG@5': [
        [0.2434, 0.2418, 0.2463, 0.2428, 0.2289],
        [0.3117, 0.3107, 0.3151, 0.3109, 0.3118],
        [0.3070, 0.3044, 0.3059, 0.3046, 0.3038]
    ],
    'Recall@10': [
        [0.0908, 0.0902, 0.0911, 0.0906, 0.0879],
        [0.1167, 0.1154, 0.1180, 0.1153, 0.1172],
        [0.1053, 0.1152, 0.1156, 0.1151, 0.1149]
    ],
    'NDCG@10': [
        [0.2293, 0.2290, 0.2345, 0.2291, 0.2214],
        [0.2874, 0.2865, 0.2880, 0.2861, 0.2882],
        [0.2763, 0.2812, 0.2828, 0.2817, 0.2815]
    ]
}

# 定义绘图函数
def plot_metric(metric_name, metric_data):
    plt.figure()
    for i, lr in enumerate(learning_rates):
        plt.plot(l2_values, metric_data[i], marker='o', label=f'lr={lr}')
    plt.title(metric_name)
    plt.xlabel('L2 Value')
    plt.ylabel(metric_name)
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{metric_name}.png'))

# 绘制并保存所有指标图像
for metric_name, metric_data in results.items():
    plot_metric(metric_name, metric_data)
