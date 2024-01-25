import open3d as o3d
import numpy as np

# import the point cloud
pcd = o3d.io.read_point_cloud(r"file_path")

# calculate the tree height
def calculate_tree_height(pcd, m, n):
    
    points = np.asarray(pcd.points)
    highest_points = points[np.argsort(points[:, 2])[-m:]]
    lowest_points = points[np.argsort(points[:, 2])[:n]]
    avg_highest_height = np.mean(highest_points[:, 2])
    avg_lowest_height = np.mean(lowest_points[:, 2])
    tree_height = avg_highest_height - avg_lowest_height

    return tree_height


# Calculate the projected area of the tree canopy
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
def calculate_projection_area(pcd):
    points = np.asarray(pcd.points)
    points_without_z = points[:, :2]
    sorted_points = points_without_z[np.lexsort((points_without_z[:, 1], points_without_z[:, 0]))]
    hull = ConvexHull(sorted_points)
    plt.scatter(points[:, 0], points[:, 1], label='Original Points', color='blue')
    for simplex in hull.simplices:
        plt.plot(sorted_points[simplex, 0], sorted_points[simplex, 1], 'k-')
    plt.title('Convex Hull')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.show()
    return hull.volume


# Calculate the maximum radius of the tree canopy
def calculate_crown_width(pcd, angle_degrees,k):
    points = np.asarray(pcd.points)
    angle_radians = np.radians(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians), 0],
        [np.sin(angle_radians), np.cos(angle_radians), 0],
        [0, 0, 1]
    ])
    rotated_points = np.dot(points, rotation_matrix)
    max_points =  rotated_points[np.argsort( rotated_points[:, 0])[-k:]]
    min_points =  rotated_points[np.argsort( rotated_points[:, 0])[:k]]
    avg_max_width = np.mean(max_points[:, 0])
    avg_min_width = np.mean(min_points[:, 0])
    crown_width = avg_max_width - avg_min_width

    return crown_width



m = 40
n = 40
k = 40

tree_height = calculate_tree_height(pcd, m, n)
total_projection_area = calculate_projection_area(pcd)


max_crown_width = 0
max_rotation_direction = None

for angle_degrees in range(0, 180, 1):
    crown_width = np.max(calculate_crown_width(pcd, angle_degrees,k))
    if crown_width > max_crown_width:
        max_crown_width = crown_width
        max_degree = angle_degrees



print(f"tree_hright: {tree_height} m")
print(f"projection_area: {total_projection_area} m²")
print(f"crown_maximun_radius: {max_crown_width} m")
