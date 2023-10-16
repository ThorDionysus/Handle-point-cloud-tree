import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

# 读取点云数据
pcd = o3d.io.read_point_cloud(r"E:\cloudsegmentation\S-1.ply")

# 将点云转换为NumPy数组
points = np.asarray(pcd.points)
points = points[np.argsort(points[:, 2])]
# 定义n，表示要比较的后n个点
n = 1600  # 可以根据需要修改n的值

# 获取前n个点
selected_points = points[:n]

# 计算边界框的最小和最大坐标
min_x, min_y = np.min(selected_points[:, :2], axis=0)
max_x, max_y = np.max(selected_points[:, :2], axis=0)

lowest_points = points[np.argsort(points[:, 2])[:50]]
avg_lowest_height = np.mean(lowest_points[:, 2])

# 创建一个Matplotlib图形
plt.figure()

# 绘制前n个点
plt.scatter(selected_points[:, 0], selected_points[:, 1], c='b', label='Points')

# 绘制边界框
plt.plot([min_x, max_x, max_x, min_x, min_x], [min_y, min_y, max_y, max_y, min_y], c='r', label='Bounding Box')

# 添加标签和图例
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend()

# 显示图形
plt.show()

# 查找第一个坐标超出边界框范围的点
out_of_bounds_point = None

for point in points:
    if np.any(point[:2] < [min_x, min_y]) or np.any(point[:2] > [max_x, max_y]):
        out_of_bounds_point = point
        break

if out_of_bounds_point is not None:
    print("枝下高为:", out_of_bounds_point[2]-avg_lowest_height)
