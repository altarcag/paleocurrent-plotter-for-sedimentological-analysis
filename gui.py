import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
#from tkinter import filedialog, messagebox

data = []

def manual_data_entry():
    global data
    data = []

    def update_data_display():
        last_entries = data[-3:]  # Get the last 3 data entries
        label31sj = [int(entry) for entry in last_entries]
        data_display_label.config(text="Last 3 Data Entries: " + ", ".join(map(str, label31sj)))

        # Update the total count label
        total_count_label.config(text="Total Data Count: " + str(len(data)))

    def add_data_point(event):
        entry = data_entry_var.get().strip()
        try:
            value = int(entry)

            if value < 0 or value > 360:
                warning_label.config(text="Invalid value! The data should be in azimuth degrees!", bg="grey")
                root.after(5000, clear_warning)
                data_entry_var.set("") # clear after return
                return # in order to not include the data to the dataset
            data.append(float(entry))
            data_entry_var.set("")  # clear the entry for next data point

        except ValueError:
            warning_label.config(text="Invalid input! Please enter a valid numeric value.", bg="grey")
            root.after(5000, clear_warning)
        data_entry_var.set("")  #clear the entry for nbext data point

        #messagebox.showwarning("Invalid Input", "Please enter a valid numeric value.")

        update_data_display()


    def clear_warning():
        warning_label.config(text="")  # Clear the warning label

    def finish_data_entry():
        root.bind('<Return>', None)  # Unbind the Enter key
        plot_histogram_and_rose(data)


    def reset_data():
        global data
        data = []
        update_data_display()

    # Clear the main application window
    for widget in root.winfo_children():
        widget.destroy()

    data_entry_var = tk.StringVar()
    data_entry_field = tk.Entry(root, textvariable=data_entry_var)
    data_entry_field.pack()
    data_entry_field.focus()  # Set focus on the data entry field

    data_entry_field.bind('<Return>', add_data_point)  # Bind Enter key to add_data_point function

    # Warning label to display error messages
    warning_label = tk.Label(root, text="", fg="red")
    warning_label.pack()

    # Button to finish data entry and plot
    finish_button = tk.Button(root, text="Finish and Plot", command=finish_data_entry)
    finish_button.pack()

    # Button to reset data
    reset_button = tk.Button(root, text="Reset Data", command=reset_data)
    reset_button.pack()

    # Data display label to show the last 4 data entries
    data_display_label = tk.Label(root, text="", fg="black", bg="white")
    data_display_label.pack()

    # total count label
    total_count_label = tk.Label(root, text=" ", fg="red")
    total_count_label.pack()

    # Update the data display label initially
    update_data_display()
    total_count_label.config(text="Total Data count: " + str(len(data)))

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

    # Add labels to the bars that match the y-axis tick values
    for bar, height in zip(ax.patches, hist):
        if height not in ax.get_yticks():
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, str(height), ha='center', va='bottom')

    fig2 = plt.figure(figsize=(7, 7))
    ax = fig2.add_subplot(111, projection='polar')
    ax.bar(np.deg2rad(midpoints), hist, width=np.deg2rad(i), edgecolor='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.set_title('paleoakıntı verileri için gül diyagramı')
    ax.set_thetagrids(np.arange(0, 360, i), labels=np.arange(0, 360, i))
    ax.set_rlabel_position(135)
    ax.set_yticks(hist)
    ax.set_yticklabels(hist)

    plt.show()

# Create the main application window
root = tk.Tk()
root.title("Paleocurrent Plotter for Sedimentological Analysis v0.3.1")
root.geometry("1280x720")
root.configure(bg="grey")

# Button to manually add data
manual_button = tk.Button(root, text="Manually Add Data", command=manual_data_entry, pady=32, padx=32)
manual_button.pack()

# Button to add data through a CSV file
csv_button = tk.Button(root, text="Add Data through a CSV file", command=csv_data_entry, pady=32, padx=32)
csv_button.pack()

# Run the application
root.mainloop()
