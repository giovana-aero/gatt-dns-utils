'''
this script prints chosen info of all of a given user's jobs. So far tested on
Euler only.
- giovana, 16/05/2025, 1721 hours
'''

import subprocess
import re

def main():

  username = 'gigiaero'

  # List of parameters to obtain from qstat (written the same as they appear in
  # the qstat -f command output)
  qstat_info_list = ['Job_Name',
                     'queue',
                     'resources_used.ncpus',
                     'resources_used.walltime',
                     'Output_Path',
                     'Submit_arguments']
  # qstat_info_list = [] # Leave empty to print everything

  process(username,qstat_info_list)

def process(username,qstat_info_list):
  output = subprocess.check_output(['qstat','-u',username])
  job_ids = re.findall(r'\d+\.icex',output) # (this command will probably 
                                            # require changes depending on the
                                            # server)

  for id_num in job_ids:
    print('[job id %s]'%id_num)
    job_info = subprocess.check_output(['qstat','-f',id_num])

    if len(qstat_info_list) == 0:
      print(job_info)

    else:
      for qstat_info in qstat_info_list:
        info = re.findall(qstat_info + ' = .+',job_info)
        
        if len(info) != 0:
          print(info[0])

        else:
          print(qstat_info + ': [info not available]')

    print(' ')

if __name__ == '__main__':
  main()
