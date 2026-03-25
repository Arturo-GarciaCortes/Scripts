"""
Python script to get the strucure within a Quantum ESPRESSO input file (pw.x) as both .xsf and .cif files. 
-A
"""

from ase.io import read
from ase.io import cif, xsf

# Here the user inputs the file path of the pw.x input file
input_file = input("Enter the path to the Quantum Espresso input file: ")

# Read the structure in the file
atoms = read(input_file)

# Open a file to write the XSF structure
with open('initial_structure.xsf', 'w') as fd:
    # Write the structure to the XSF file
    xsf.write_xsf('initial_structure.xsf', [atoms])

# Open a file to write the CIF structure
with open('initial_structure.cif', 'w') as fd:
    # Write the structure to the CIF file
    cif.write_cif('initial_structure.cif', atoms, cif_format=None, wrap=True, labels=None, loop_keys=None)