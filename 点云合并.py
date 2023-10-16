import open3d as o3d

# 定义用于存储所有点云的列表
point_clouds = []
# 文件路径列表，包含要合并的点云文件路径
file_paths = [ ]
#树干S：7、8、14、25、38、39、53
#树叶S：4、10、11、18、19、20、23、29、30、35、40、41、47、52、59
#果实：6、12、22、43、49.50

# 逐个加载点云文件并添加到列表中
for file_path in file_paths:
    point_cloud = o3d.io.read_point_cloud(file_path)
    point_clouds.append(point_cloud)

# 将所有点云合并成一个
merged_point_cloud = o3d.geometry.PointCloud()
for point_cloud in point_clouds:
    merged_point_cloud += point_cloud
#滤波
merged_point_cloud,index = merged_point_cloud.remove_radius_outlier(nb_points=20, radius=0.02)
# S-1:0.015, S-2:0.02, S-3:0.05
# 保存合并后的点云为一个新的PLY文件
o3d.io.write_point_cloud("E:\cloudsegmentation\S-2.ply", merged_point_cloud)
