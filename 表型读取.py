import open3d as o3d
import numpy as np
# 读取点云数据
pcd = o3d.io.read_point_cloud(r"C:\cloudsegmentation\M-F.ply")
# 进行点云去噪
pcd, index = pcd.remove_radius_outlier(nb_points=20, radius=0.04)


# 计算株高
def calculate_tree_height(pcd, m, n):
    # 将点云转换为NumPy数组
    points = np.asarray(pcd.points)
    # 找到最高的m个点和最低的n个点
    highest_points = points[np.argsort(points[:, 2])[-m:]]
    lowest_points = points[np.argsort(points[:, 2])[:n]]
    # 计算最高点和最低点的平均高度
    avg_highest_height = np.mean(highest_points[:, 2])
    avg_lowest_height = np.mean(lowest_points[:, 2])
    # 计算株高，即平均最高点高度减去平均最低点高度
    tree_height = avg_highest_height - avg_lowest_height

    return tree_height


# 计算投影面积
def calculate_projection_area(pcd, projection_direction):
    # 创建投影平面
    projection_plane = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10.0, origin=[0, 0, 0])

    # 计算点云投影到平面上
    points = np.asarray(pcd.points)
    projection_coords = np.dot(points, projection_direction)
    projection_points = points - np.outer(projection_coords, projection_direction)

    # 创建投影点云
    projection_pcd = o3d.geometry.PointCloud()
    projection_pcd.points = o3d.utility.Vector3dVector(projection_points)

    # 计算投影面积
    distances = np.asarray(projection_pcd.compute_nearest_neighbor_distance())
    projection_areas = np.pi * (distances / 2.0) ** 2  # 假设点云是圆形投影
    total_projection_area = np.sum(projection_areas)

    return total_projection_area


# 计算冠幅
def calculate_crown_width(pcd, angle_degrees,k):
    # 将点云转换为NumPy数组
    points = np.asarray(pcd.points)
    # 创建旋转矩阵将单位向量旋转到指定的方向
    angle_radians = np.radians(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians), 0],
        [np.sin(angle_radians), np.cos(angle_radians), 0],
        [0, 0, 1]
    ])

    # 计算旋转后的点云坐标
    rotated_points = np.dot(points, rotation_matrix)
    # 获取旋转后点云的边界
    max_points =  rotated_points[np.argsort( rotated_points[:, 0])[-k:]]
    min_points =  rotated_points[np.argsort( rotated_points[:, 0])[:k]]
    # 计算最高点和最低点的平均高度
    avg_max_width = np.mean(max_points[:, 0])
    avg_min_width = np.mean(min_points[:, 0])
    # 计算株高，即平均最高点高度减去平均最低点高度
    crown_width = avg_max_width - avg_min_width

    return crown_width

#计算体积
def calculate_point_cloud_volume(pcd):
    # 将点云转换为NumPy数组
    points = np.asarray(pcd.points)

    # 获取点云的坐标范围（边界框的最小和最大坐标）
    min_bound = np.min(points, axis=0)
    max_bound = np.max(points, axis=0)

    # 计算点云的体素分辨率，假设是等间距的
    voxel_size = 0.01  # 体素分辨率，可以根据需求调整

    # 计算体素网格的维度，将坐标范围除以体素分辨率
    dimensions = ((max_bound - min_bound) / voxel_size).astype(int) + 1

    # 创建一个与体素网格相同维度的零矩阵，用于表示体素网格
    voxel_grid = np.zeros(dimensions, dtype=bool)

    # 将点云中的点映射到体素网格中
    # 对于每个点，计算它在体素网格中的索引，并将相应的体素标记为存在
    for point in points:
        voxel_index = ((point - min_bound) / voxel_size).astype(int)
        voxel_grid[tuple(voxel_index)] = True

    # 计算体素网格中存在的体素数量
    num_voxels = np.sum(voxel_grid)

    # 计算点云的体积，体积=体素数量*体素体积
    volume = num_voxels * (voxel_size**3)

    return volume



# 设置投影方向（例如，垂直于地面的方向）
projection_direction = np.array([0, 0, 1], dtype=np.float64)  # 显式指定数据类型
# 设置要考虑的最高和最低点的数量
m = 40
n = 30
k = 40
# 计算株高
tree_height = calculate_tree_height(pcd, m, n)
# 计算点云的投影面积（不进行简化计算）
total_projection_area = calculate_projection_area(pcd, projection_direction)

# 初始化最大冠幅和对应的旋转方向
max_crown_width = 0
max_rotation_direction = None

# 循环每次旋转1度并计算冠幅
for angle_degrees in range(0, 180, 1):
    # 计算点云树木在指定方向上的冠幅
    crown_width = np.max(calculate_crown_width(pcd, angle_degrees,k))
    # 更新最大冠幅和对应的旋转方向
    if crown_width > max_crown_width:
        max_crown_width = crown_width
        max_degree = angle_degrees

volume = calculate_point_cloud_volume(pcd)

# 定义体素分辨率（控制体素网格的细粒度）
voxel_resolution = 0.01  # 调整为适当的值，以匹配您的数据

# 将点云转换为体素网格
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_resolution)

# 计算体素网格的表面积
surface_area = 0
for voxel in voxel_grid.get_voxels():
    if len(voxel.grid_index) > 0:  # 检查体素内是否有点
        surface_area += 1

# 乘以体素尺寸的平方来获得表面积（假设体素是正方体）
surface_area *= voxel_resolution**2

# 打印结果
print(f"株高: {tree_height} 米")
print(f"整个点云的投影面积: {total_projection_area} 米²")
print(f"树冠最大直径: {max_crown_width} ,{max_degree} 米")
print(f"体积: {volume} 米³")
print(f"点云的表面积为: {surface_area} 米³")