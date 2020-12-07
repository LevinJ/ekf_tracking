# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.  
#
# Purpose of this file : Loop over all frames in a Waymo Open Dataset file
#                        and perform basic operations on the data
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

##################
## Imports

## general package imports
import os
import sys
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
import copy
import zlib

## Add current working directory to path
sys.path.append(os.getcwd())

## Waymo open dataset reader
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils
from tools.waymo_reader.simple_waymo_open_dataset_reader import WaymoDataFileReader, dataset_pb2, label_pb2
 
##################
## Set parameters and perform initializations

## Select Waymo Open Dataset file and frame numbers
# data_filename = 'training_segment-1005081002024129653_5313_150_5333_150_with_camera_labels.tfrecord' # Sequence 1
data_filename = 'training_segment-10072231702153043603_5725_000_5745_000_with_camera_labels.tfrecord' # Sequence 2
# data_filename = 'training_segment-10963653239323173269_1924_000_1944_000_with_camera_labels.tfrecord' # Sequence 3
show_only_frames = [1, 5] # show only frames in interval for debugging

## Prepare Waymo Open Dataset file for loading
data_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataset', data_filename) # adjustable path in case this script is called from another working directory
results_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results')
datafile = WaymoDataFileReader(data_fullpath)
datafile_iter = iter(datafile)  # initialize dataset iterator


## Selective execution and visualization
exec_lidar = [] # options are 
exec_visualization = [] # options are 
exec_list = exec_lidar + exec_visualization
vis_pause_time = 0 # set pause time between frames in ms (0 = stop between frames until key is pressed)

##################
## Perform detection & tracking over all selected frames

cnt_frame = 0 

while True:
    try:
        #################################
        ## Get next frame from Waymo dataset

        frame = next(datafile_iter)
        if cnt_frame < show_only_frames[0]:
            cnt_frame = cnt_frame + 1
            continue
        elif cnt_frame > show_only_frames[1]:
            print('reached end of selected frames')
            break
        
        print('------------------------------')
        print('processing frame #' + str(cnt_frame))


        ## C1-3-Ex1 : Extract data structure 'lidar' for TOP lidar and 'camera' for FRONT camera
        lidar_name = dataset_pb2.LaserName.TOP
        lidar = [obj for obj in frame.lasers if obj.name == lidar_name][0]
        camera_name = dataset_pb2.CameraName.FRONT
        camera = [obj for obj in frame.images if obj.name == camera_name][0]
        
        ## C1-3-Ex2 : Visualize the camera image 
        from PIL import Image
        import io
        image = np.array(Image.open(io.BytesIO(camera.image)))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        dim = (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5))
        resized = cv2.resize(image, dim)
        cv2.imshow("Front-camera image", resized)
        cv2.waitKey(0)

        #################################
        ## Extract range image data

        ## extract actual range image
        lidar_name = dataset_pb2.LaserName.TOP
        laser = [obj for obj in frame.lasers if obj.name == lidar_name][0] # get laser data structure from frame
        if len(laser.ri_return1.range_image_compressed) > 0: # use first response
            ri = dataset_pb2.MatrixFloat()
            ri.ParseFromString(zlib.decompress(laser.ri_return1.range_image_compressed))
            ri = np.array(ri.data).reshape(ri.shape.dims)
            print(ri.shape)

        ## extract sensor calibration
        lidar_calib = [obj for obj in frame.context.laser_calibrations if obj.name == lidar_name][0] # get laser calibration
        min_pitch = lidar_calib.beam_inclination_min
        max_pitch = lidar_calib.beam_inclination_max
        print('min. pitch = ' + str(round(min_pitch*180/np.pi,2)) + '°, max. pitch = '
              + str(round(max_pitch*180/np.pi,2)) + '°, pitch range = '
              + str(round((max_pitch-min_pitch)*180/np.pi,2)) + '°')

        ## display range image data (range and intensity)
        print('max. range = ' + str(round(np.amax(ri[:,:,0]),2)) + 'm')
        print('min. range = ' + str(round(np.amin(ri[:,:,0]),2)) + 'm')

        ## visualize negative range image entries
        ri_range = np.zeros(ri[:,:,0].shape)
        ri_range[ri[:,:,0]==-1] = 255
        cv2.imshow("WindowNameHere", ri_range)
        cv2.waitKey(0)
        # ri_range = range_image[:,:,0] * 256 / (np.amax(range_image[:,:,0]) - np.amin(range_image[:,:,0]))



        ## Perform a task
        if 'task-1' in exec_list:
            print('executing task 1')
            
            
        # increment frame counter
        cnt_frame = cnt_frame + 1    

    except StopIteration:
        # if StopIteration is raised, break from loop
        break


#################################
## Post-processing
