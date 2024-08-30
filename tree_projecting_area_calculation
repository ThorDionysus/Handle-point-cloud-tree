import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay


def load_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    return np.asarray(pcd.points)


def project_to_plane(points):
    points[:, 2] = -1.0
    return points


def voxel_downsample(points, voxel_size=0.05):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    downsampled_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    return np.asarray(downsampled_pcd.points)


def alpha_shape(points, alpha):
    tri = Delaunay(points[:, :2])  
    triangles = points[tri.simplices]

    a = np.linalg.norm(triangles[:, 0] - triangles[:, 1], axis=1)
    b = np.linalg.norm(triangles[:, 1] - triangles[:, 2], axis=1)
    c = np.linalg.norm(triangles[:, 2] - triangles[:, 0], axis=1)

    s = (a + b + c) / 2.0
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))

    circum_r = a * b * c / (4.0 * area)
    triangles = triangles[circum_r < 1.0 / alpha]

    return triangles


def plot_point_cloud_and_boundary(points, boundary_triangles):
    plt.figure(figsize=(10, 10))

    plt.scatter(points[:, 0], points[:, 1], s=100, color='blue', label='Projected Points')

    for triangle in boundary_triangles:
        plt.fill([triangle[0, 0], triangle[1, 0], triangle[2, 0]],
                 [triangle[0, 1], triangle[1, 1], triangle[2, 1]],
                 color='yellow', alpha=0.6)
        plt.plot([triangle[0, 0], triangle[1, 0]], [triangle[0, 1], triangle[1, 1]], color='red')
        plt.plot([triangle[1, 0], triangle[2, 0]], [triangle[1, 1], triangle[2, 1]], color='red')
        plt.plot([triangle[2, 0], triangle[0, 0]], [triangle[2, 1], triangle[0, 1]], color='red')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('Alpha Shape Boundary and Projected Points')
    plt.show()


def compute_area(triangles):
    total_area = 0.0
    for tri in triangles:
        a = np.linalg.norm(tri[0] - tri[1])
        b = np.linalg.norm(tri[1] - tri[2])
        c = np.linalg.norm(tri[2] - tri[0])
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        total_area += area
    return total_area

def save_point_cloud(points, file_path):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(file_path, pcd)


if __name__ == "__main__":
    points = load_point_cloud("your_point_cloud_file.ply")
    points = project_to_plane(points)
    points_subsampled = voxel_downsample(points, voxel_size=0.03)
    alpha = 30
    boundary_triangles = alpha_shape(points_subsampled, alpha)
    plot_point_cloud_and_boundary(points_subsampled, boundary_triangles)
    boundary_area = compute_area(boundary_triangles)
    print(f"-> projecting area: {boundary_area} m^3
")
    boundary_points = boundary_triangles.reshape(-1, 3)
    save_point_cloud(boundary_points, "Alpha_Shapes.pcd")
