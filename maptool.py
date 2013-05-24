import re
import os
import sys
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))

# root of SD card
path_to_sdcard="/s21/studium/projekte/wordpress/20130521_lumix_map_tool/sdcard"
mapdata_on_sdcard = path_to_sdcard + "/PRIVATE/MAP_DATA"

# MAP_DATA directory of DVD
path_to_mapdata="/s22/data/lumix_map_data/"

# comma-separated regions
#01 - Japan
#02 - South Asia, Southeast Asia
#03 - Oceania
#04 - North America, Central America
#05 - South America
#06 - Northern Europe
#07 - Eastern Europe
#08 - Western Europe
#09 - West Asia, Africa
#10 - Russia, North Asia
regions="6;7"

mapdata_filename = script_dir + "/MapList.dat"

mapdata_lines = open(mapdata_filename, 'r').readlines()

if not re.match("^(\d;)*\d$", regions):
  print "Region list needs to be a semicolon-separated list of integers"
  sys.exit(1)

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
  print "Region" , selected_region_id
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
