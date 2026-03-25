# This python script serves to read a Quantum ESPRESSO (QE) input file for a vc-relax or relax calculation and fix the atoms located between a specified range along the z-direction

import os

qe_input_path = 'pw_template.in' # Specify the path to find the QE input file

# Define range along z-direction
lower_limit = 8.0
upper_limit = 48.54

# Defining required functions

# Function for extracting all the atoms from the original input_file
def extract_ATOMICPOSITIONS(qe_file):
    atomic_positions = []
    is_capturing = False
    
    #print('ATOMIC_POSITIONS crystal')
    
    with open(qe_file, 'r') as file:
        for line in file:
            if 'ATOMIC_POSITIONS angstrom' in line:
                is_capturing = True
            elif is_capturing:
                atomic_positions.append(line)

    return atomic_positions


# Function for extracting the z-coordinate of all atoms
def get_z_coordinates(atoms):

    atoms_lists = [None] * len(atoms)
    z_coordinates = []
    
    for i,atom in enumerate(atoms):
        # Extract the string and split by spaces
        atoms_lists[i] = atom.split()
        
    # Removing empy sublists generated due to blank spaces at the end of the input file
    atoms_lists = [sublist for sublist in atoms_lists if sublist]

    # Get only the last item of each sublist, which corresponds to the z-coordinate of the atom
    for list in atoms_lists:
        z_coord = list[-1]
        z_coordinates.append(z_coord)
    
    return z_coordinates


# Funtion to identify and select the atoms that will be fixed (those who are between the range z_i to z_f)
def selecting_atoms(z_coordinates, z_i, z_f):

    atoms_in_range_indexes = []
    
    # Convert the items in the z_coordinates list from string to float
    for i in range(len(z_coordinates)):
        z_coordinates[i] = float(z_coordinates[i])

    # Identify the atoms that are in the specified range (z_i - z_f)
    for i, z_coord in enumerate(z_coordinates):
        if z_i < z_coord < z_f:
            atom_index = i
            atoms_in_range_indexes.append(atom_index)
    
    return atoms_in_range_indexes


# Funtion to fix the selected atoms
def fix_atoms(atoms_to_fix_indexes, original_atomic_positions):
    new_positions = list(original_atomic_positions)

    for index in atoms_to_fix_indexes:
        line = original_atomic_positions[index]
        new_positions[index] = line[:-2] + ' 0 0 0 \n'

    return new_positions

# Function to generate a new file which will contain the structure with fixed atoms
def copy_input_template(input_template):
    input_file = input_template[:-3] + '_fixed_atoms.in'
    
    with open(input_template, 'r') as template:
        with open(input_file, 'w') as destination:
            for line in template:
                destination.write(line)
                    
    return input_file

# Funtion to set the new QE input file with fixed atoms by replacing the original ATOMIC_POSITIONS card with the lines in list new_positions
def set_qe_input_file(qe_file, new_atomic_positions):
    with open(qe_file, 'r') as file:
        lines = file.readlines()

    with open(qe_file + "_temp", 'w') as temp_file:
            is_editing = False
            for line in lines:
                if 'ATOMIC_POSITIONS' in line:
                    is_editing = True
                    temp_file.write(line)
                elif is_editing:
                    temp_file.write(new_atomic_positions.pop(0))  # Write one line from new_atomic_positions list
                else:
                    temp_file.write(line)

    # Replace the original file with the temporary file
    os.replace(qe_file + "_temp", qe_file)

# MAIN PROGRAM #

# Reading and storing the ATOMIC_POSITIONS card of the original QE file
atomic_pos = extract_ATOMICPOSITIONS(qe_input_path)

# Exctracting the z-coordinates of all atoms in the structure
z_coordinates = get_z_coordinates(atomic_pos)

# Identify atoms inside the specified range
atoms_inside_range_index = selecting_atoms(z_coordinates, lower_limit, upper_limit)

# Fixing atoms inside the range by adding '0 0 0' at the end of the line
new_atomic_pos = fix_atoms(atoms_inside_range_index, atomic_pos)

# Modifying the QE input file by adding the new atomic positions with fixed atoms
new_qe_file_path = copy_input_template(qe_input_path)
set_qe_input_file(new_qe_file_path, new_atomic_pos)
