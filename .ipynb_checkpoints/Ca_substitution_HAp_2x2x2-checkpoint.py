import pandas as pd
import numpy as np
import os

### FUNCTIONS SECTION ###

# Function for extracting all the atoms from the original input_file
def extract_ATOMICPOSITIONS(in_file):
    all_atoms = []
    is_capturing = False
    
    #print('ATOMIC_POSITIONS crystal')
    
    with open(in_file, 'r') as file:
        for line in file:
            if 'ATOMIC_POSITIONS crystal' in line:
                is_capturing = True
            elif 'K_POINTS automatic' in line:
                is_capturing = False
            elif is_capturing:
                all_atoms.append(line)
    
    return all_atoms

#Functions for randomly selecting which Ca1 and/or Ca2 ions will be modified.
def generate_index_Ca1(substituted_Ca1):
    # Random generation of 'x' number of indexes for the atoms that will be substitued
    already_substitued = []

    while len(already_substitued) < substituted_Ca1:
        random_index_Ca1 = np.random.randint(32)
        if random_index_Ca1 not in already_substitued:
            already_substitued.append(random_index_Ca1)

    return already_substitued

def generate_index_Ca2(substituted_Ca2):
    # Random generation of 'x' number of indexes that will be substitued
    already_substitued = []

    while len(already_substitued) < substituted_Ca2:
        random_index_Ca2 = np.random.randint(48)
        if random_index_Ca2 not in already_substitued:
            already_substitued.append(random_index_Ca2)

    return already_substitued


# Function for changing the selected Ca1 or Ca2 ions for the dopant
def susbtitution_Ca1(dopant, indexes, Ca1_list):
    # Random substitution of 'x' number of Ca1 sites
    new_Ca1 = list(Ca1_list)
    
    for index in indexes:
        line = new_Ca1[index]
        coordinates = line[8:]
        modified_line = '' + dopant + '      ' + coordinates #This is considering that dopant has two letters
        new_Ca1[index] = modified_line
        
    return new_Ca1

def susbtitution_Ca2(dopant, indexes, Ca2_list):
    # Random substitution of 'x' number of Ca2 sites
    new_Ca2 = list(Ca2_list)
    
    for index in indexes:
        line = new_Ca2[index]
        coordinates = line[8:]
        modified_line = '' + dopant + '      ' + coordinates #This is considering that dopant has two letters
        new_Ca2[index] = modified_line
        
    return new_Ca2

# Function to generate the new files which will contain the modified (substituted) models
def copy_input_template(input_template, number_structures, s_Ca1, s_Ca2):
    input_files_names = []
    s_Ca1 = str(s_Ca1)
    s_Ca2 = str(s_Ca2)
    
    for i in range(number_structures):
        input_name = input_template + '_' + s_Ca1 + '-Ca1' + '_' + s_Ca2 + '-Ca2_' + str(i+1) + '.in'
        input_files_names.append(input_name)
    
    for input_file in input_files_names: 
        with open(input_template, 'r') as template:
            with open(input_file, 'w') as destination:
                for line in template:
                    destination.write(line)
                    
    return input_files_names

# Mother function which incorporates all other functions in order to carry out the random Ca ion substitution

def change_ATOMICPOSITIONS(input_files, substituted_Ca2, substituted_Ca1, dopant, atoms, Ca_1, Ca_2):
    modified_atoms_lists = []
    
    for in_file in input_files:
        # Randomly generate indexes for the Ca1 and Ca2 sites to be substitued
        Ca1_sub_indexes = generate_index_Ca1(substituted_Ca1)
        Ca2_sub_indexes = generate_index_Ca2(substituted_Ca2)
        
        # Modify (substitute) the randomly selected Ca1 and Ca2 ions
        modified_Ca1_list = susbtitution_Ca1(dopant, Ca1_sub_indexes, Ca_1)
        modified_Ca2_list = susbtitution_Ca2(dopant, Ca2_sub_indexes, Ca_2)

        # Put the modified Ca2 and Ca1 lists together
        modified_Ca_atoms_list = modified_Ca1_list + modified_Ca2_list

        # edit the original list 'atoms' to include the modifications made to Ca atoms
        POH_atoms = atoms[80:352]
        modified_atoms_list = modified_Ca_atoms_list + POH_atoms
        modified_atoms_lists.append(modified_atoms_list)
        
    return modified_atoms_lists

# Write the modified atomic information to the previously created input files
def set_new_input_files(input_files, new_atomic_positions):
    for i, in_file in enumerate(input_files):
        new_atoms = new_atomic_positions[i]
        
        # Open the input file and create a temporary file to write the modifications
        with open(in_file, 'r') as file:
            lines = file.readlines()

        with open(in_file + "_temp", 'w') as temp_file:
            is_editing = False
            for line in lines:
                if 'ATOMIC_POSITIONS' in line:
                    is_editing = True
                    temp_file.write(line)
                elif 'K_POINTS' in line:
                    is_editing = False
                    temp_file.write(line)
                elif is_editing:
                    temp_file.write(new_atoms.pop(0))  # Write one line from new_atoms list
                else:
                    temp_file.write(line)

        # Replace the original file with the temporary file
        os.replace(in_file + "_temp", in_file)

##MAIN CODE###

# Set how many Ca1 and/or Ca2 ions you would like to change and specify the dopant
dopant = 'Eu'
substituted_Ca1 = 3
substituted_Ca2 = 0
n_models = 5 # How many different random models of the same Ca1/Ca2 distribution you want to create

# Set input file that contains the atomic coordinates you want to edit (it has to be in the same directory)

input_file = 'Eu-HAp_supercell_us'

# Extract all the atomic positions section of the input file

atoms = extract_ATOMICPOSITIONS(input_file)

# Divide the Ca atoms into Ca1 and Ca2 types.

Ca_atoms = atoms[0:80] # extract all the Ca atoms of the atomic positions section
Ca_1 = Ca_atoms[48:80] # Ca atoms surrounded by nine oxygen ions
Ca_2 = Ca_atoms[0:48] # Ca atoms surrounded by six oxygen ions

# Create 'n_models' number of input files for the different structures, specifying how many Ca1 and Ca2 atoms have been substitued
models_input_files = copy_input_template(input_file, n_models, substituted_Ca1, substituted_Ca2)

# Do random substitution for a set number of Ca1 and Ca2 ion sites
new_atoms_lists = change_ATOMICPOSITIONS(models_input_files, substituted_Ca2, substituted_Ca1, dopant, atoms, Ca_1, Ca_2)

# Adjust the new input files with the modified atomic information --> Ca ion substitution
set_new_input_files(models_input_files, new_atoms_lists)
