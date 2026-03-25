# EXCTRATING AND PLOTTING THE ENERGIES OF THE K-POINTS CONVERGENCE TESTS (WITHOUTH SHIFTS IN THE GRID)

import os
import matplotlib.pyplot as plt

# Defining the extract final total energy function and the name of the file where the energy comes from
def extract_energies(output_files_real_path):
    filenames = []
    Energies = []
    for path in output_files_real_path:
        with open(path, 'r') as file:
            energy_line = None  # Initialize energy_line before the loop
            for line in file:
                if '!    total energy' in line:
                    energy_line = line
                    break
        if energy_line:
            index = energy_line.find('total energy')
            total_energy_s = energy_line[index + 29: index + 44]
            total_energy = float(total_energy_s)
            total_energy = total_energy * 13.60569301 # Convert Ry to eV 
            Energies.append(total_energy)
            filename = os.path.basename(path)  # Extract filename from path using os.path.basename
            filenames.append(filename)
            print('For file:', filename)
            print('Final total energy =', total_energy, 'eV \n')
        else:
            print('No total energy found in', path)

    return Energies, filenames

# Function for depuring the filename and keep only the k-points grid
def extract_grids(filenames):
    grids = []
    for file in filenames:
        index = file.find('-')
        if index != -1:
            grid_1 = file[index+1: -4]  # Extracts substring from the first '-' to the 4th-end character (to avoid to have '.out')
            grid = int(grid_1) # Converts the chain of characters that contains the grid to an int number to be able to sort it in the next function
            grids.append(grid)
        else:
            print('Make sure to rename all the .out files with the following format: \n')  # Handle the case where '-' is not found
            print('DesiredPrefix-k1k2k3')

    return grids

def plot_energy_vs_kpoints(total_energies, k_grids):
    X = k_grids
    Y = total_energies 

    # Pair the lists together
    paired = list(zip(X, Y))

    # Sort pairs based on the values in the first list (X) in ascending order
    sorted_pairs = sorted(paired, key=lambda pair: pair[0])

    # Unzip the sorted pairs
    sorted_X, sorted_Y = zip(*sorted_pairs)

    # Convert back to lists
    sorted_X = list(sorted_X)
    sorted_Y = list(sorted_Y)
    
    for i in range(len(sorted_X)):   # Convert the int numbers (k-points grids) to strings again in order to plot them accordingly
        sorted_X[i] = str(sorted_X[i])

    plt.plot(sorted_X, sorted_Y, marker='o', linestyle='-', label='k-point grid')
    plt.xlabel('k-point grid')
    plt.ylabel('Energy (eV)')
    plt.legend(loc='lower right')
    plt.title('Convergence test (k-point grid)')
    plt.savefig('k-points_convergence_tests.png', dpi=400)  # Change the filename and dpi as needed to save it

    plt.show()

            
# MAIN PROGRAM
output_files_real_path = []

# Get the list of files in the current directory
files_in_directory = os.listdir()

# Filter out only the .out files
output_files_real_path = [file for file in files_in_directory if file.endswith('.out')]

# Calling the function for extracting the total energies of each file in file_real_path
Energies, filenames = extract_energies(output_files_real_path)
k_grids = extract_grids(filenames)
plot_energy_vs_kpoints(Energies, k_grids)
