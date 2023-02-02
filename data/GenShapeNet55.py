import shutil
import os
import json
import argparse

parser = argparse.ArgumentParser(description='Generate Small ShapeNetCompletion')
parser.add_argument('--test', help='test_files', required=True)
parser.add_argument('--train', help='train_files', required=True)
args = vars(parser.parse_args())

test_files = int(args["test"])
train_files = int(args["train"])

with open("shapenet_synset_dict.json", "r") as f:
    data = json.load(f)

catlist = []
for x, y in data.items():
    catlist.append(x)

def create_file(file, dest, count):
    with open("./ShapeNet55-34/ShapeNet-55/"+file) as f:
        train = f.read()
    
    train = train.split("\n")
    train.sort()

    while len(train[0]) == 0:
        train = train[1:]

    print(len(train))
    dlist = {}

    for x in train:
        try:
            dlist[x.split('-')[0]].append(x)
        except KeyError:
            dlist[x.split('-')[0]] = [x]

    flist = []

    for cat in catlist:
        ct = 0
        for x in dlist[cat]:
            if ct < count:
                flist.append(x)
                ct += 1
    
    data = "\n".join(flist)
    print(f"{len(flist)} Files are separated")
    with open("./ShapeNet55-34/ShapeNet-55/"+dest, "w") as f:
        f.write(data)


create_file("train2.txt", "train.txt", train_files)
create_file("test2.txt", "test.txt", test_files)

