pip install -r requirements.txt
pip install --upgrade --no-cache-dir gdown
# PointNet++
git clone https://github.com/erikwijmans/Pointnet2_PyTorch.git
cd Pointnet2_PyTorch/pointnet2_ops_lib
python setup.py install --user
cd ../..
# GPU kNN
pip install --upgrade https://github.com/unlimblue/KNN_CUDA/releases/download/0.2/KNN_CUDA-0.2-py3-none-any.whl
cd extensions/chamfer_dist
python setup.py install --user
cd ../..