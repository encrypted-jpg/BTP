import os
import argparse

parser = argparse.ArgumentParser(description='Generate Small ShapeNetCompletion')
parser.add_argument('--test', type=float, default=0.1, help='test_files', required=False)
parser.add_argument('--train', type=int, default=100, help='train_files', required=True)
args = vars(parser.parse_args())

test_files = float(args["test"])
train_files = int(args["train"])

with open("files.txt", "r") as f:
    data = f.read().splitlines()

cdict = {}

for x in data:
    try:
        cdict[x.split("_")[0]].append(x)
    except KeyError:
        cdict[x.split("_")[0]] = [x]

test = []
train = []
for x, y in cdict.items():
    n = int(len(y)*test_files)
    test.extend(y[:n])
    train.extend(y[n:n+train_files])
    # print(x, n, len(y) - n)

print(f" Train Files = {len(train)}, Test Files = {len(test)}")
test_list = "\n".join(test)
train_list = "\n".join(train)

with open("train.txt", "w") as f:
    f.write(train_list)

with open("test.txt", "w") as f:
    f.write(test_list)

