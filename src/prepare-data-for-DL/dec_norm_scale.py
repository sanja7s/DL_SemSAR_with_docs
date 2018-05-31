#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:36:18 2018

@author: sanja7s
"""
import os
import rasterio
import numpy as np
import cv2

global SMALL_VALUE
SMALL_VALUE = 1.0


def dec_norm_scale(geotif_file_name, out_dir):

	with rasterio.open(geotif_file_name, 'r') as ds:    
		#print('to decibel, normalize, scale ', geotif_file_name)

		new_bands = []
		for band_id in range(ds.count):
			band_id += 1	
			band = ds.read(band_id)

			
			# we check for the corner images using the DEM band
			# this DEM has 0.0 values for No Data
			if band_id == 3:
				if check_if_corner_img(band):
					#print ('omit', geotif_file_name)
					return
			

			new_band = np.zeros(band.shape, dtype=np.float32) 
			dec_band = 10 * np.log10(band + SMALL_VALUE) # to decibel
			new_band = cv2.normalize(dec_band, new_band, 0,255, cv2.NORM_MINMAX, cv2.CV_32F) # normalize, scale to (0, 255)
			new_bands.append(new_band)

		profile = ds.profile
		profile.update(dtype=rasterio.float32)		
		out_file_name = os.path.join(out_dir, os.path.basename(geotif_file_name))   

		with rasterio.open(os.path.join(out_file_name), 'w', **profile) as to:
			i = 0
			for new_band in new_bands:
				i+=1
				to.write(new_band, i)
			


# do not save corner images (partly outside boundaries of the original .tiff)
def check_if_corner_img(img):
    img_lst = np.asarray(img).reshape(-1)
    return (len(np.unique(img_lst)) == 1) or (np.amin(img) == 0)
		
	
def batch_dec_norm_scale(in_dir, out_dir):
	""" 
	turn to decibels, normalize and scale to (0,255) 
	each bands of each of the images in the folder in_dir
	save in out_dir
	"""

	for root, subdirs, fl in os.walk(in_dir): 
		for f in fl:
			if f.endswith(".tiff") or f.endswith(".tif"):
				# can add this is you already created some training images
				# and do not want to overwrite them
				#out_file_name = os.path.join(out_dir, f)  
				#if os.path.isfile(out_file_name):
				#	continue
				image_path = os.path.join(root, f)
				#print (image_path)
				dec_norm_scale(image_path, out_dir)
			
