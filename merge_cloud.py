import open3d as o3d
import os

# Enter the folder path containing the PLY files to be merged
folder_path = ""  # Replace with your input folder path

# Get a list of all PLY files in the folder
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".ply")]

point_clouds = []
for file_path in file_paths:
    point_cloud = o3d.io.read_point_cloud(file_path)
    point_clouds.append(point_cloud)

merged_point_cloud = o3d.geometry.PointCloud()
for point_cloud in point_clouds:
    merged_point_cloud += point_cloud

# Enter the path where you want the result to be saved
output_path = ""  # Replace with your desired output file path
o3d.io.write_point_cloud(output_path, merged_point_cloud)
