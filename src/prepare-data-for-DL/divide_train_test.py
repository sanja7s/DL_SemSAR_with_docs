#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:31:41 2018

@author: sanja7s
"""
import os
import rasterio
import numpy as np
from affine import Affine
from pyproj import Proj, transform
from osgeo import osr, gdal
import shutil
from shutil import copyfile, move


def get_extent(dataset):

	cols = dataset.RasterXSize
	rows = dataset.RasterYSize
	transform = dataset.GetGeoTransform()
	minx = transform[0]
	maxx = transform[0] + cols * transform[1] + rows * transform[2]

	miny = transform[3] + cols * transform[4] + rows * transform[5]
	maxy = transform[3]

	return {
			"minX": str(minx), "maxX": str(maxx),
			"minY": str(miny), "maxY": str(maxy),
			"cols": str(cols), "rows": str(rows)
			}


def get_latlong(r, extent):
# find the raster's info

	minx = float(extent["minX"])
	maxx = float(extent["maxX"])
	miny = float(extent["minY"])
	maxy = float(extent["maxY"])

	T0 = r.transform  # upper-left pixel corner affine transform
	p1 = Proj(r.crs)
	A = r.read()  # pixel values

	# All rows and columns
	cols, rows = np.meshgrid(np.arange(A.shape[2]), np.arange(A.shape[1]))

	# Get affine transform for pixel centres
	T1 = T0 * Affine.translation(0.5, 0.5)
	# Function to convert pixel row/column index (from 0) to easting/northing at centre
	rc2en = lambda r, c: (c, r) * T1

	# All eastings and northings (there is probably a faster way to do this)
	eastings, northings = np.vectorize(rc2en, otypes=[np.float, np.float])(rows, cols)

	# Project all longitudes, latitudes
	p2 = Proj(proj='latlong',datum='WGS84')

	lon_min, lat_min = transform(p1, p2, minx, miny)
	lon_max, lat_max = transform(p1, p2, maxx, maxy)
 
	return {
		"min_lon": str(lon_min), "min_lat": str(lat_min),
		"max_lon": str(lon_max), "max_lat": str(lat_max)
		}


def train_or_test(img_name):
	# decide where this image should go

	minmaxlonlat = img_extent_and_lon_lat(img_name)

	min_lon = float(minmaxlonlat["min_lon"])
	max_lon = float(minmaxlonlat["max_lon"])

	if min_lon > 28.0 or max_lon < 24.0:
		return 'train'
	elif min_lon >= 24.0 and max_lon <= 28.0:
		return 'test'
	else:
		return 'discard'



def img_extent_and_lon_lat(path_to_file):
	ds = gdal.Open(path_to_file)
	extent = get_extent(ds)
	with rasterio.open(path_to_file) as ds:
		return get_latlong(ds, extent)	


def split_data_to_train_test(models_DIR, train_dir, label_dir, model_name='Corine-Sentinel-DEM'):

	res = {'train':0, 'test':0, 'discard':0}

	data_dir = os.path.join(models_DIR, model_name)
	if not os.path.exists(data_dir):
		os.makedirs(data_dir)

	for subdir in ['test', 'test_labels', 'train', 'train_labels', 'val', 'val_labels']:
		if not os.path.exists(os.path.join(data_dir, subdir)):
			os.makedirs(os.path.join(data_dir, subdir))

	# recursively iterate through all the files f in inDir
	for root, subdirs, fl in os.walk(label_dir):
		for f in fl:
			if f.endswith(".tiff") or f.endswith(".tif"):
				fPath = os.path.join(root, f)
				to = train_or_test(fPath)
				res[to] += 1
				dst_labels = os.path.join(data_dir, to + '_labels')
				dst_images = os.path.join(data_dir, to)
				img_pair_path =  os.path.join(train_dir, f)
				if to != 'discard':
					copyfile(fPath, os.path.join(dst_labels,f))
					copyfile(img_pair_path, os.path.join(dst_images,f))
	print (res)

def take_out_val_data_pct(models_DIR, model_name='Corine-Sentinel-DEM', val_pct=0.15):
	# we also take out the validation dataset from the training

	data_dir = os.path.join(models_DIR, model_name)

	train_images_dir = os.path.join(data_dir, 'train')
	train_labels_dir = os.path.join(data_dir, 'train_labels')
	val_images_dir = os.path.join(data_dir, 'val')
	val_labels_dir = os.path.join(data_dir, 'val_labels')
	files = os.listdir(train_images_dir)

	i = int(len(files) * val_pct)
	for f in sorted(files):
		img_name = os.path.join(train_images_dir, f)
		label_name = os.path.join(train_labels_dir, f)
		try:
			move(img_name, val_images_dir)
			try:
				move(label_name, val_labels_dir)
			except shutil.Error:
				continue
		except shutil.Error:
			continue
		#print (i)
		i-=1
		if not i:
			break

def split_data_to_train_test_val(label_dir, train_dir, models_DIR, model_name='Corine-Sentinel-DEM'):

	#split_data_to_train_test(models_DIR, train_dir, label_dir, model_name)
	take_out_val_data_pct(models_DIR, model_name='Corine-Sentinel-DEM', val_pct=0.15)



current_dir = os.path.abspath(os.path.dirname(__file__))
print ('project', current_dir)
in_dir = os.path.join(current_dir, '../../data/DL_prepare/labels')
print ('working_DIR',in_dir)
models_DIR = os.path.join(current_dir, '../../data/DL_models/Semantic-Segmentation-Suite/')

label_dir = os.path.join(current_dir, '../../data/DL_prepare/labels')
train_dir = os.path.join(current_dir, '../../data/DL_prepare/train')


split_data_to_train_test_val(label_dir, train_dir, models_DIR)