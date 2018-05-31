#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:31:41 2018

@author: sanja7s
"""
import create_Corine_mask
import split_images
import grayscale2rgb
import dec_norm_scale
import os, sys
   
"""
the steps:
    -- first slice the SAR image file
    -- then convert to decibels, normalize (to normal distribution) and scale to (0,255) each band
    -- then create corresponding mask label pieces from Corine
    -- then remove border slices and single labels (pairs)
"""

test = 0
training = 1
labels = 1


current_dir = os.path.abspath(os.path.dirname(__file__))
#print ('project', current_dir)
if test:
    working_DIR = os.path.join(current_dir, '../../data/DL_prepare/TEST/')
    #print ('working_DIR',working_DIR)
else:
    working_DIR = os.path.join(current_dir, '../../data/DL_prepare/')


# need to provide the directory with prepared SAR images   
original_dir = os.path.join(working_DIR,'prepared-SAR-tiffs')

original_cropped_dir = os.path.join(working_DIR,'cropped-SAR-tiffs')

training_dir = os.path.join(working_DIR,'train')
labels_dir = os.path.join(working_DIR,'labels')

# the rest of the neccessary directory structure will be created if not exists
for output_path in [original_cropped_dir, training_dir, labels_dir]:
    if not os.path.exists(output_path):
        os.makedirs(output_path) 

# the path to the Corine mask and corresponding palette file
m = os.path.join(current_dir, '../../data/DL_prepare/Corine/clc2012_fi20m.tif') 
palette_file_name = os.path.join(current_dir, '../../data/DL_prepare/Corine/clc2012_fi20m.clr') 


##########################################################################################################
if training:
    """
        -- slice the file into training images
    """
    split_images.batchSplit(original_dir, original_cropped_dir)

    """
        -- prepare training images for DL
    """
    dec_norm_scale.batch_dec_norm_scale(original_cropped_dir, training_dir)
    

if labels:
    """
        -- create Corine mask labels corresponding to training images
    """
    create_Corine_mask.batch_create_mask(m, training_dir, labels_dir, type_of_mask = 'Corine', palette_file_name=palette_file_name)
##########################################################################################################
