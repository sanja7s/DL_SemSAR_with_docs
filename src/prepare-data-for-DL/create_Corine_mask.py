#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:31:41 2018

@authors: sanja7s, mask overlap code by Patrik Vilja

"""
import os
import sys
import numpy as np
import rasterio
from rasterio.windows import Window
from rasterio import windows
from pyproj import Proj, transform
import matplotlib.pyplot as plt
#import numpy.ma as ma

def reduceAffine(shape, affineTransform, fn):
    """ Reduce function """
    height, width = shape
    xs = np.zeros(shape, dtype=np.float64, order='F')
    ys = np.zeros(shape, dtype=np.float64, order='F')

    for x in range(0, width):
        xs[:,x],  ys[:,x] = fn(affineTransform, height, x)
    return xs, ys

def affine2crs(shape, affineTransform):
    """ Transform affine coordinates to crs """
    reducer = lambda aff, height, x: aff * (np.full(height, x, dtype=np.float64), np.arange(0, height) + 0.5)
    return reduceAffine(shape, affineTransform, reducer)

def crs2affine(shape, affineTransform, east, north):
    """ Transform crs to affine """
    reducer = lambda aff, height, x: np.floor(~aff * (east[:,x], north[:,x]))

    return reduceAffine(shape, affineTransform, reducer)

def window(cols, rows):
    return Window.from_slices((np.min(rows), np.max(rows)+1), (np.min(cols), np.max(cols)+1))


def mask(cols, rows, window, a, b):
    """ Apply the mask of a to b """

    def reshapeMask(cols, rows, shape, b_data):
        """ Reshape the low resolution complement to match the given image shape """

        rows = rows.astype(np.int32)
        cols = cols.astype(np.int32)
        c = [rows.reshape(rows.size, order='F') - np.min(rows),
             cols.reshape(cols.size, order='F') - np.min(cols)]

        try:
            return b_data[c].reshape(*shape, order='F')
        except IndexError:
            return None

    a_data = a.read(1)  
    b_data = b.read(1, window=window)

    reshaped_data = reshapeMask(cols, rows, a.shape, b_data)
    if reshaped_data is not None:
        return reshaped_data * (a_data > 0) 
    else:
        return None

def mask_overlap(raster_a, raster_mask, mask=mask):
    """ overlap raster mask and raster a """
    # transform affine coordinates of raster A into crs
    east, north = affine2crs(raster_a.shape, raster_a.transform)

    # project lat/lon of A raster to crs of B raster
    c, d = transform(Proj(raster_a.crs), Proj(raster_mask.crs), east, north)

    # transform lat/lon of raster B into affine coordinates
    cols, rows = crs2affine(raster_a.shape, raster_mask.transform, c, d)

    if (np.min(rows) >= 0 and np.max(rows) > 0 and np.min(cols) >= 0 and np.max(cols) > 0):
        # apply mask of b to a
        overlap = mask(cols, rows, window(cols, rows), raster_a, raster_mask)
    else:
        overlap = None
    return cols, rows, overlap


def tiff2rgb(img_name, imt, palette_file_name, rgb=3):

    def check_if_corner_img(img):
        # do not take images extending outside the mask borders
        return (np.amax(img) == 255)
    
    def check_if_single_label(img):
        # this does not really happen, 
        # but in theory could sometime
        # we do not need image with a single label
        imgLst = np.asarray(img).reshape(-1)
        return len(np.unique(imgLst)) == 1
 
    def read_in_labels(palette_file_name):
        # this is hard-coded for specifically the Corine mask
        d = np.zeros((256, 3), "uint8") 
        with open(palette_file_name, 'r') as f:
            if rgb == 3:
                for line in f:
                    pid, r, g, b = line.split()
                    if int(pid) in range(46, 49):
                        d[int(pid)] = [0,191,255] # blue
                    elif int(pid) in range(40, 46): 
                        d[int(pid)] = [173,216,230] # light blue
                    elif int(pid) in range(22, 40): 
                        d[int(pid)] = [127,255,0] # green
                    elif int(pid) in range(16, 22): 
                        d[int(pid)] = [222,184,135] # brown
                    elif int(pid) in range(1, 16): 
                        d[int(pid)] = [128,0,0] # maroon
                    else:
                        d[int(pid)] = [0,0,0]
            else:
                for line in f:
                    d[int(pid)] = [int(r),int(g),int(b)]
        return d

    # if single label or corner, do not save label image AND
    # delete the corresponding training image
    if check_if_single_label(imt) or check_if_corner_img(imt):
        return None

    if rgb == 1:
        # the case when the label is equal the pixel value
        # and we have only one band in the label images
        # this could be used for the WaterMask, for instance
        im = np.zeros((imt.shape[0], imt.shape[1], 3), "uint8")
        im[:,:,0] = imt
        im[:,:,1] = imt
        im[:,:,2] = imt
    elif rgb == 3:
        # the case when the label is indexed by a palette file
        # and the label file is in rgb 3-band format
        # this works for the Corine mask
        im = np.zeros((imt.shape[0], imt.shape[1], 3), "uint8") 
        d = read_in_labels(palette_file_name)
        im[:,:,:] = d[imt]

    return im


def batch_create_mask(m, in_dir, out_dir, type_of_mask = 'Corine', palette_file_name = None):
    """ create Corine masks from all files """
    
    with rasterio.open(m, 'r') as mask_file:
        
        for root, subdirs, fl in os.walk(in_dir):
            for f in fl:
                if f.endswith(".tiff") or f.endswith(".tif"):
                    fPath = os.path.join(root, f)
                    with rasterio.open(fPath, 'r') as image_file:
            
                        cols, rows, overlap = mask_overlap(image_file, mask_file)
                        if overlap is None:
                            # if this image is outside the mask area, skip
                            try:
                                os.remove(fPath)
                            except FileNotFoundError:
                                print ('NOT REMOVED ', fPath)
                        else:
                            profile = image_file.profile
                            if type_of_mask == 'Corine':
                                out_img = tiff2rgb(f, overlap, palette_file_name)
                                profile.update(count=3, dtype=rasterio.uint8)
                            # this can be adapted to other masks, say the WaterMask
                            elif type_of_mask == 'WaterMask':
                                out_img = overlap
                                profile.update(count=1, dtype=rasterio.uint8)
                            else:
                                out_img = overlap
                                profile.update(count=1, dtype=rasterio.uint8)
                            if out_img is None:
                                try:
                                    os.remove(fPath)
                                except FileNotFoundError:
                                    print ('NOT REMOVED ', fPath)
                                continue

                            with rasterio.open(os.path.join(out_dir, f), 'w', **profile) as out:
                                for band_id in range(out_img.shape[-1]):
                                    band_id += 1    
                                    out.write(out_img[...,band_id-1], band_id)

