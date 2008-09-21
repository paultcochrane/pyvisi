#!/usr/bin/env python

# $Id$

import time
import os

# read in directory name (give a default value)
in_dirname = "vtk"
prompt_text = "Enter the input directory name: (default: %s) " % in_dirname
input = raw_input(prompt_text)
if input is not '':
    in_dirname = input

# read in input filename stem (give a default value)
in_fname_stem = "frame_"
prompt_text = "Enter the input filename stem: (default: %s) " % in_fname_stem
input = raw_input(prompt_text)
if input is not '':
    in_fname_stem = input

# read in output directory (give a default value)
out_dirname = "vtk"
prompt_text = "Enter the output directory name: (default: %s) " % out_dirname
input = raw_input(prompt_text)
if input is not '':
    out_dirname = input

# read in output filename stem (give a default value)
out_fname_stem = "frame_"
prompt_text = "Enter the output filename stem: (default: %s) " % out_fname_stem
input = raw_input(prompt_text)
if input is not '':
    out_name_stem = input

# read in vertical tag cut height (give a default value)
vertical_cut_height_str = "0.0"
prompt_text = "Enter the vertical tag cut height: (default: %s) " % vertical_cut_height_str
input = raw_input(prompt_text)
if input is not '':
    vertical_cut_height_str = input
vertical_cut_height = float(vertical_cut_height_str)

# read in elevation angle (give a default value)
elevation_angle_str = "0.0"
prompt_text = "Enter the elevation angle: (default: %s) " % elevation_angle_str
input = raw_input(prompt_text)
if input is not '':
    elevation_angle_str = input
elevation_angle = float(elevation_angle_str)

# read in view radius (give a default value)
view_radius_str = "70.0"
prompt_text = "Enter the view radius: (default: %s) " % view_radius_str
input = raw_input(prompt_text)
if input is not '':
    view_radius_str = input
view_radius = float(view_radius_str)

# get the date as well
date_str = time.asctime()

## write out xml file with info
fp = open("lsm_config.xml", "w")
fp.write("<?xml version=\"1.0\"?>\n")
fp.write("<tsm_config>\n")

# write out the date
fp.write("    <date>%s</date>\n" % date_str)

# write out directory name
fp.write("    <input_directory>%s</input_directory>\n" % in_dirname)

# write out input filename stem
fp.write("    <input_filename>%s</input_filename>\n" % in_fname_stem)

# write out output directory
fp.write("    <output_directory>%s</output_directory>\n" % out_dirname)

# write out output filename stem
fp.write("    <output_filename>%s</output_filename>\n" % out_fname_stem)

# write out vertical tag cut height
fp.write("    <vertical_cut_height>%g</vertical_cut_height>\n" % vertical_cut_height)

# write out elevation angle
fp.write("    <elevation_angle>%g</elevation_angle>\n" % elevation_angle)

# write out view radius
fp.write("    <view_radius>%g</view_radius>\n" % view_radius)

fp.write("</lsm_config>\n")
fp.close()


