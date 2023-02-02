import shutil
import os
import json
import argparse

parser = argparse.ArgumentParser(description='Generate Small ShapeNetCompletion')
parser.add_argument('--test', help='test_files', required=True)
parser.add_argument('--train', help='train_files', required=True)
parser.add_argument('--val', help='val_files', required=True)
args = vars(parser.parse_args())

test_files = int(args["test"])
train_files = int(args["train"])
val_files = int(args["val"])

original = "ShapeNetCompletion"
folder = "ShapeNetCompletion2"
original = os.path.join(os.getcwd(), original)
folder = os.path.join(os.getcwd(), folder)

jdict = []
tdict = {}
ff = os.path.join(original, os.path.join("test", "complete"))
flist = os.listdir(ff)

for i, x in enumerate(flist):
	cdict = {"taxonomy_id": str(x), "taxonomy_name":"None", "test": [], "train": [], "val": []}
	jdict.append(cdict)
	tdict[x] = i

def makedirs():
	os.mkdir(folder)
	os.mkdir(os.path.join(folder, "test"))
	os.mkdir(os.path.join(folder, "train"))
	os.mkdir(os.path.join(folder, "val"))
	os.mkdir(os.path.join(os.path.join(folder, "test"), "complete"))
	os.mkdir(os.path.join(os.path.join(folder, "val"), "complete"))
	os.mkdir(os.path.join(os.path.join(folder, "train"), "complete"))
	os.mkdir(os.path.join(os.path.join(folder, "test"), "partial"))
	os.mkdir(os.path.join(os.path.join(folder, "train"), "partial"))
	os.mkdir(os.path.join(os.path.join(folder, "val"), "partial"))


def copy(source_folder, dest):
	for file_name in os.listdir(source_folder):
	    # construct full file path
	    source = os.path.join(source_folder, file_name)
	    destination = os.path.join(dest, file_name)
	    if os.path.isfile(source):
	        shutil.copy(source, destination)
	        if not os.path.isfile(destination):
	        	shutil.copy(source, destination)
	        # print('copied', file_name)


def copy_partial(count, from_folder):
	print("Copying Partial Files from", from_folder, count)
	ff = os.path.join(original, os.path.join(from_folder, "partial"))
	tf = os.path.join(folder, os.path.join(from_folder, "partial"))
	flist = os.listdir(ff)
	for x in flist:
		cnt = 0
		os.mkdir(os.path.join(tf, x))
		for y in list(os.listdir(os.path.join(ff, x))):
			if cnt < count:
				os.mkdir(os.path.join(tf, os.path.join(x, y)))
				copy(os.path.join(ff, os.path.join(x, y)), os.path.join(tf, os.path.join(x, y)))
				jdict[tdict[x]][from_folder].append(y)
				cnt += 1
			else:
				break

def copy_complete(count, from_folder):
	print("Copying Complete Files from", from_folder, count)
	ff = os.path.join(original, os.path.join(from_folder, "complete"))
	tf = os.path.join(folder, os.path.join(from_folder, "complete"))
	flist = os.listdir(ff)
	for x in flist:
		cnt = 0
		os.mkdir(os.path.join(tf, x))
		for y in list(os.listdir(os.path.join(ff, x))):
			if cnt < count:
				try:
					shutil.copy(os.path.join(ff, os.path.join(x, y)), os.path.join(tf, os.path.join(x, y)))
					print(os.path.join(tf, os.path.join(x, y)))
				except:
					print("Copy Error")
				cnt += 1
			else:
				break

def copy_data(count, from_folder):
	print("Copying Files from", from_folder, count)
	pff = os.path.join(original, os.path.join(from_folder, "partial"))
	ptf = os.path.join(folder, os.path.join(from_folder, "partial"))
	ff = os.path.join(original, os.path.join(from_folder, "complete"))
	tf = os.path.join(folder, os.path.join(from_folder, "complete"))
	flist = os.listdir(pff)
	for x in flist:
		cnt = 0
		os.mkdir(os.path.join(ptf, x))
		os.mkdir(os.path.join(tf, x))
		for y in list(os.listdir(os.path.join(pff, x))):
			if cnt < count:
				os.mkdir(os.path.join(ptf, os.path.join(x, y)))
				copy(os.path.join(pff, os.path.join(x, y)), os.path.join(ptf, os.path.join(x, y)))
				shutil.copy(os.path.join(ff, os.path.join(x, y+".pcd")), os.path.join(tf, os.path.join(x, y+".pcd")))
				# if not os.path.isfile(os.path.join(tf, os.path.join(x, y+".pcd"))):
				# 	print("Copy Error")
				# 	shutil.copy(os.path.join(ff, os.path.join(x, y+".pcd")), os.path.join(tf, os.path.join(x, y+".pcd")))
				# jdict[tdict[x]][from_folder].append(y)
				cnt += 1
			else:
				break

def get_data(count, from_folder):
	pff = os.path.join(original, os.path.join(from_folder, "partial"))
	ptf = os.path.join(folder, os.path.join(from_folder, "partial"))
	ff = os.path.join(original, os.path.join(from_folder, "complete"))
	tf = os.path.join(folder, os.path.join(from_folder, "complete"))
	flist = os.listdir(pff)
	total_count = 0
	for x in flist:
		cnt = 0
		# os.mkdir(os.path.join(ptf, x))
		# os.mkdir(os.path.join(tf, x))
		for y in list(os.listdir(os.path.join(pff, x))):
			if cnt < count:
				# os.mkdir(os.path.join(ptf, os.path.join(x, y)))
				# copy(os.path.join(pff, os.path.join(x, y)), os.path.join(ptf, os.path.join(x, y)))
				# shutil.copy(os.path.join(ff, os.path.join(x, y+".pcd")), os.path.join(tf, os.path.join(x, y+".pcd")))
				# if not os.path.isfile(os.path.join(tf, os.path.join(x, y+".pcd"))):
				# 	print("Copy Error")
				# 	shutil.copy(os.path.join(ff, os.path.join(x, y+".pcd")), os.path.join(tf, os.path.join(x, y+".pcd")))
				jdict[tdict[x]][from_folder].append(y)
				cnt += 1
			else:
				break
		total_count += cnt
	print("Copying Files from", from_folder, total_count)


def copy_files():
	makedirs()
	# copy_partial(test_files, "test")
	# copy_partial(train_files, "train")
	# copy_partial(val_files, "val")
	# copy_complete(test_files, "test")
	# copy_complete(train_files, "train")
	# copy_complete(val_files, "val")

	copy_data(test_files, "test")
	copy_data(train_files, "train")
	copy_data(val_files, "val")

def get_files():
	get_data(test_files, "test")
	get_data(train_files, "train")
	get_data(val_files, "val")

# copy_files()

get_files()

# Serializing json
json_object = json.dumps(jdict, indent=4)
 
# Writing to sample.json
with open("PCN.json", "w") as outfile:
    outfile.write(json_object)

