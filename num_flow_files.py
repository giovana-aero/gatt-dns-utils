'''
when called from inside a case folder, this will print the number of flow 
files in that folder only. if called from a folder with multiple cases, the
number of files from all cases will be printed (not recursive)
- giovana, 30/05/2025, 1632 hours
'''

# instructions: navigate to a given folder containing files to be counted and
# run this script, such as
# 
# $ python3 /home/gigiaero/scripts/num_flow_files.py
#
# suggestion: include an alias in your .bashrc to avoid having to type the 
# complete command everytime, like
#
# > alias num_flow_files='python3 /home/gigiaero/scripts/num_flow_files.py'

import subprocess
import os

def main():

  # Get current address and file list
  address = subprocess.check_output(['pwd']).decode("utf-8")[0:-1]
  files = os.listdir(address)

  # Check if the current folder contains flow files
  num_flows = count_flow_files(files)

  # Single case
  if num_flows != 0:
    num_flows = count_flow_files(files)
    print('%s | %d flow files'%(address,num_flows))
  
  # Multiple cases inside the present folder
  else:
    entry_list = []
    for entry in files:
      if os.path.isdir(address + '/' + entry):
        entry_list.append(address + '/' + entry)
    
    entry_list.sort()

    for entry in entry_list:
      files = os.listdir(entry)
      num_flows = count_flow_files(files)

      if num_flows == 0:
        print('%s is not a DNS case folder'%entry)
      
      else:
        print('%s | %d flow files'%(entry,num_flows))

def count_flow_files(files):
  num_flows = 0
  for file in files:
    if 'flow_' in file and '.mat' in file:
      num_flows += 1
  
  return num_flows

if __name__ == '__main__':
  main()