'''
note: see readme file for instructions
'''

import os
import datetime

def main():

  # Set operation mode:
  mode = 1 # Transfer everyday at specified times
  # mode = 2 # Transfer now

  # Define hour, minute and second in list format
  # All lists must have the same length
  transfer_time_h = [7,19]
  transfer_time_m = [0,0]
  transfer_time_s = [0,0]

  # DNS folder
  address = '/home/gigiaero/GATT_DNS-main_xf1200/'

  # Case folders (which must be located in 'address')
  case_list = ['packet3D_intrd60_Re835M09_dx2dy05dz311_A005',
               'packet3D_intrd60_Re835M09_dx2dy05dz311_A01',
               'packet3D_Re835M09_dx2dy05dz311_A005',
               'whitenoise3D_Re835M02_dx2dy05dz311_A0001',
               'whitenoise3D_Re835M09_dx2dy05dz311_A0001',
               'whitenoise3D_Re835M09_dx2dy05dz311_A005',
               'whitenoise3D_Re835M09_dx2dy05dz311_A01']

  # auto_rsync_rm executable location
  executable = '/home/gigiaero/scripts/auto_rsync_rm/a.out'

  # Folder where the log files of this script are saved
  log_address = '/home/gigiaero/scripts/auto_rsync_rm/logs/'

  process(mode,transfer_time_h,transfer_time_m,transfer_time_s,address,
          case_list,executable,log_address)

def process(mode,transfer_time_h,transfer_time_m,transfer_time_s,address,
          case_list,executable,log_address):
  if address[-1] != '/':
    address = address + '/'

  if log_address[-1] != '/':
    log_address = log_address + '/'

  if mode == 1:
    
    transfer_time = []
    for i in range(len(transfer_time_h)):
      transfer_time.append(check_transfer_time(transfer_time_h[i],
                                               transfer_time_m[i],
                                               transfer_time_s[i]))

    # Transfer files every day at specified times
    while 1:
      print('Waiting until next transfer time...')
      for i in range(len(transfer_time)):
        print('%06d'%transfer_time[i])

      while 1:
        if int(datetime.datetime.now().strftime("%H%M%S")) in transfer_time:
          transfer(address,case_list,log_address,executable)
          
          break
  
  elif mode == 2:
    transfer(address,case_list,log_address,executable)

  else:
    print('Invalid mode')


def check_transfer_time(transfer_time_h,transfer_time_m,transfer_time_s):
  if transfer_time_h < 0 or transfer_time_h > 23:
    raise Exception('invalid transfer_time_h')

  if transfer_time_m < 0 or transfer_time_m > 59:
    raise Exception('invalid transfer_time_m')

  if transfer_time_s < 0 or transfer_time_s > 59:
    raise Exception('invalid transfer_time_s')

  return int(transfer_time_h*1e4 + transfer_time_m*1e2 + \
                      transfer_time_s)

def transfer(address,case_list,log_address,executable):
  now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
  log_name = log_address + 'log_' + str(now) + '.txt'

  for i in range(len(case_list)):
    os.system('echo [' + address + case_list[i] + '] | tee -a ' + log_name)

    if os.path.isdir(address + case_list[i]):
      os.system('cd ' + address + case_list[i] + '; ' + executable + 
                ' | tee -a ' + log_name)

    else:
      os.system('echo Directory does not exist! | tee -a ' + log_name)

if __name__ == '__main__':
  main()