# This script verifies if there are missing flow files in given case folders.
# note: the code assumes the first flow file is number 0000000000, and the 
# bin/parameters.m file in each case folder is required to obtain the qtimes 
# values
# - giovana, 27/04/2025

import os
import re
import numpy as np

def main():
  
  address = '/home/gigiaero/results_xf1200/'
  case_folders = ['packet3D_intrd30_Re835M02_dx2dy05dz311_A0001',
                  'packet3D_intrd30_Re835M09_dx2dy05dz311_A0001',
                  'packet3D_intrd30_Re835M09_dx2dy05dz311_A001',
                  'packet3D_intrd30_Re835M09_dx2dy05dz311_A01',
                  'packet3D_intrd60_Re835M02_dx2dy05dz311_A0001',
                  'packet3D_intrd60_Re835M09_dx2dy05dz311_A0001',
                  'packet3D_intrd60_Re835M09_dx2dy05dz311_A001',
                  'packet3D_intrd60_Re835M09_dx2dy05dz311_A01',
                  'packet3D_Re835M02_dx2dy05dz311_A0001',
                  'packet3D_Re835M09_dx2dy05dz311_A0001',
                  'packet3D_Re835M09_dx2dy05dz311_A001',
                  'packet3D_Re835M09_dx2dy05dz311_A01',
                  'whitenoise3D_Re835M02_dx2dy05dz311_A0001',
                  'whitenoise3D_Re835M09_dx2dy05dz311_A0001',
                  'whitenoise3D_Re835M09_dx2dy05dz311_A001',
                  'whitenoise3D_Re835M09_dx2dy05dz311_A01']

  process(address,case_folders)
  
def process(address,case_folders):
  if address[-1] != '/':
    address = address + '/'

  print('Current directory: ' + address)

  for i in range(len(case_folders)):

    if case_folders[-1] != '/':
      case_folders[i] = case_folders[i] + '/'
      
    if os.path.isdir(address + case_folders[i]):

      files = os.listdir(address + case_folders[i])

      qtimes = int(find_parameter_value(address + case_folders[i] + 
                                        'bin/parameters.m','qtimes'))

      # Find flow files and make a list with their numbers
      flow_nums = []
      for file in files:
        if 'flow_' in file and 'diverged' not in file and 'old' not in file:
          flow_nums.append(int(file[5:15]))

      flow_nums = np.sort(flow_nums)
      qtimes_array = np.diff(flow_nums)

      if np.all(qtimes_array == qtimes):
        print('Case: ' + case_folders[i][0:-1] + ' | qtimes = ' + str(qtimes) + 
              ' | No flow files missing!')
      
      else:
        indexes = np.where(qtimes_array != qtimes)[0]
        missigno = []
        step = 0
        for idx in indexes:
          num = int(qtimes_array[idx]/qtimes)
          for j in range(1,num):
            missigno.append(qtimes*(idx + step + j))
          
          step = step + num - 1

        print('Case ' + case_folders[i][0:-1] + ' | qtimes = ' + str(qtimes))
        print(' > Missing files: ',end='')
        for n in missigno:
          print('%.10d '%n,end='')

        print('')
  
    else:
      print(case_folders[i][0:-1] + ': Directory does not exist!')

def find_parameter_value(file,parameter,make_float=True):

    with open(file,'r') as file:
      for line in file:
        if parameter in line and line[0] != '%':
          parameter_match = re.findall(parameter + r'\s*=\s*(.*)\s*;',
                                      line.strip())[0]
          if make_float:
            parameter_match = float(parameter_match)
          
          break
      
    return parameter_match

if __name__ == '__main__':
  main()
