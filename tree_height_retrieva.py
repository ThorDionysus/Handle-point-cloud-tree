import open3d as o3d
import numpy as np

# Import the point cloud
pcd = o3d.io.read_point_cloud(r"file_path")

# Calculate the tree height
def calculate_tree_height(pcd, m, n):
    points = np.asarray(pcd.points)
    highest_points = points[np.argsort(points[:, 2])[-m:]]
    lowest_points = points[np.argsort(points[:, 2])[:n]]
    avg_highest_height = np.mean(highest_points[:, 2])
    avg_lowest_height = np.mean(lowest_points[:, 2])
    tree_height = avg_highest_height - avg_lowest_height

    return tree_height

m = 40
n = 40
tree_height = calculate_tree_height(pcd, m, n)

print(f"Tree height: {tree_height} m")
