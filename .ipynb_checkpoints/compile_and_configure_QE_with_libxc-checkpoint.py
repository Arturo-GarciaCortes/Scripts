######CODE TO CONFIGURE/COMPILE QUANTUM ESPRESSO#######

#!!!! This code needs to be run into the main directory of QE !!!!!

#Import libraries that allows us to navigate and run commands in terminal
import subprocess
import os
 
make_file = 'make.inc'

##FUNCTIONS TO EDIT THE MAKE.INC FILE
def modify_cmake_dflags(make_file):
    # Open the make file in read and write mode ('r+')
    with open(make_file, 'r+') as file:
        # Read all lines into a list
        lines = file.readlines()

        # Initialize a counter to keep track of the number of occurrences found
        dflags_occurrence = 0
        
        # Iterate through each line in the list
        for i, line in enumerate(lines):
            # Check if it is the line we want to modify (DFLAGS)
            if 'DFLAGS         =  -D__FFTW -D__MPI' in line:
                # Increment the occurrence count
                dflags_occurrence += 1

                # When it is the second occurrence:
                if dflags_occurrence == 1:
                    # Find the index of 'DFLAGS' word in the line
                    index = line.find('DFLAGS')

                    # Replace the line to add -D__LIBXC to DFLAGS as requested by QE
                    lines[i] = 'DFLAGS         =  -D__FFTW -D__LIBXC -D__MPI\n'

        # Move the file pointer to the beginning of the file
        file.seek(0)

        # Write the modified lines back to the file
        file.writelines(lines)

        # Truncate the remaining content in the file after the new content to ensure we're not editing more lines
        file.truncate()
        
    return 0
        
def modify_cmake_iflags(make_file):
    # Open the make file in read and write mode ('r+')
    with open(make_file, 'r+') as file:
        # Read all lines into a list
        lines = file.readlines()

        # Initialize a counter to keep track of the number of occurrences found
        iflags_occurrence = 0
        
        # Iterate through each line in the list
        for i, line in enumerate(lines):
            # Check if it is the line we want to modify (IFLAGS)
            if 'IFLAGS         = -I$(TOPDIR)/include' in line:
                # Increment the occurrence count
                iflags_occurrence += 1

                # When it is the second occurrence:
                if iflags_occurrence == 1:
                    # Find the index of 'IFLAGS' in the line
                    index = line.find('IFLAGS')

                    # Replace the line to add -I/path/to/libxc/include/ for using libxc
                    lines[i] = 'IFLAGS         = -I$(TOPDIR)/include -I$(TOPDIR)/FoX/finclude -I/home/agarcia8/libxc/include/\n'

        # Move the file pointer to the beginning of the file
        file.seek(0)

        # Write the modified lines back to the file
        file.writelines(lines)

        # Truncate the remaining content in the file after the new content to ensure we're not editing more lines
        file.truncate()
        
    return 0
    
def modify_cmake_ldlibs(make_file):
    # Open the make file in read and write mode ('r+')
    with open(make_file, 'r+') as file:
        # Read all lines into a list
        lines = file.readlines()

        # Initialize a counter to keep track of the number of occurrences found
        ldlibs_occurrence = 0
        
        # Iterate through each line in the list
        for i, line in enumerate(lines):
            # Check if it is the line we want to modify
            if 'LD_LIBS        =' in line:
                # Increment the occurrence count
                ldlibs_occurrence += 1

                # When it is the second occurrence:
                if ldlibs_occurrence == 1:
                    
                    index = line.find('LD_LIBS')

                    # set LD_LIBS=-L/path/to/libxc/lib/ -lxcf03 -lxc for using libxc
                    lines[i] = 'LD_LIBS=-L/home/agarcia8/libxc/lib/ -lxcf03 -lxc\n'
        # Move the file pointer to the beginning of the file
        file.seek(0)

        # Write the modified lines back to the file
        file.writelines(lines)

        # Truncate the remaining content in the file after the new content to ensure we're not editing more lines
        file.truncate()
        
    return 0

## MAKE THE MODIFICATIONS TO THE C PARAMETER

# Open the .f90 file in read and write mode ('r+')
with open(routines_file, 'r+') as file:
    # Read all lines into a list
    lines = file.readlines()

    # Initialize a counter to keep track of the number of occurrences found
    occurrence_count = 0

    # Iterate through each line in the list
    for i, line in enumerate(lines):
        # Check if 'tb09_param' is in the line
        if 'tb09_param' in line:
            # Increment the occurrence count
            occurrence_count += 1

            # When it is the second occurrence:
            if occurrence_count == 2:
                # Find the index of 'tb09_param' in the line
                index = line.find('tb09_param')

                # Modify the line to include the new value of 'c_param'
                lines[i] = line[:index + 13] + c_param + ' ! c parameter value\n'

    # Move the file pointer to the beginning of the file
    file.seek(0)

    # Write the modified lines back to the file
    file.writelines(lines)

    # Truncate the remaining content in the file after the new content to ensure we're not editing more lines
    file.truncate()
    

### CONFIGURE AND COMPILE QUANTUM ESPRESSO ###

# Path to main QE directory where the commands must be executed
qe_directory = "/home/dft/Downloads/qe-7.3"

# Commands to run
configure_command = "./configure -enable-parallel" # do ./configure and link QE with libxc as specified in QE's user's guide
make_command = "make all"

# Execute the configure command in the QE main directory
try:
    subprocess.run(configure_command, shell=True, cwd=qe_directory, check=True)
    print("Configure command executed successfully.")

    # If configure succeeds, edit make.inc file
    try:
        modify_cmake_dflags(make_file)
        modify_cmake_iflags(make_file)
        modify_cmake_ldlibs(make_file)
        print("Make.inc file was edited succesfully")
        
        # Once the make.inc was succesfully set, excecute the make command
        try:
            subprocess.run(make_command, shell=True, cwd=qe_directory, check=True)
            print("make all command executed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error executing make command:", e)
        
    except subprocess.CalledProcessError as e:
        print("Error editing make.inc file:", e):
        
except subprocess.CalledProcessError as e:
    print("Error executing configure command:", e)
