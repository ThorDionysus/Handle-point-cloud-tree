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
def calculate_projection_area(pcd, projection_direction):
    
    projection_plane = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10.0, origin=[0, 0, 0])
    points = np.asarray(pcd.points)
    projection_coords = np.dot(points, projection_direction)
    projection_points = points - np.outer(projection_coords, projection_direction)
    projection_pcd = o3d.geometry.PointCloud()
    projection_pcd.points = o3d.utility.Vector3dVector(projection_points)
    distances = np.asarray(projection_pcd.compute_nearest_neighbor_distance())
    projection_areas = np.pi * (distances / 2.0) ** 2 
    total_projection_area = np.sum(projection_areas)

    return total_projection_area


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

# Calculate the vloume of the tree
def calculate_point_cloud_volume(pcd):

    points = np.asarray(pcd.points)
    min_bound = np.min(points, axis=0)
    max_bound = np.max(points, axis=0)
    voxel_size = 0.01  # Voxel resolution, adjustable according to your needs
    dimensions = ((max_bound - min_bound) / voxel_size).astype(int) + 1
    voxel_grid = np.zeros(dimensions, dtype=bool)
    for point in points:
        voxel_index = ((point - min_bound) / voxel_size).astype(int)
        voxel_grid[tuple(voxel_index)] = True
    num_voxels = np.sum(voxel_grid)
    volume = num_voxels * (voxel_size**3)

    return volume

projection_direction = np.array([0, 0, 1], dtype=np.float64)  
m = 40
n = 40
k = 40

tree_height = calculate_tree_height(pcd, m, n)
total_projection_area = calculate_projection_area(pcd, projection_direction)


max_crown_width = 0
max_rotation_direction = None

for angle_degrees in range(0, 180, 1):
    crown_width = np.max(calculate_crown_width(pcd, angle_degrees,k))
    if crown_width > max_crown_width:
        max_crown_width = crown_width
        max_degree = angle_degrees

volume = calculate_point_cloud_volume(pcd)


voxel_resolution = 0.01  # Voxel resolution, adjustable according to your needs
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_resolution)

surface_area = 0
for voxel in voxel_grid.get_voxels():
    if len(voxel.grid_index) > 0: 
        surface_area += 1

surface_area *= voxel_resolution**2

print(f"tree_hright: {tree_height} m")
print(f"projection_area: {total_projection_area} m²")
print(f"crown_maximun_radius: {max_crown_width} m")
print(f"volume: {volume} m³")
print(f"surface_area: {surface_area} m³")
