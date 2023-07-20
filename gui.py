import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def manual_data_entry():
    data = []

    def add_data_point(event):
        entry = data_entry_var.get().strip()
        try:
            value = int(entry)
            if value < 0 or value > 360:
                raise ValueError("Invalid value! The data should be in azimuth degrees!")
            data.append(float(entry))
            data_entry_var.set("")  # Clear the entry for next data point
        except ValueError:
            data_entry_var.set("Invalid input! Please enter a valid numeric value.")

    def finish_data_entry(event):
        root.bind('<Return>', None)  # Unbind the Enter key
        plot_histogram_and_rose(data)

    # Clear the main application window
    for widget in root.winfo_children():
        widget.destroy()

    data_entry_var = tk.StringVar()
    data_entry_field = tk.Entry(root, textvariable=data_entry_var)
    data_entry_field.pack()
    data_entry_field.focus()  # Set focus on the data entry field

    data_entry_field.bind('<Return>', add_data_point)  # Bind Enter key to add_data_point function

    root.bind('<Escape>', finish_data_entry)  # Bind Escape key to finish_data_entry function

def csv_data_entry():
    csv_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    data = pd.read_csv(csv_path, header=None).values.flatten()
    plot_histogram_and_rose(data)

def plot_histogram_and_rose(data):
    i = 30

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(data, np.arange(0, 361, i))
    ax.set_xlim(0, 360)
    plt.xticks(np.arange(0, 361, i))

    plt.xlabel("Paleoakıntı verileri için derece aralığı", fontsize=15)
    plt.ylabel("Frekans", fontsize=15)

    bins = np.arange(0, 361, i)
    hist, _ = np.histogram(data, bins=bins)
    hist = np.array(hist)
    midpoints = bins[:-1] + np.diff(bins) / 2

    fig2 = plt.figure(figsize=(7, 7))
    ax = fig2.add_subplot(111, projection='polar')
    ax.bar(np.deg2rad(midpoints), hist, width=np.deg2rad(i), edgecolor='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.set_title('paleoakıntı verileri gül diyagramı')
    ax.set_thetagrids(np.arange(0, 360, i), labels=np.arange(0, 360, i))
    ax.set_rlabel_position(135)
    ax.set_yticks(hist)
    ax.set_yticklabels(hist)

    plt.show()

# Create the main application window
root = tk.Tk()
root.title("Data Visualization App")

# Button to manually add data
manual_button = tk.Button(root, text="Manually Add Data", command=manual_data_entry)
manual_button.pack()

# Button to add data through a CSV file
csv_button = tk.Button(root, text="Add Data from CSV", command=csv_data_entry)
csv_button.pack()

# Run the application
root.mainloop()
