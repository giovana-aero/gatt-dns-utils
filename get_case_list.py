'''
this script searches and prints the names of case folders inside a given path.
set frmt to true to print the names formmated conveniently to paste to the 
case_list variable in exec_auto_rsync_rm.py.

note: comment/uncomment lines 37 and 38 depending on if you are using python 2
or python 3

- giovana, 02/06/2025, 1446 hours
'''

import re
import subprocess

def main():

  # Folder where the cases are saved
  address = '/home/gigiaero/GATT_DNS-main_xf1200'

  # Keywords in the case names
  names = ['baseflow','packet3D','whitenoise3D']

  # Print formatting to case_list (set to true or false)
  frmt = 1

  process(address,names,frmt)

def process(address,names,frmt):
  if address[-1] != '/':
    address = address + '/'

  address_list_complete = str(subprocess.check_output('ls -d1 ' + address +'*/',
                              shell=True))

  case_list = []
  for name in names:
    output = re.findall(address + '(.*' + name + '.*)/',address_list_complete)

    if len(output) != 0:
      case_list += output

  if frmt:
    print(version_info[0])
    if version_info[0] == 3:
      print '[',        # use this in python2
      # print('[',end='') # use this in python3

    for i in range(len(case_list) - 1):
      print('\'' + case_list[i] + '\',')
    
    print('\'' + case_list[i] + '\']')

  else:
    for case in case_list:
      print(case)
