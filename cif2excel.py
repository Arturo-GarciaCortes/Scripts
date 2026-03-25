import pandas as pd 
import numpy as np
import ase
from ase import Atoms
from ase.io.espresso import read_espresso_out
from ase.io import read,write,cif
from ase.visualize import view
from ase.visualize import ngl

# Here the user enters the path to the .CIF file of the structure you want to extract the atomic coordinates from
cif_file = input("Enter the path to the .CIF of the structure you want to extract the atomic coordinates from: ")
structure_name = input("Enter the name for the structure that will appear in the excel file: ")


# Reading the .cif file using the ASE software
structure = ase.io.cif.read_cif(cif_file)

# Get the chemical symbols of all elements present in the structure
chemical_symbols = structure.get_chemical_symbols()

# Get the atomic coordinates (x,y,x) of all atoms in the structure
positions = structure.get_positions()

# Splitting the atomic coordinates into three different lists
coordinates_x = []
coordinates_y = []
coordinates_z = []
for i in range(len(positions)):
    coordinates_x.append(positions[i][0])
    coordinates_y.append(positions[i][1])
    coordinates_z.append(positions[i][2])

# Get the cell parameters 
cell_parameters = structure.get_cell_lengths_and_angles()
lattice_param_a = [cell_parameters[0]]
lattice_param_b = [cell_parameters[1]]
lattice_param_c = [cell_parameters[2]]

# Creating dataframe for atomic coordinates from lists
data_atomic_coordinates = {'Atom': chemical_symbols, 'x (Å)': coordinates_x, 'y (Å)': coordinates_y, 'z (Å)': coordinates_z}
df_atomic_coordinates = pd.DataFrame(data_atomic_coordinates)

# Creating dataframe for cell parameters from lists
data_cell_parameters = {None: 'Cell parameters', 'a (Å)': lattice_param_a, 'b (Å)': lattice_param_b, 'c (Å)': lattice_param_c}
df_cell_parameters = pd.DataFrame(data_cell_parameters)

# Exporting dataframes to a single sheet in an Excel file
output_filename = f"{structure_name}_data.xlsx"
with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
    df_cell_parameters.to_excel(writer, sheet_name='Data', index=False)
    df_atomic_coordinates.to_excel(writer, sheet_name='Data', startrow=len(df_cell_parameters) + 2, index=False)

print(f"Data successfully exported to {output_filename}")
