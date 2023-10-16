import open3d as o3d
import numpy as np
from sklearn.cluster import KMeans

# 读取点云数据
point_cloud = o3d.io.read_point_cloud(r"C:\cloudsegmentation\S-F.ply")

# 将点云颜色信息和坐标信息转换为NumPy数组
colors = np.asarray(point_cloud.colors)
points = np.asarray(point_cloud.points)

# 使用K-Means聚类算法
kmeans = KMeans(n_clusters=3)  # 请根据需要设置聚类数目
kmeans.fit(colors)

# 获取每个点的所属聚类标签
cluster_labels = kmeans.labels_

# 计算每个聚类的中心颜色
cluster_centers = []
for cluster_id in range(max(cluster_labels) + 1):
    cluster_mask = cluster_labels == cluster_id
    cluster_colors = colors[cluster_mask]
    cluster_center = np.mean(cluster_colors, axis=0)
    cluster_centers.append(cluster_center)

# 按照中心簇的颜色属性进行排序
sorted_cluster_indices = np.argsort(cluster_centers, axis=0)[:, 0]  # 根据R通道的值排序

# 创建一个Open3D点云对象来存储排序后的结果
sorted_point_clouds = [o3d.geometry.PointCloud() for _ in range(len(cluster_centers))]

# 将点云根据排序后的聚类标签分割成多个子点云
for sorted_cluster_id, original_cluster_id in enumerate(sorted_cluster_indices):
    cluster_mask = cluster_labels == original_cluster_id
    sorted_cluster_colors = colors[cluster_mask]
    sorted_cluster_points = points[cluster_mask]

    # 创建一个Open3D点云对象
    sorted_point_cloud = o3d.geometry.PointCloud()
    sorted_point_cloud.colors = o3d.utility.Vector3dVector(sorted_cluster_colors)
    sorted_point_cloud.points = o3d.utility.Vector3dVector(sorted_cluster_points)

    sorted_point_clouds[sorted_cluster_id] = sorted_point_cloud

# 可以将排序后的结果可视化
o3d.visualization.draw_geometries(sorted_point_clouds)

# 将排序后的聚类结果保存为PLY文件，保留颜色和坐标信息
for sorted_cluster_id, sorted_cluster_point_cloud in enumerate(sorted_point_clouds):
    o3d.io.write_point_cloud(f"C:\cloudsegmentation\S-KMeans-Sorted{sorted_cluster_id}.ply", sorted_cluster_point_cloud)
