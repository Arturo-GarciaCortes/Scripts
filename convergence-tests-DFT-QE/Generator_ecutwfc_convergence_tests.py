import numpy as np
from pathlib import Path
import sys

# Automatic generation of input files for convergence test calculations (ecutwfc)

def generate_ecutwfc_convergence_files(
    template_file: str,
    initial_ecut: int,
    final_ecut: int,
    step: int,
    ecutrho_multiplier: int = 8,
) -> None:
    """
    Generates input files for ecutwfc convergence tests.

    Args:
        template_file: The name of the input file template.
        initial_ecut: The initial ecut value.
        final_ecut: The final ecut value.
        step: The step size for the ecut range.
        ecutrho_multiplier: The multiplier for ecutrho.
    """

    template_path = Path(template_file)
    if not template_path.is_file():
        print(f"Error: Template file not found at '{template_path}'")
        sys.exit(1)

    template_content = template_path.read_text()
    ecut_values = np.arange(initial_ecut, final_ecut + step, step)

    for ecut_value in ecut_values:
        new_filename = f"{template_path.stem}-{ecut_value}.in"
        new_content = template_content.replace("ecutwfc", f"ecutwfc            = {ecut_value}")

        if "ecutrho" in new_content:
            ecutrho_value = ecut_value * ecutrho_multiplier
            new_content = new_content.replace("ecutrho", f"ecutrho = {ecutrho_value}")

        Path(new_filename).write_text(new_content)
        print(f"Generated file: {new_filename}")


if __name__ == "__main__":
    # Set this part before each use.
    input_file_template = "HAp-PBEsol"  # Name of the input file template in format: 'Material_Structureorphase_Functional&Calculationtype-ecuttest-'
    init_ecut = 20
    final_ecut = 80
    step = 10

    generate_ecutwfc_convergence_files(
        input_file_template, init_ecut, final_ecut, step
    )
