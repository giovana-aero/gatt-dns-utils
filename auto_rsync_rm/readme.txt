instructions to configure the auto_rsync_rm programs. to illustrate, the 
examples will follow my setup to backup DNS cases from euler to sisifo.
lines beginning with "$" represent terminal commands.

1.set up public keys to execute rsync and ssh commands without password:
  https://www.thegeekstuff.com/2011/07/rsync-over-ssh-without-password/
  example: here, the local server would be euler, and the remote host would be 
  sisifo. the following steps are done on the local server.
  as instructed in the link above, verify you can use ssh and rsync without
  passwords.

2.create folders to store the source code and the transfer log files.
  example:
  $ mkdir ~/scripts
  $ mkdir ~/scripts/auto_rsync_rm        # scripts are saved here
  $ mkdir ~/scripts/auto_rsync_rm/logs   # logs are saved here

3.make a symbolic link to ~/.ssh:
  $ ln -s ~/.ssh .
  the above command must be executed in the same directory as the auto_rsync_rm
  programs. in the example, that directory would be "~/scripts/auto_rsync_rm".

4.set up the C program parameters. for now, set test_mode to true and adjust the
  following variables:
  > destination_server -> [username]@[server ip] (must end with ':')
  > destination_port -> -e 'ssh -p [port number]' (must begin with a space)
  > destination_folder -> directory where you store your DNS results (must not 
                          end with '/')
  all above parameters are referent to the remote host (in the present example, 
  that would be sisifo). these strings must be enclosed with double quotes. for 
  clarification, the destination_folder directory is intended to contain 
  multiple DNS case folders.
  example: check auto_rsync_rm.c to see my setup.
  
5.compile the C program:
  $ gcc auto_rsync_rm.c
  the executable will most probably be named "a.out".

6.set up the python program parameters:
  > mode -> set to 1 to transfer everyday at specified times, and set to 2 to 
            transfer the moment you run the script. for now, to test the setup,
            set "mode = 2".
  > transfer_time_h -> list containing the time for transfers (hours)
  > transfer_time_m -> same as above, for minutes
  > transfer_time_s -> same as above, for seconds
  > address -> directory of the DNS code (which we assume will contain the 
               simulation files)
  > case_list -> a list containing the names of all case folders which you want
                 to transfer
  > executable -> path to the C program's executable compiled in step 5
  > log_address -> directory where the logs of the transfers will be saved
  note that, even if you set only one daily time to transfer, the transfer_time
  variables still should be written as lists (that is, for instance, 
  "transfer_time_h = [7]" and so on).
  the variables address, case_list, executable and log_address are referent to 
  the local server (in the present example, euler)
  example: check exec_auto_rsync_rm.py to see my setup.

7.run the exec_auto_rsync script.
  example:
  $ python2.7 exec_auto_rsync.py
  verify the output on screen and in the log file. compare the listed files in
  the commands to the files in the folders.
  if everything is good, continue to the next step.

8.open the C code again, and set test_mode to false. compile the program again
  as done in step 5.

9.create a screen to run the python script.
  example:
  $ screen -S rsync-screen
  reminders:
  $ screen -ls               # lists all screens
  $ screen -r [screen name]  # attaches to a screen
  $ exit                     # in a screen to terminate it
  and ctrl + a + d exits a screen without terminating it.

10.run the exec_auto_rsync.py script.
  example:
  $ clear; python2.7 exec_auto_rsync.py   # where "clear" clears the terminal
  to stop, ctrl + c on the terminal.

00.observations
  - backup files (old_flow_* and old_meanFlowSFD_* files) saved from the 
    meanflow.m script are ignored in the transfers
  - in the first transfer of a given case, all files are sent except the last
    flow file. for subsequent transfers, only the log.txt and the flow files
    except the last are sent. the last flow file is kept to make it easier to 
    continue simulations which were interrupted.

- giovana, 02/06/2025, 1404 hours
