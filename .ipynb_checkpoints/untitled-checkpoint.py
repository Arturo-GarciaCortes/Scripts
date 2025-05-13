### PYTHON SCRIPT TO GET THE BAND GAP VALUE OF A STRUCTURE FROM THE .DAT.GNU AND QUANTUM ESPRESSO .OUT (NSCF) FILES ###
# These files are obtained from a 'bands' type calculation.

import ase
from ase import atoms
from ase.visualize import view
import pandas as pd

# Program functions

def get_energies(dat_file):
    """
    This function reads the .dat.gnu file and filters data to keep only the energy values (y-axis column)
    """
    lines = []
    energies = []
    
    # Read the file and store all lines into a list
    with open(dat_file, 'r') as file:
        for line in file:
            lines.append(line)
            
    # Get only the y-values (energies) of the data 
    for line in lines:
        energy = line[12:20]
        energies.append(energy)
    
    # Using filter() to remove empty items in energy list
    energies = list(filter(None, energies))

    # Convert the items in the list (energies) from string to float
    for i in range(len(energies)):
        energies[i] = float(energies[i])

    return energies

def get_fermi_energy(nscf_out_file):
    """
    This function reads the QE .out file from the nscf calculation to find the line which stores the Fermi energy to convert
    it to float and return that value.
    """
    ecutwfc = []
    with open(nscf_out_file, 'r') as file:
        fermi_energy_line = None  # Initialize energy_line before the loop
        for line in file:
            if 'the Fermi energy is' in line:
                fermi_energy_line = line
                break
                
    if fermi_energy_line:
        index = fermi_energy_line.find('the Fermi energy is')
        fermi_energy = float(fermi_energy_line[index + 22: index + 31])

    return fermi_energy

def get_max_VB_and_min_CB(energies, fermi_energy):
    """
    This function (1) compares the values stored in the energies list with the Fermi energy to obtain the energy values that
    form the valence band (when the energy is lower than the Fermi energy) as well as those that form the conduction band 
    (when energy is higher than the Fermi energy) in order to (2) get the higher energy value that is lower than the Fermi
    energy (max of valence band) and the lower energy value that is higher than the Fermi energy (min of the conduction band).
    """
    valence_band_energies = []
    conduction_band_energies = []

    # Valence band
    for energy in energies:
        if energy < fermi_energy:
            valence_band_energies.append(energy)
    
    # Conduction band
    for energy in energies:
        if energy > fermi_energy:
            conduction_band_energies.append(energy)

    # Getting the max of the valence band
    max_VB = max(valence_band_energies)

    # Getting the min of the conduction band
    min_CB = min(conduction_band_energies)

    return max_VB, min_CB

def calculate_band_gap(max_VB, min_CB):
    """
    This function computes the band gap of the material by taking the difference between the maximum of the valence band
    and the minimum of the conduction band
    """
    band_gap = abs(min_CB - max_VB)
    
    return band_gap

################################# MAIN PROGRAM #############################################

# Getting the energies from the dat.gnu file
energies = get_energies(dat_gnu_file)

# Retrieving the Fermi energy from the QE .out file from a nscf calculation
Fermy_e = get_fermi_energy(nscf_out_file)

# Separating the energies correspoding to the valence band from those that form the conduction band and obtain their max and min, respectively
max_valence_band, min_conduction_band = get_max_VB_and_min_CB(energies, Fermy_e)

# Calculating band gap
band_gap = calculate_band_gap(max_valence_band, min_conduction_band)

print('The band gap of this structure is: ', band_gap, 'eV')