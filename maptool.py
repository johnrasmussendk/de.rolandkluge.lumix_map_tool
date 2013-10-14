#!/usr/bin/python

#
# This tool is a very simple re-engineered version of the Lumix Map Tool.
#
# It may be used for copying detailed geographic data to the camera's SD card.
# To get an idea, of how the tool is used, execute
#
#  python maptool.py --help
#
# Author: Roland Kluge
#

import re
import os
import sys
import shutil
import getopt

script_dir = os.path.dirname(os.path.abspath(__file__))

def main():  
  
  regions, path_to_mapdata, path_to_sdcard = parse_and_verify_args()
  
  mapdata_on_sdcard = path_to_sdcard + "/PRIVATE/MAP_DATA"

  mapdata_filename = script_dir + "/MapList.dat"
  mapdata_lines = open(mapdata_filename, 'r').readlines()

  current_region_id = -1;
  filelist = []
  files_per_region = []
  for line in mapdata_lines:
    line = line.strip()
    if re.match("^\d\d", line):
      current_region_id = int(line)
      filelist = []
      files_per_region.append(filelist)
    elif re.match("^\d/BACK\d\d\d.KWI", line):
      filelist.append(line)
    
  shutil.rmtree(mapdata_on_sdcard, ignore_errors = True)
  os.makedirs(mapdata_on_sdcard)

  for selected_region_id in regions.split(";"):
    print "Copying region " + selected_region_id + " ..."
    for path in files_per_region[int(selected_region_id)]:
      # print "Copy file" , path
      
      subdir = path.split("/")[0];
      filename = path.split("/")[1];
      
      abspath_to_source_file = path_to_mapdata + "/" + path
      target_dir = mapdata_on_sdcard + "/" + subdir
      target_file = target_dir + "/" + filename
      
      if not os.path.exists(target_dir):
        os.mkdir(target_dir)
      
      if not os.path.exists(target_file):
        shutil.copy(abspath_to_source_file, target_dir)
    print "Copying region " + selected_region_id + " DONE"
    
  print "All operations exited succesfully."

def parse_and_verify_args():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:m:r:", ["help", "sdcard=", "mapdata=", "regions="])
  except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)
    
  path_to_sdcard = None
  path_to_mapdata = None
  regions = None
    
  for o, a in opts:
    if o in ("-h", "--help"):
      print usage()
      sys.exit()
    elif o in ("-s", "--sdcard"):
      path_to_sdcard = a
    elif o in ("-m", "--mapdata"):
      path_to_mapdata = a  
    elif o in ("-r", "--regions"):
      regions = a
      
  if regions is None or not re.match("^(\d+;)*\d+$", regions):
    print "Region list needs to be a semicolon-separated list of integers but was '" + str(regions) + "'"
    sys.exit(1)
  if path_to_sdcard is None or not os.path.exists(path_to_sdcard):
    print path_to_sdcard
    print "Option --sdcard is mandatory and needs to be an existing path"
    sys.exit(1)
  if path_to_mapdata is None or not os.path.exists(path_to_sdcard):
    print "Option --mapdata is mandatory and needs to be an existing path"
    sys.exit(1)
      
  return [regions, path_to_mapdata, path_to_sdcard]

def usage():
  return "Usage: " + __file__ + """: --regions="<regions>" --mapdata="<path-to-mapdata>" --sdcard="<path-to-sdcard>" 
(The quotes around parameter values are obligatory!)

-h
--help
  Print help
  
-r
--regions 
  The semicolon-separated indices of the regions to copy. E.g. 1;6;10. At least 
  one region needs to be given.
   1 - Japan
   2 - South Asia, Southeast Asia
   3 - Oceania
   4 - North America, Central America
   5 - South America
   6 - Northern Europe
   7 - Eastern Europe
   8 - Western Europe
   9 - West Asia, Africa
  10 - Russia, North Asia

-m
--mapdata 
  Path to the directory containing the map data. The referenced directory
  should contain be the folder MAP_DATA on the DVD.

-s
--sdcard  
  Path to sdcard. The tool will create subdirectories PRIVATE/MAP_DATA below this 
  path and copy the appropriate files.
  
Example:
  
python mapdata.py --regions="6;7;8;10" --mapdata="/media/dvd/MAP_DATA" --sdcard="/media/sdcard"
python mapdata.py -r "6;7;8" -m "/media/dvd/MAP_DATA" -s "/media/sdcard"
  """

main()
