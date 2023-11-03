import open3d as o3d

# Enter the file path of the point cloud to be merged
file_paths = []

point_clouds = []
for file_path in file_paths:
    point_cloud = o3d.io.read_point_cloud(file_path)
    point_clouds.append(point_cloud)

merged_point_cloud = o3d.geometry.PointCloud()
for point_cloud in point_clouds:
    merged_point_cloud += point_cloud
    
# enter the path that you want the result to be saved
o3d.io.write_point_cloud("E:\cloudsegmentation\S-2.ply", merged_point_cloud)
