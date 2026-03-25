from ase import Atoms
from ase.io.espresso import read_espresso_out
from ase.io import cif, xsf

# Obtaining the relaxed structure and information from a Quantum ESPRESSO output file (relax or vc-relax calculation)
qe_output_file = './qe.35781554.out' # Specify this at every usage
with open(qe_output_file, 'r') as file:
    for atoms in read_espresso_out(file, index=slice(-1,None)): # Storing only the last structure coordinates and information
        relaxed_structure = atoms

# Open a file to write the CIF structure
with open('optimized_structure.cif', 'w') as fd:
    # Write the structure to the CIF file
    cif.write_cif('optimized_structure.cif', relaxed_structure, cif_format=None, wrap=True, labels=None, loop_keys=None)

# Open a file to write the XSF structure
with open('optimized_structure.xsf', 'w') as fd:
    # Write the structure to the XSF file
    xsf.write_xsf('optimized_structure.xsf', [relaxed_structure])

