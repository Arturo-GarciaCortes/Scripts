import numpy as np
from pathlib import Path
import sys

# Automatic generation of input files for convergence test calculations (degauss)

def generate_degauss_convergence_files(
    template_file: str,
    initial_degauss: float,
    final_degauss: float,
    step: float,
) -> None:
    """
    Generates input files for degauss convergence tests.

    Args:
        template_file: The name of the input file template.
        initial_degauss: The initial degauss value.
        final_degauss: The final degauss value.
        step: The step size for the degauss range.
    """

    template_path = Path(template_file)
    if not template_path.is_file():
        print(f"Error: Template file not found at '{template_path}'")
        sys.exit(1)

    template_content = template_path.read_text()
    degauss_values = [
        f"{deg:.3f}" # formatting deg values as strings with 3-decimal precision to ensure clean filenames and input values
        for deg in np.arange(initial_degauss, final_degauss + step, step)
    ]

    for degauss_value in degauss_values:
        new_filename = f"{template_path.stem}-{degauss_value}.in"
        # Replace the first occurrence of 'degauss' in the template.
        new_content = template_content.replace("degauss", f"degauss            = {degauss_value}", 1)
        Path(new_filename).write_text(new_content)
        print(f"Generated file: {new_filename}")


if __name__ == "__main__":
    # Set this part before each use.
    input_file_template = "CaB6"  # Name of the input file template
    init_degauss = 0.001
    final_degauss = 0.01
    step = 0.001

    generate_degauss_convergence_files(
        input_file_template, init_degauss, final_degauss, step
    )
