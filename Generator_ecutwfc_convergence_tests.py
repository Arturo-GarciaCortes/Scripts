import numpy as np

# Automatic generation of input files for convergence test calculations (ecutwfc)

# Set this part before each use.
input_file_template = 'HAp-PBEsol' # Name of the input file template in format: 'Material_Structureorphase_Functional&Calculationtype-ecuttest-'

# Set cutt-off energies range (all must be an int number) before use this script
init_ecut = 20
final_ecut = 80
step = 10

# Functions to use

def ecut_range(initial_ecut, final_ecut, step):
    ecuts_range = np.arange(initial_ecut, final_ecut+step, step)
    ecuts_range_list = ecuts_range.tolist()
    ecuts_range_string = []
    
    for ecut in ecuts_range_list:
        ecut_s = str(ecut)
        ecuts_range_string.append(ecut_s)
        
    return ecuts_range_string

def copy_input_template(input_template, ecuts_range_string):
    input_files_names = []
    
    for ecut in ecuts_range_string:
        input_name = input_template + '-' + ecut + '.in'
        input_files_names.append(input_name)
    
    for input_file in input_files_names: 
        with open(input_template, 'r') as template:
            with open(input_file, 'w') as destination:
                for line in template:
                    destination.write(line)
                    
    return input_files_names
                
def set_input_files(input_files, ecuts_string):
    for input_file, ecut_value in zip(input_files, ecuts_string):
        with open(input_file, 'r+') as file:
            # Read all lines into a list
            lines = file.readlines()
    
            for i, line in enumerate(lines):
                # Check if the ecutwfc is in the line
                if 'ecutwfc' in line:
                    index = line.find('ecutwfc') 
                    lines[i] = line[:index + 18] + ecut_value + '\n'
                
                # UNCOMMENT THIS PART OF CODE IF THE QE INPUT FILE IS CONSIDERING THE VARIABLE ECUTHRO
                elif 'ecutrho' in line:
                    ecut_int = int(ecut_value)
                    ecuthro_int = ecut_int * 8 #SET THIS LINE ACCORDINGLY FOR THE NUMBER OF TIMES YOU WANT TO MULTIPLY THE ECUTWFC TO BE THE ECUTHRO VALUE
                    ecuthro = str(ecuthro_int)
                    index = line.find('ecutrho')
                    lines[i] = line[:index + 18] + ecuthro + '\n'                 
                
            # Move the file pointer to the beginning of the file
            file.seek(0)

            # Write the modified lines back to the file
            file.writelines(lines)

            # Truncate the remaining content (if any) in the file after the new content
            file.truncate()

#MAIN PROGRAM
ecuts_range = ecut_range(init_ecut, final_ecut, step)
input_files_templates = copy_input_template(input_file_template, ecuts_range)
set_input_files(input_files_templates, ecuts_range)
