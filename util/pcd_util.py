import open3d as o3d
import os
import numpy as np

def read_pcd(filename):
    pcd = o3d.io.read_point_cloud(filename)
    return np.array(pcd.points)


def save_pcd(filename, points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(filename, pcd)