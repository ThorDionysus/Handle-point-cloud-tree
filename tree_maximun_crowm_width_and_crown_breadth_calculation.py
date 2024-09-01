import open3d as o3d
import numpy as np

# Import the point cloud
pcd = o3d.io.read_point_cloud("H:\Pointcloud File\cloudsegmentation\Tree7-AH-F.ply")

# Calculate the maximum radius of the tree canopy
def calculate_crown_width(pcd, angle_degrees, k):
    points = np.asarray(pcd.points)
    angle_radians = np.radians(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians), 0],
        [np.sin(angle_radians), np.cos(angle_radians), 0],
        [0, 0, 1]
    ])
    rotated_points = np.dot(points, rotation_matrix)
    max_points = rotated_points[np.argsort(rotated_points[:, 0])[-k:]]
    min_points = rotated_points[np.argsort(rotated_points[:, 0])[:k]]
    avg_max_width = np.mean(max_points[:, 0])
    avg_min_width = np.mean(min_points[:, 0])
    crown_width = avg_max_width - avg_min_width

    return crown_width

# Calculate the North-South diameter
def calculate_north_south_diameter(pcd):
    points = np.asarray(pcd.points)
    max_north = np.max(points[:, 1])
    min_south = np.min(points[:, 1])
    ns_diameter = max_north - min_south
    return ns_diameter

k = 40
max_crown_width = 0
max_rotation_direction = None

# Find the maximum crown width by rotating
for angle_degrees in range(0, 180, 1):
    crown_width = calculate_crown_width(pcd, angle_degrees, k)
    if crown_width > max_crown_width:
        max_crown_width = crown_width
        max_rotation_direction = angle_degrees

# Calculate the North-South diameter
ns_diameter = calculate_north_south_diameter(pcd)

print(f"Maximum crown width: {max_crown_width} m at {max_rotation_direction} degrees")
print(f"crown breadth: {ns_diameter} m")
