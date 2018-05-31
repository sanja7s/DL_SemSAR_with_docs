#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 10:43:09 2018

@author: sanja7s
"""
from PIL import Image
import os
from scipy import misc
import numpy as np
from collections import defaultdict


def grayscale2rgb(out_dir, imgNameTiff, palette_file_name, rgb, training_dir=''):
    
    imgNamePng = os.path.split(imgNameTiff)[1] 
    imgPath = os.path.join(out_dir, imgNamePng) 
    
    if os.path.exists(imgPath):
        return 

    def check_if_corner_img(img):
        imgLst = np.asarray(img).reshape(-1)
        return (len(np.unique(imgLst)) == 1) or (np.amin(img) == 0)
    
    def check_if_single_label(img):
        imgLst = np.asarray(img).reshape(-1)
        return len(np.unique(imgLst)) == 1


        
    def read_in_labels(palette_file_name, rgb=2):
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

    try:
        imt = misc.imread(imgNameTiff)
    except OSError:
        return

    if not rgb:
        # if single label, do not save label image AND
        # delete corresponding training image
        #if check_if_corner_img(imt):
        #    return

        # for saving the training data -- we save as it is
        im = Image.open(imgNameTiff)
        im.save(imgPath)
    else:

        # if single label, do not save label image AND
        # delete corresponding training image
        if check_if_single_label(imt):
            try:
                os.remove(os.path.join(training_dir,imgNamePng))
                print ('REMOVED tiff2png', os.path.join(training_dir,imgNamePng))
            except FileNotFoundError:
                print ('NOT REMOVED tiff2png', os.path.join(training_dir,imgNamePng))
            return

        if rgb == 1:
            # the case when the label is equal the pixel value
            # and we have only one band in the label images
            im = np.zeros((imt.shape[0], imt.shape[1], 3), "uint8")
            im[:,:,0] = imt
            im[:,:,1] = imt
            im[:,:,2] = imt
        elif rgb == 2:
            # the case when the label is indexed by a palette file
            # and the label file is rgb 3-band format
            im = np.zeros((imt.shape[0], imt.shape[1], 3), "uint8") 
            d = read_in_labels(palette_file_name)
            im[:,:,:] = d[imt]
        elif rgb == 3:
            # the case when the label is indexed by a palette file
            # and when we want to reduce the number of classes
            im = np.zeros((imt.shape[0], imt.shape[1], 3), "uint8") 
            d = read_in_labels(palette_file_name, rgb=3)
            im[:,:,:] = d[imt]
        print (imgPath)
        misc.imsave(imgPath, im)


def batch_grayscale2rgb(in_dir, out_dir, palette_file_name, rgb=0, training_dir=''):
    # recursively iterate through all the files f in in_dir
    for root, subdirs, fl in os.walk(in_dir):
        for f in fl:
            if f.endswith(".tiff") or f.endswith(".tif"):
                fPath = os.path.join(root, f)
                grayscale2rgb(out_dir, fPath, palette_file_name, rgb, training_dir=training_dir) 
                
                

def test():
    palette_file_name = '/Users/wa.sscepano/Documents/IceEye/DL-data/clc2012_fi20m/clc2012_fi20m.clr'
    maskDir = '/Users/wa.sscepano/Documents/IceEye/DL-data/prepare/label-mask-tiffs'
    labelsDir = '/Users/wa.sscepano/Documents/IceEye/DL-data/prepare/labels-test'
    training_dir = '/Users/wa.sscepano/Documents/IceEye/DL-data/prepare/training-pngs'
    batch_grayscale2rgb(maskDir, labelsDir, palette_file_name, rgb=3, training_dir=training_dir)

#test()
