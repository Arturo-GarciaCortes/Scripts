import numpy as np

# Automatic generation of input files for convergence test calculations (degauss)

# Set this part before each use.
input_file_template = 'CaB6' # Name of the input file template

# Set cutt-off energies range (all must be an int number) before use this script
init_degauss = 0.001
final_degauss = 0.01
step = 0.001

# Functions to use

def degauss_range(initial_degauss, final_degauss, step):
    degauss_range = np.arange(initial_degauss, final_degauss+step, step)
    degauss_range_list = degauss_range.tolist()
    degauss_range_string = []
    
    for deg in degauss_range_list:
        deg_s = str(deg)
        degauss_range_string.append(deg_s)
        
    return degauss_range_string

def copy_input_template(input_template, degauss_range_string):
    input_files_names = []
    
    for deg in degauss_range_string:
        input_name = input_template + '-' + deg + '.in'
        input_files_names.append(input_name)
    
    for input_file in input_files_names: 
        with open(input_template, 'r') as template:
            with open(input_file, 'w') as destination:
                for line in template:
                    destination.write(line)
                    
    return input_files_names
                
def set_input_files(input_files, degauss_string):
    for input_file, deg_value in zip(input_files, degauss_string):
        with open(input_file, 'r+') as file:
            # Read all lines into a list
            lines = file.readlines()
    
            for i, line in enumerate(lines):
                # Check if the ecutwfc is in the line
                if 'degauss' in line:
                    index = line.find('degauss') 
                    lines[i] = line[:index + 18] + deg_value + '\n'
                
            # Move the file pointer to the beginning of the file
            file.seek(0)

            # Write the modified lines back to the file
            file.writelines(lines)

            # Truncate the remaining content (if any) in the file after the new content
            file.truncate()

#MAIN PROGRAM
degauss_range = degauss_range(init_degauss, final_degauss, step)
input_files_templates = copy_input_template(input_file_template, degauss_range)
set_input_files(input_files_templates, degauss_range)
