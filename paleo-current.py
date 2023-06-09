import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

print("select operation")
print("1. manually add data")
print("1. add data through CSV path")

while True:
    #taking input
    choice = input("Enter choice(1/2): ")

    #check if choice is one of the two options
    if choice in ('1'):
        # Manually add data
        data = []
        print("Enter data (0-360), type 'ok' to finish:")
        while True:
            entry = input("Enter data point: ")

            if entry == 'ok':
                break
            if entry == '':
                continue

            value = int(entry)
            if value < 0 or value > 360:
                print("Invalid value! the data should be in azimuth degrees!")
            else:
                data.append(float(entry))

        break

    if choice in ('2'):
    # reading the CSV
        csv_path = input("Enter the path for the CSV file: ")
        data = pd.read_csv(csv_path, header=None).values.flatten()
        break

    else:
        print("Invalid choice")
        print("1. manually add data")
        print("1. add data through CSV path")

# Extract the degree values given in azimuth
#a = data.values.flatten()

a = np.array(data)

#the degree intervals (30 and 45 degrees are mostly used in paleocurrent diagrams)
i = 30

fig, ax = plt.subplots(figsize=(7,5))
ax.hist(a, np.arange(0, 361, i))
ax.set_xlim(0, 360)
plt.xticks(np.arange(0, 361, i))

plt.xlabel("Paleoakıntı verileri için derece aralığı", fontsize = 15)
plt.ylabel("Frekans",fontsize = 15)

#buradan sonrası rose diagram için

# the flow direction bins
bins = np.arange(0, 361, i)

# Computing the FREQUENCY! of flow directions given in AZIMUTH! for each bin
hist, _ = np.histogram(a, bins=bins)

# Using original frequency values
hist = np.array(hist)

# Computing the midpoints of each bin in order to put them in between the frequency intervals given in azimuth degrees
midpoints = bins[:-1] + np.diff(bins) / 2

# Create a polar plot
fig2 = plt.figure(figsize=(7, 7))
ax = fig2.add_subplot(111, projection='polar')

# plotting the rose diagram
ax.bar(np.deg2rad(midpoints), hist, width=np.deg2rad(i), edgecolor='white')

# Setting the direction of the plot to clockwise (because of azimuth)
ax.set_theta_direction(-1)

# Setting the position of the 0 degree to the north (again, azimuth)
ax.set_theta_zero_location('N')

# Setting the title and legend
ax.set_title('paleoakıntı verileri gül diyagramı')

#setting the angular tick labels
ax.set_thetagrids(np.arange(0, 360, i), labels=np.arange(0, 360, i))

# Set the radial tick labels for the frequency scale
ax.set_rlabel_position(135)
ax.set_yticks(hist)
ax.set_yticklabels(hist)

# Show the plot :P
plt.show()

