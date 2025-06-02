import os
import numpy as np
import sys
from subprocess import check_output
from time import sleep

'''
This script reads data from a given log.txt file and plots its data in text
format on a CLI. Use this to get a quick overview of a simulation's behavior.
This code was written for Linux systems.

Usage: navigate to the directory containing the chosen log.txt file and execute
this script. It doesn't need to be saved at the same directory of the log.txt
file. For example, if this script is saved at your home directory, use
> python3 ~/logError_plot_terminal.py
Suggestion: add an alias to your .bashrc file such as
alias log-error='python3 [path to script]/logError_plot_terminal.py'

Select the desired graph by entering U, V, W, R or E, and type Q to quit.
Pressing enter with no input plots the graph for the following variable, and
if the flow is 2D, the W error plot is skipped. The plot legend displays the
current variable and the axes' range as [[smallest value], [largest value]].

The plots cover a slice of the data always ending at the last values of the log
and starting somewhere along the full range. Change this parameter by adding an
integer as an argument to the script on execution. For instance, to visualize
the plots of the last 200 lines of data in the log file, use
> python3 logError_plot_terminal.py 200
If no argument is given, a default value of 500 is used.

A warning: the terminal is cleared when plotting.

- Giovana, january 2025

'''

def main():

  # Parameters
  if len(sys.argv) == 1:
    log_input_N = 500 # number of log entries to be loaded
                      # (middle of file to end)
  else:
    log_input_N = int(sys.argv[1])

  # Terminal dimensions (this defines how the plot will be formatted)
  t_height = int(check_output(["tput","lines"]).decode("utf-8"))
  t_width = int(check_output(["tput","cols"]).decode("utf-8"))
  v_margin = 3 # margin added to not crop the upper part of the plot and to fit
              # the legend

  # Get data from file
  address = check_output(["pwd"]).decode("utf-8")
  log_data = np.genfromtxt(address[:-1] + "/log.txt",skip_header=1)
  log_lines = log_data.shape[0]

  if log_input_N > log_lines:
    print("Warning: Too few lines in log file. ",end='')
    print("Setting log_input_N = log_lines = {}".format(log_lines))
    log_input_N = log_lines
    sleep(2)

  indexes = np.linspace(log_lines-log_input_N,log_lines-1,t_width).astype("int")
  U = log_data[indexes,5]
  V = log_data[indexes,6]
  W = log_data[indexes,7]
  R = log_data[indexes,8]
  E = log_data[indexes,9]
  if sum(W) == 0: two_d = True
  else: two_d = False

  # Normalize in terms of the terminal's dimensions
  U = normalize(U,t_height - v_margin)
  V = normalize(V,t_height - v_margin)
  if not two_d: W = normalize(W,t_height - v_margin)
  R = normalize(R,t_height - v_margin)
  E = normalize(E,t_height - v_margin)

  # Build the plots
  txt_plot_U = build_plot(U,t_width,t_height - v_margin)
  txt_plot_V = build_plot(V,t_width,t_height - v_margin)
  txt_plot_W = build_plot(W,t_width,t_height - v_margin)
  txt_plot_R = build_plot(R,t_width,t_height - v_margin)
  txt_plot_E = build_plot(E,t_width,t_height - v_margin)

  op = 'U'
  while op != 'q' and  op != 'Q':
    if op == 'u' or op == 'U':
      print_plot(txt_plot_U,t_width)
      plot_legend("U",5,log_data,indexes)
      op = input()

      if len(op) == 0: op = 'V'

      continue

    if op == 'v' or op == 'V':
      print_plot(txt_plot_V,t_width)
      plot_legend("V",6,log_data,indexes)
      op = input()

      if len(op) == 0 and two_d: op = 'R'
      elif len(op) == 0: op = 'W'

      continue

    if op == 'w' or op == 'W':
      print_plot(txt_plot_W,t_width)
      plot_legend("W",7,log_data,indexes)
      op = input()

      if len(op) == 0: op = 'R'

      continue

    if op == 'r' or op == 'R':
      print_plot(txt_plot_R,t_width)
      plot_legend("R",8,log_data,indexes)
      op = input()

      if len(op) == 0: op = 'E'

      continue

    if op == 'e' or op == 'E':
      print_plot(txt_plot_E,t_width)
      plot_legend("E",9,log_data,indexes)
      op = input()

      if len(op) == 0: op = 'Q'

      continue

    else:
      os.system("clear")
      print("Incorrect option | >> Next (U, V, W, R, E, or Q to quit): ",\
          end='')
      op = input()

def normalize(var,height):
  
  return ((var - min(var))/max((var - min(var)))*(height)).astype("int")

def build_plot(var,width,height):
  
  plot = []
  list_idx = 0
  for i in range(height,-1,-1):
    plot.append(" "*width)
    idx = np.where(var == i)[0]

    for j in range(len(idx)):
      plot[list_idx] = plot[list_idx][0:idx[j]] + "*" + \
                        plot[list_idx][idx[j]+1:]

    list_idx += 1

  return plot

def print_plot(plot,t_width):
  
  os.system("clear")
  for i in range(len(plot)):
      print(plot[i])

  print("-"*t_width)

def plot_legend(var,var_num,log_data,indexes):
  
  s_num_0 = log_data[indexes[0],0]
  s_num_f = log_data[indexes[-1],0]
  var_change_0 = min(log_data[indexes,var_num])
  var_change_f = max(log_data[indexes,var_num])
  print(" Variable: %c | Save number [%d, %d] | %c change [%E, %E] | "\
          %(var,s_num_0,s_num_f,var,var_change_0,var_change_f),end='')
  print(">> Next: ",end='')

if __name__ == '__main__':
  main()
