import os
import matplotlib.pyplot as plt

# Defining the extract final total energy function.
def extract_energies(output_files_real_path):
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
            print('For file:', filename)
            print('Final total energy =', total_energy, 'eV \n')
        else:
            print('No total energy found in', path)

    return Energies 

def extract_ecutwfc(output_files_real_path):
    ecutwfc = []
    for path in output_files_real_path:
        with open(path, 'r') as file:
            energy_line = None  # Initialize energy_line before the loop
            for line in file:
                if 'kinetic-energy cutoff' in line:
                    energy_line = line
                    break
        if energy_line:
            index = energy_line.find('kinetic-energy cutoff')
            total_energy_s = energy_line[index + 33: index + 39]
            total_energy = float(total_energy_s)
            ecutwfc.append(total_energy)

    return ecutwfc


def plot_energy_vs_ecut(total_energies, ecutwfc):
    X = ecutwfc
    Y = total_energies
    
    # Pair the lists together
    paired_lists = list(zip(X, Y))

    # Sort the paired lists based on the first list (List1)
    paired_lists_sorted = sorted(paired_lists)

    # Unzip the sorted pairs back into two lists
    sorted_ecutwfc, sorted_total_energies = zip(*paired_lists_sorted)

    # Convert the zipped tuples back to lists
    sorted_X = list(sorted_ecutwfc)
    sorted_Y = list(sorted_total_energies)

    plt.plot(sorted_X, sorted_Y, marker='o', linestyle='-')
    plt.xlabel('E cut-off (Ry)')
    plt.ylabel('Energy (eV)')
    plt.title('E cutt-off convergence test')
    plt.show()

            
# MAIN PROGRAM
output_files_real_path = []

# Get the list of files in the current directory
files_in_directory = os.listdir()

# Filter out only the .out files
output_files_real_path = [file for file in files_in_directory if file.endswith('.out')]

# Calling the function for extracting the total energies of each file in file_real_path
ecutwfc_values = extract_ecutwfc(output_files_real_path)
Energies = extract_energies(output_files_real_path)
plot_energy_vs_ecut(Energies, ecutwfc_values)
