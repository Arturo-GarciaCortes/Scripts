####### CODE TO PLOT ELECTRON CHARGE DENSITY IN 1D #########

import pandas as pd
import matplotlib.pyplot as plt

txt_file = 'initial_slab.txt' # File generated using pp.x program which contains the electron charge density (plot_num=0; iflag=1; output_format=0). 
# For more information about the plot see: https://www.quantum-espresso.org/Doc/INPUT_PP.html#idm108

# Read the .txt file which contains the electron charge density
df = pd.read_csv(txt_file, sep='\s+', header=None)

# Rename the column headers
df.columns = ['1D-coordinate (alat)', 'rho']

# Recover the atomic coordinates (x,y,z dimension) in alat units into a list 
coordinate = df['1D-coordinate (alat)']
# Recover the electron charge density
rho = df['rho']

## Making the plot ##

# Assigning values to x and y axis
x_axis = coordinate
y_axis = rho

plt.plot(x_axis, y_axis, marker='', linestyle='-', color='green')
plt.xlim(0, 19) # Adjust these values accordingly
plt.xlabel('1D-coordinate (alat)')
plt.ylabel('$rho$')
plt.title('1D plot of electron charge density')
#plt.legend()  # Show legend with labels
plt.savefig('electron_charge_density-1D.png', dpi=400)  # Change the filename and dpi as needed
plt.show()