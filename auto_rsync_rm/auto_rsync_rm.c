/*
notes:
- this does not account for old_* files
- see readme file for instructions
*/

#include<stdio.h>
#include<dirent.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<stdbool.h> 

double power(double x,int p);
double get_flow_number(char flow[20]);

int main(){

  bool test_mode = true; // Set to true or false. When true, the rsync and rm
                          // commands will be printed to screen and not be 
                          // executed

  // rsync settings
  char destination_server[] = "gigiaero@143.107.181.107:"; // Must end with :
  char destination_port[] = " -e 'ssh -p 3201'"; // Must begin with space
  char destination_folder[] = "~/results_xf1200"; // Do not include the last bar
  char case_folder[500];
  char current_dir[500];

  DIR *address;
  struct dirent *files;
  address = opendir(".");
  // char filenames[500][20];
  int i=0,j=0,k=0,flowfiles=0,bar_idx;
  int status;
  double max_flow_num=0.,flow_num=0.;
  int max_flow_idx=0;

  if(address){

    // Count the number of flow files 
    puts("Reading directory...");
    while((files = readdir(address)) != NULL){
      if(((int)(files->d_name[0])) == ((int)'f') && 
         ((int)(files->d_name[1])) == ((int)'l') && 
         ((int)(files->d_name[2])) == ((int)'o') &&
         ((int)(files->d_name[3])) == ((int)'w')){
        flowfiles++;
      }
    }

    // Get the name of the flow files
    char flows[flowfiles][20];
    address = opendir(".");
    while((files = readdir(address)) != NULL){
      for(j=0;j<=20;j++){
        if(((int)(files->d_name[0])) == ((int)'f') && 
           ((int)(files->d_name[1])) == ((int)'l') && 
           ((int)(files->d_name[2])) == ((int)'o') &&
           ((int)(files->d_name[3])) == ((int)'w'))
          flows[i][j] = files->d_name[j];
      }

      if(((int)(files->d_name[0])) == ((int)'f') && 
         ((int)(files->d_name[1])) == ((int)'l') && 
         ((int)(files->d_name[2])) == ((int)'o') &&
         ((int)(files->d_name[3])) == ((int)'w')){
        i++;

        // This feature is necessary to ensure that the flow excluded from rsync
        // is the last. Relying on the order of the files is not enough because
        // readdir sometimes reads the files out of order
        flow_num = get_flow_number(files->d_name);
        if(flow_num > max_flow_num){
          max_flow_num = flow_num;
          max_flow_idx = i - 1;
        }
      }
    }

    closedir(address);

    // Get working path
    if(getcwd(current_dir,sizeof(current_dir)) != NULL)
        printf("Current working dir: %s\n",current_dir); 
    else{
        perror("getcwd() error");
        return 2;
    }

    // Detect the current case folder
    i = 0;
    while(current_dir[i] != '\0'){
      if(((int)current_dir[i]) == ((int)'/'))
        bar_idx = i;
      
      i++;
    }
    
    // Get case name from the complete directory
    k = 0;
    for(j=bar_idx;j<i;j++,k++)
      case_folder[k] = current_dir[bar_idx + k];
    case_folder[k] = '\0';

    printf("Case folder: %s\n",case_folder);
    printf("Number of flow files: %d\n",flowfiles);

    if(flowfiles <= 1){
      puts("Not enough flow files. Transfer cancelled.");
      return 1;
    }

    // Get only the flow files
    // (where 20 is the length of a flow file name + a single space, and the +1
    // represents the '\0' character, ignoring the last flow file)
    char flow_list[20*(flowfiles - 1) + 1];
    k = 0;
    for(i=0;i<flowfiles;i++){
      if(i != max_flow_idx){ // Include all flow files except the last one
        for(j=0;j<19;j++){
          flow_list[k] = flows[i][j];
          k++;
        }
        flow_list[k] = ' ';
        k++;
      }
    }
    flow_list[k] = '\0';
    
    // Check if flow_0000000000.mat exists. If so, transfer everything but the
    // last flow file
    // Here 48 contains the strings in the first two strcats below and 500*3 
    // contains the destination info
    char command[20*(flowfiles - 1) + 48 + 500*3];
    // char* command = (char*) malloc(0*(flowfiles - 1) + 48 + 500*3);
    if(strcmp(flows[0],"flow_0000000000.mat") == 0){
      puts("flow_0000000000.mat present");

      // Configure rsync command
      strcat(command,"rsync -Paz ");
      strcat(command,"bin log.txt meanflowSFD.mat mesh.mat ");
      strcat(command,flow_list);
      strcat(command,destination_server);
      strcat(command,destination_folder);
      strcat(command,case_folder);
      strcat(command,destination_port);
    }
    // If not, transfer only the flow files (except the last) and log.txt
    else{
      strcat(command,"rsync -Paz ");
      strcat(command,"log.txt ");
      strcat(command,flow_list);
      strcat(command,destination_server);
      strcat(command,destination_folder);
      strcat(command,case_folder);
      strcat(command,destination_port);
    }

    // Execute rsync
    printf("Destination server: %s\n",destination_server);
    printf("Destination folder: %s\n",destination_folder);
    
    if(test_mode){
      puts(command);
      status = 0;
    }
    else
      status = system(command);
    
    // Remove flow files (only if rsync finished nominally)
    if(status == 0){
      puts("rsync done. Deleting flow files...");
      command[0] = '\0';
      strcat(command,"rm -v ");
      strcat(command,flow_list);
      
      if(test_mode)
        puts(command);
      else
        system(command);
      putchar('\n');
    }
    else{
      puts("Error: rsync did not finish. Keeping files.");
      putchar('\n');
      // free(command);
      return 3;
    }

    // free(command);

  }

  else{
    puts("Address error");
    return 4;
  }

  return 0;
}

// Added this function to avoid having to include math.h 
double power(double x,int p){
  int i;
  double y=1.;

  for(i=0;i<p;i++)
    y *= x;

  return y;
}

double get_flow_number(char flow[20]){
  // Using doubles here because an int would overflow
  double num=0.; 
  int i,p=9;

  for(i=5;i<=14;i++,p--)
    num += ((double)flow[i] - 48.)*power(10.,p);
  // printf("%10.0f\n",num);

  return num;
}
