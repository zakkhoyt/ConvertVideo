#!/usr/bin/env python

# This script accepts an input video file and will convert it to mpeg4
# in one of two sizes. Either the default size or cif (352x288). 
# The output file's path name will be equal to the input's file path from 
# the root directory given as the argument. This allows for mirroring directories

# Mandatory parameters are as follows:
# Param1: input video file (mp4, mpg, avi, etc.....)
# Param2: output directory (../output/)
# Param3: output video size <Default|iPhone> (default it Default)

# Optional parameters:
# Param 4: -n		Print the processing commands, but do not execute

# Example use for single file without action (mac)
# python convert_video.py favorite_category/even_better_subcategory/great_video.mpg output iPhone -n
# Example use for single file (mac)
# python convert_video.py favorite_category/even_better_subcategory/great_video.mpg output iPhone

# Example batch use. Pipe files into script without processing (mac):
# find ../my_videos | grep ".flv\|.avi\|.mpg\|.wmv\|.mpeg\|.m4v" | xargs -I input_file python convert_video.py input_file out Default -n
# Example batch use. Pipe files into script (mac):
# find ../my_videos | grep ".flv\|.avi\|.mpg\|.wmv\|.mpeg\|.m4v" | xargs -I input_file python convert_video.py input_file out Default

# TODO: Add auto renaming
# TODO: Allow different output formats

import sys
import os

if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1].find('copy') > -1:
			sys.stdout.write('Example batch usage:\n')
			sys.stdout.write('find ../bin/! | grep ".flv\|.avi\|.mpg\|.wmv\|.mpeg\|.m4v" | xargs -I input_file python convert_video.py input_file out iPhone\n')
			os.system('echo find ../bin/! | grep \\".flv\|.avi\|.mpg\|.wmv\|.mpeg\|.m4v\\" | xargs -I input_file python convert_video.py input_file out iPhone | pbcopy')
			sys.exit(0)

	if len(sys.argv) <= 3:
		sys.stderr.write('Usage: ' + sys.argv[0] + ' <input_video> <output_dir> <Defult|iPhone>\n')
		sys.exit(2)
	
	
	vid_input = sys.argv[1]
	vid_output_dir = sys.argv[2]
	vid_size = sys.argv[3]
	if len(sys.argv) > 4:
		other_arg = sys.argv[4]
	else:
		other_arg = '';
	convert_command = ''


	# Get the base path to the input file so we can recreate the same dir structure for output
	vid_input = vid_input.replace('//', '/')
	base_path = vid_input[vid_input.find('/'):len(vid_input)]	
	base_path = base_path[0:base_path.rfind('/')]

	# Get the base file name of the input vid and append new extension
	input_file = os.path.splitext(vid_input)[0]
	input_file = input_file.replace('//', '/')
	tokens = input_file.split('/')
	input_file = tokens[len(tokens)-1]

	# Create path to output dir
	new_dir = '"' + vid_output_dir + base_path + '"'
	new_dir = new_dir.replace('//', '/')

	# Check if we want to put example on the clipboard

	# Create new file name
	output_file = vid_output_dir + '/' + base_path + '/' + input_file + '.mp4'
	output_file = output_file.replace('//', '/')

	if vid_size != 'Default' and vid_size != 'iPhone':
		sys.stderr.write('Usage: ' + sys.argv[0] + ' <input> <output> <Defult|iPhone>\n')
		sys.exit(2)

	# Only convert the file if output_file doensn't already exist
	if os.path.isfile(output_file):
		sys.stdout.write('************** ' + output_file + ' already exists.... skipping\n')
	else:
		os.system('mkdir -p ' + new_dir)
		if vid_size == 'Default':
			convert_command = 'ffmpeg -i ' + '"' + vid_input + '"' + ' -y -f mp4 -strict -2 -sameq ' + '"' + output_file + '"'
		elif vid_size == 'iPhone':
			convert_command = 'ffmpeg -i ' + '"' + vid_input + '"' + ' -y -f mp4 -s cif -b 128 -strict -2 -sameq ' + '"' + output_file + '"'

	# Print out the command and paths
	sys.stdout.write('--------------------------------------------\n')
	sys.stdout.write('Platform: ' + sys.platform + '\n')
	sys.stdout.write('new_dir: ' + new_dir + '\n')
	sys.stdout.write('Input file: ' + vid_input + '\n')
	sys.stdout.write('Output file: ' + output_file + '\n')
	sys.stdout.write('Converstion command: ' + convert_command + '\n')
	sys.stdout.write('--------------------------------------------\n')
	if other_arg.find('-n') < 0:
		os.system(convert_command)

sys.exit(0)

