# Point Cloud Tree Segmentation and Tree Phenotype Retrieval Program
## Introduction
This project is designed to process tree point cloud data. It offers various essential functionalities, including point cloud segmentation, point cloud merging, and basic phenotype retrieval. Please note that this project is specifically tailored for PLY files. 
### Requirement
Before utilizing this set of code, make sure you have the following packages and libraries installed:
#### open3d: 
You can install it using pip with the following command:
```
pip install open3d
```
#### NumPy:
If you haven't already have NumPy installed, you can install it with:
```
pip install numpy
```
#### scikit-learn (sklearn):
You can install scikit-learn with:
```
pip install scikit-learn
```
ensure that these packages are available in your Python environment before executing the code. Additionally, verify that you have a valid point cloud file located at the specified "file_path" or replace it with the actual path to the point cloud you wish to work with.

## Point Cloud K-Means Clustering Segmentation
This Python script is designed to cluster and sort a 3D point cloud using the K-Means clustering algorithm. It utilizes the Open3D library for point cloud processing and the scikit-learn library for K-Means clustering. The code reads a point cloud file, clusters the points based on their color information, and sorts the clusters by the mean color of each cluster.
### Code Explanation
The script loads the point cloud data from the specified file, extracting both colors and points.
K-Means clustering is applied to the colors of the points to group them into clusters.
Each cluster's mean color is calculated, and the clusters are sorted based on this mean color.
The sorted clusters are saved as separate PointCloud files.
### Usage
1. Clone or download this repository to your local machine.
2. Replace "file_path" in the code with the path to the point cloud file you want to process.
3. Adjust the n_clusters variable in the K-Means section to set the desired number of clusters.
4. Update the "flie_path" in the code to specify the path where you want to save the resulting point cloud files.
5. Run the script.
## Point Cloud Merging
This code is used to merge point clouds that have been segmented through K-means clustering. It uses the Open3D library to merge multiple PLY format point clouds located in a specified input folder. The merged point cloud is then saved as a single PLY file in the desired output location.
### Code Explanation
This code segment extracts all PLY-format files from the specified target folder. Subsequently, it creates a new point cloud and adds all the point clouds to the newly created one. Finally, it exports the merged point cloud.
### Usage
1. Clone or download this repository to your local machine.
2. Modify the script to specify your input folder and desired output file path:
- Set the `folder_path` variable to the path of the folder containing the PLY files you want to merge.
- Set the `output_path` variable to the path where you want to save the merged point cloud.
3. Run the script.
## Basic Phenotype Retrieval
Basic Phenotype Retrieval is a Python program designed to analyze point cloud data from trees. It provides a set of functionalities to calculate various tree-related parameters, such as tree height, projection area, crown maximum radius, volume, and surface area. This program is specifically tailored for PLY files.
### Code Explanation
This code segment calculates various basic morphological parameters of point cloud trees using custom-defined functions.It calculates the height of trees by sorting the coordinates of the point cloud based on their z-values.Then, it utilizes projection and the differential element method to approximate the tree's projected area. Similarly, it employs the differential element method to estimate the volume of the tree.It uses a rotation matrix to rotate the point cloud tree at intervals of 1 degree from 0 degrees to 180 degrees. By comparing the diameters measured at each angle, it ultimately determines the maximum diameter of the point cloud tree.Finally, the code will output the values of the aforementioned basic tree morphological 
### Usage
1. Clone or download this repository to your local machine.
2. Load the point cloud data by specifying the file path.
3. Perform point cloud preprocessing, including radius filtering.

## Measure Undercanopy Height
This program achieves the retrieval of advanced parameters under the branches of trees by drawing point clouds to approximate and estimate the positions of specific points.
### Code Explanation

This code first sorts the point cloud based on the z-values. Then, it selects the top n points and performs drawing on these points to achieve the functionality of capturing. Based on the distribution of these points and in conjunction with the tree point cloud, it determines the current position of the capture plane and subsequently measures the height of the capture plane. This program requires multiple adjustments of the n value to capture positions under the branches accurately.
### Usage
1. Clone or download this repository to your local machine.
2. Load the point cloud data by specifying the file path.
3. Set an initial value for n, and adjust it based on the results and the shape of the bounding box.
   
## Point Cloud RGB Extration

### Code Explanation

### Usage
