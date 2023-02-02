#  Copyright (c) 2020. Author: Hanchen Wang, hw501@cam.ac.uk

import os, argparse, numpy as np
import json
from tensorpack import DataFlow, dataflow
# from open3d.open3d.io import read_triangle_mesh, read_point_cloud
import open3d


# def sample_from_mesh(filename, num_samples=16384):
#     pcd = read_triangle_mesh(filename).sample_points_uniformly(number_of_points=num_samples)
#     return np.array(pcd.points)


class pcd_df(DataFlow):
    def __init__(self, model_list, folder, dir, num_scans, num_partial_points=1024):
        self.model_list = model_list
        self.num_scans = num_scans
        self.folder = folder
        self.dir = dir
        self.partial_dir = os.path.join(folder, os.path.join(dir, "partial"))
        self.complete_dir = os.path.join(folder, os.path.join(dir, "complete"))
        self.num_ppoints = num_partial_points


    def size(self):
        return len(self.model_list) * self.num_scans

    @staticmethod
    def read_pcd(filename):
        pcd = open3d.open3d.io.read_point_cloud(filename)
        return np.array(pcd.points)

    def get_data(self):
        for data in self.model_list:
            model_id = data["taxonomy_id"]
            for pt in data[self.dir]:
                complete = self.read_pcd(os.path.join(self.complete_dir, os.path.join(model_id, '%s.pcd' % pt)))
                for i in range(self.num_scans):
                    partial = self.read_pcd(os.path.join(self.partial_dir, os.path.join(model_id, os.path.join('%s'%pt, '%02d.pcd' % i))))
                    if len(partial) > self.num_ppoints:
                        partial = partial[np.random.choice(len(partial), self.num_ppoints)]
                    yield model_id + "-" + pt.replace('/', '_'), partial, complete


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_scans', type=int, default=1)
    parser.add_argument('--output_file', default=r'ShapeNetCompletion.lmdb')
    parser.add_argument('--pcn', default="./PCN.json")
    parser.add_argument('--folder', default="./ShapeNetCompletion/")
    parser.add_argument('--dir', default="test")
    args = parser.parse_args()

    with open(args.pcn) as file:
        model_list = json.load(file)
    df = pcd_df(model_list, args.folder, args.dir, args.num_scans)
    if os.path.exists(args.output_file):
        os.system('rm %s' % args.output_file)
    dataflow.LMDBSerializer.save(df, args.output_file)
