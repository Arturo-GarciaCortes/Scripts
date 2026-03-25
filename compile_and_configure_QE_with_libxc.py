######CODE TO CONFIGURE AND COMPILE QUANTUM ESPRESSO ENABLING PARALLEL EXCECUTION AND LIBXC#######

#!!!! This script needs to be run into the main directory of QE !!!!!

#Import libraries that allows us to navigate and run commands in terminal
import subprocess
import os

# PLEASE SPECIFY THE FOLLOWING DIRECTORIES
qe_directory = '/path/to/qe/main/directory' #Path to Quantum Espresso main directory
libxc_path = '/path/to/libxc' #Path to libxc directory

#Name of the make file to be edited (it tends to be make.inc)
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
            if 'DFLAGS         =  -D' in line:
                # Increment the occurrence count
                dflags_occurrence += 1

                # When it is the first occurrence:
                if dflags_occurrence == 1:

                    # Building the str chain that adds -D__LIBXC to DFLAGS as requested by QE
                    body_chain = line
                    body_chain = body_chain.strip() # Strip any trailing newline characters to keep everything in the same line
                    str_chain = body_chain + ' -D__LIBXC\n'

                    # Replace the line to add -D__LIBXC to DFLAGS as requested by QE
                    lines[i] = str_chain

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
            if 'IFLAGS         = -I' in line:
                # Increment the occurrence count
                iflags_occurrence += 1

                # When it is the first occurrence:
                if iflags_occurrence == 1:

                    # Building the str chain that adds -I/libxc_path/include/ to IFLAGS as requested by QE
                    body_chain = line
                    body_chain = body_chain.strip() # Strip any trailing newline characters to keep everything in the same line
                    str_chain = body_chain + ' -I' + libxc_path + '/include/\n'

                    # Replace the line to add -I/libxc_path for using libxc
                    lines[i] = str_chain

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

                # When it is the first occurrence:
                if ldlibs_occurrence == 1:
                    
                    # Building the str chain that adds -L/path/to/libxc/lib/ -lxcf03 -lxc to LD_LIBS as requested by QE
                    body_chain = line
                    body_chain = body_chain.strip() # Strip any trailing newline characters to keep everything in the same line
                    str_line = body_chain + '-L' + libxc_path + '/lib/ -lxcf03 -lxc\n' 

                    # set LD_LIBS=-L/path/to/libxc/lib/ -lxcf03 -lxc for using libxc (if If libxc release is 5.0.0 replace -lxcf03 with -lxcf90)
                    lines[i] = str_line

        # Move the file pointer to the beginning of the file
        file.seek(0)

        # Write the modified lines back to the file
        file.writelines(lines)

        # Truncate the remaining content in the file after the new content to ensure we're not editing more lines
        file.truncate()
        
    return 0

### CONFIGURE AND COMPILE QUANTUM ESPRESSO ###

# Commands to run in qe_directory
configure_command = './configure -enable-parallel' # do ./configure and enable parallel excecution also linking QE with libxc from make.inc file as specified in QE's user's guide
make_command = 'make all'

# Execute the configure command in the QE main directory
try:
    subprocess.run(configure_command, shell=True, cwd=qe_directory, check=True)
    print('Configure command executed successfully.')

    # If configure succeeds, edit make.inc file
    try:
        modify_cmake_dflags(make_file)
        modify_cmake_iflags(make_file)
        modify_cmake_ldlibs(make_file)
        print('make.inc file was edited succesfully to link QE with Libxc')
        
        # Once the make.inc was succesfully set, excecute the make command
        try:
            subprocess.run(make_command, shell=True, cwd=qe_directory, check=True)
            print('make all command executed successfully.')
        except subprocess.CalledProcessError as e:
            print('Error executing make command:', e)
        
    except subprocess.CalledProcessError as e:
        print('Error editing make.inc file:', e)
        
except subprocess.CalledProcessError as e:
    print('Error executing configure command:', e)
