import re
from pathlib import Path
from typing import List, Tuple
import matplotlib.pyplot as plt

# Conversion factor from Rydberg to eV
RY_TO_EV = 13.60569301

def parse_output_file(file_path: Path) -> Tuple[float, float]:
    """
    Parses a Quantum Espresso output file to extract the charge density cutoff
    and the final total energy.

    Args:
        file_path: The path to the .out file.

    Returns:
        A tuple containing the charge density cutoff (in Ry) and the
        total energy (in eV). Returns (None, None) if values are not found.
    """
    ecutrho = None
    total_energy = None

    # Regular expressions for robust parsing
    ecutrho_re = re.compile(r"charge density cutoff\s+=\s+([\d.]+)\s+Ry")
    energy_re = re.compile(r"!\s+total energy\s+=\s+([-\d.]+)\s+Ry")

    with file_path.open('r') as f:
        for line in f:
            ecut_match = ecutrho_re.search(line)
            if ecut_match:
                ecutrho = float(ecut_match.group(1))

            energy_match = energy_re.search(line)
            if energy_match:
                # The final energy is the last one found in the file
                total_energy = float(energy_match.group(1))

    if total_energy is not None:
        total_energy *= RY_TO_EV  # Convert energy to eV

    return ecutrho, total_energy

def plot_convergence(data: List[Tuple[float, float]]):
    """
    Plots the total energy as a function of the charge density cutoff.

    Args:
        data: A list of tuples, where each tuple contains the
              (ecutrho, total_energy).
    """
    # Sort data based on the charge density cutoff
    data.sort()

    # Unzip the sorted data for plotting
    ecutrho_values = [item[0] for item in data]
    total_energies = [item[1] for item in data]

    plt.figure(figsize=(10, 6))
    plt.plot(ecutrho_values, total_energies, marker='o', linestyle='-')
    plt.xlabel('Charge Density Cutoff (Ry)')
    plt.ylabel('Total Energy (eV)')
    plt.title('Ecutrho Convergence Test')
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to find .out files, extract data, and plot the results.
    """
    current_directory = Path('.')
    output_files = list(current_directory.glob('*.out'))

    if not output_files:
        print("No .out files found in the current directory.")
        return

    print(f"Found {len(output_files)} output files to process.")

    convergence_data = []
    for file in output_files:
        ecutrho, energy = parse_output_file(file)
        if ecutrho is not None and energy is not None:
            convergence_data.append((ecutrho, energy))
            print(f"  - {file.name}: Ecutrho = {ecutrho} Ry, Energy = {energy:.4f} eV")
        else:
            print(f"  - {file.name}: Could not extract required data.")

    if convergence_data:
        plot_convergence(convergence_data)
    else:
        print("No data was successfully extracted. Cannot generate plot.")

if __name__ == "__main__":
    main()