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
      
  if regions is None or not re.match("^(\d;)*\d$", regions):
    print "Region list needs to be a semicolon-separated list of integers but was '" + str(regions) + "'\n"
    print usage()
    sys.exit(1)
  if path_to_sdcard is None:
    print usage()
    sys.exit(1)
  if path_to_mapdata is None:
    print usage()
    sys.exit(1)
      
  return [regions, path_to_mapdata, path_to_sdcard]

def usage():
  return "Usage: " + __file__ + """: --regions <regions> --mapdata <path-to-mapdata> --sdcard <path-to-sdcard>
-r
--regions 
  Comma-separated list of integers.
  01 - Japan
  02 - South Asia, Southeast Asia
  03 - Oceania
  04 - North America, Central America
  05 - South America
  06 - Northern Europe
  07 - Eastern Europe
  08 - Western Europe
  09 - West Asia, Africa
  10 - Russia, North Asia

-m
--mapdata 
  Path to the directory containing the map data. The referenced directory
  should contain be the folder MAP_DATA on the DVD.

-s
--sdcard  
  Path to sdcard. The tool will create subdirectories PRIVATE/MAP_DATA.
  """

main()
