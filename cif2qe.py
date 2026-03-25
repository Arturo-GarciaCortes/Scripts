## Convert a .cif file to a Quantum ESPRESSO input file ##

import ase
from ase.build import bulk
from ase.io import read,write,cif,espresso
from ase.io.espresso import write_espresso_in
from ase import Atoms

cif_file = './last_structure.cif' # Specify the path and name of the .cif file that contains the structure
structure = ase.io.cif.read_cif(cif_file)

# Set pseudopotentials data for generating the QE input file (real data)
pseudopotentials = {'Ca': 'Ca_ONCV_PBE-1.2.upf', 'B': 'B_ONCV_PBE-1.2.upf', 'Li': 'Li_ONCV_PBE-1.2.upf'}

# Set input data for the QE input file
input_data = {
    'calculation': 'scf',
    'prefix': 'Li-CaB6_1x1_calcium_terminated_on-top',
    'outdir': './',
    'pseudo_dir': './',
    'restart_mode': 'from_scratch',
    'tprnfor': True,
    'ecutwfc': 80,
    'occupations': 'smearing',
    'degauss': 0.005,
    'smearing': 'marzari-vanderbilt',
    'conv_thr': 1e-6,
    'mixing_beta': 0.7,
}  # This flat dictionary will be converted to a nested dictionary where, for example, "calculation" will be put into the "control" section

## Write the QE input file ##
qe_path_name = './Li-CaB6_1x1_calciumterm_ontop_sp-18-steps.in' # Specify the path and name of the quantum espresso input file
write(qe_path_name, structure, input_data=input_data, pseudopotentials=pseudopotentials, format='espresso-in')

