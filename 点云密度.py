import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取点云文件
pcd = o3d.io.read_point_cloud("D:\Pointcloud File\S526.ply")
# 进行点云去噪
pcd , index = pcd.remove_radius_outlier(nb_points=20, radius=0.05)
#保存去噪后的文件
ply_filename = "D:\Pointcloud File/S526-F.ply"
# 将点云保存为PLY文件
o3d.io.write_point_cloud(ply_filename, pcd)
# 构建KD树以加速最近点搜索
kdtree = o3d.geometry.KDTreeFlann(pcd)
# 初始化一个列表，用于存储每个点的最近邻距离
nearest_neighbor_distances = []
# 初始化变量用于存储最近距离的和和平方和
sum_distances = 0.0
sum_distances_squared = 0.0

for i in range(len(pcd.points)):
    [k, idx, _] = kdtree.search_knn_vector_3d(pcd.points[i], 2)  # 查找2个最近邻点
    if k == 2:
        nearest_neighbor_distance = np.linalg.norm(pcd.points[i] - pcd.points[idx[1]])
        nearest_neighbor_distances.append(nearest_neighbor_distance)

        # 更新最近距离的和和平方和
        sum_distances += nearest_neighbor_distance
        sum_distances_squared += nearest_neighbor_distance ** 2
#计算平均值
average_distance = np.mean(nearest_neighbor_distances)
#计算距离加权
Q_distance=sum_distances_squared/sum_distances
#输出
print(f"平均最近邻距离: {average_distance:.10f} m")
print(f"距离加权: {Q_distance:.10f} m")

# 初始化一个字典，用于存储每个距离值对应的点的数量
distance_count = {}
for i in range(len(pcd.points)):
    [k, idx, _] = kdtree.search_knn_vector_3d(pcd.points[i], 2)  # 查找2个最近邻点
    if k == 2:
        nearest_neighbor_distance = round(np.linalg.norm(pcd.points[i] - pcd.points[idx[1]]), 5)

        # 更新距离值对应的点的数量
        if nearest_neighbor_distance in distance_count:
            distance_count[nearest_neighbor_distance] += 1
        else:
            distance_count[nearest_neighbor_distance] = 1

# 提取距离值和对应的点的数量
distances = list(distance_count.keys())
counts = list(distance_count.values())

# 绘制图表
plt.bar(distances, counts, width=0.0001)  # 调整width以适应您的数据范围
plt.xlabel('lengh')
plt.ylabel('point number')
plt.xlim(0, 0.015)

output_folder = "D:\Output Plot"
output_filename = "distance_distribution2.png"
output_path = os.path.join(output_folder, output_filename)
plt.savefig(output_path)

plt.show()




