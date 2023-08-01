import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk, Image
import os

data = []

canvas1 = 0
canvas2 = 0
toolbar = 0

def manual_data_entry():
    # Disable the "Manually Add Data" button to prevent multiple clicks
    manual_button.config(state=tk.DISABLED)

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
                data_entry_var.set("")  # clear after return
                return  # in order to not include the data to the dataset
            data.append(float(entry))
            data_entry_var.set("")  # clear the entry for next data point

        except ValueError:
            warning_label.config(text="Invalid input! Please enter a valid numeric value.", bg="grey")
            root.after(5000, clear_warning)
        data_entry_var.set("")  # clear the entry for nbext data point

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

    data_entry_var = tk.StringVar()
    data_entry_field = tk.Entry(button_frame, textvariable=data_entry_var, width=30)
    data_entry_field.pack()
    data_entry_field.focus()  # Set focus on the data entry field

    data_entry_field.bind('<Return>', add_data_point)  # Bind Enter key to add_data_point function

    # Warning label to display error messages
    warning_label = tk.Label(button_frame, text="", fg="red")
    warning_label.pack()

    # Button to finish data entry and plot
    finish_button = tk.Button(button_frame, text="Finish and Plot", command=finish_data_entry, height=2, width=25)
    finish_button.pack()

    # Button to reset data
    reset_button = tk.Button(button_frame, text="Reset Data", command=reset_data, height=2, width=25)
    reset_button.pack()

    # Data display label to show the last 4 data entries
    data_display_label = tk.Label(button_frame, text="", fg="black", bg="white")
    data_display_label.pack()

    # total count label
    total_count_label = tk.Label(button_frame, text=" ", fg="red")
    total_count_label.pack()

    # Update the data display label initially
    update_data_display()
    total_count_label.config(text="Total Data Count: " + str(len(data)))


def csv_data_entry():
    csv_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    data = pd.read_csv(csv_path, header=None).values.flatten()
    plot_histogram_and_rose(data)


def plot_histogram_and_rose(data):
    global canvas1
    global canvas2
    global toolbar

    i = 30

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.hist(data, np.arange(0, 361, i))
    ax.set_xlim(0, 360)
    plt.xticks(np.arange(0, 361, i))

    plt.xlabel("Degree Intervals", fontsize=15)
    plt.ylabel("Frekans", fontsize=15)

    bins = np.arange(0, 361, i)
    hist, _ = np.histogram(data, bins=bins)
    hist = np.array(hist)
    midpoints = bins[:-1] + np.diff(bins) / 2

    # Add labels to the bars that match the y-axis tick values
    for bar, height in zip(ax.patches, hist):
        if height not in ax.get_yticks():
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05, str(height), ha='center', va='bottom')

    fig2 = plt.figure(figsize=(6, 6))
    ax = fig2.add_subplot(111, projection='polar')
    ax.bar(np.deg2rad(midpoints), hist, width=np.deg2rad(i), edgecolor='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.set_title('Rose Diagram for Paleocurrent values')
    ax.set_thetagrids(np.arange(0, 360, i), labels=np.arange(0, 360, i))
    ax.set_rlabel_position(135)
    ax.set_yticks(hist)
    ax.set_yticklabels(hist)

    # plt.show()

    if canvas1:
        canvas1.get_tk_widget().pack_forget()
        canvas1 = 0
    if canvas2:
        canvas2.get_tk_widget().pack_forget()
        canvas2 = 0
    if toolbar:
        toolbar.pack_forget()
        toolbar.update()

    # creating a canvas to put the plotted charts inside of the gui
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas2.draw()
    canvas2.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas2, root)
    toolbar.update()

    canvas1 = FigureCanvasTkAgg(fig, master=root)
    canvas1.draw()


# anahtar ;)
switchKey = True


def switch():
    global switchKey
    global canvas1
    global canvas2
    global toolbar
    if switchKey:
        canvas2.get_tk_widget().pack_forget()
        toolbar.pack_forget()
        toolbar = NavigationToolbar2Tk(canvas1, root)
        toolbar.update()
        canvas1.get_tk_widget().pack()
        switchKey = False
    else:
        canvas1.get_tk_widget().pack_forget()
        toolbar.pack_forget()
        toolbar = NavigationToolbar2Tk(canvas2, root)
        toolbar.update()
        canvas2.get_tk_widget().pack()
        switchKey = True


# Create the main application window
root = tk.Tk()
root.title("Paleocurrent Plotter for Sedimentological Analysis v0.3.1")
root.geometry("1280x768")
root.configure(bg="grey")
script_dir = os.path.dirname(__file__)
root.iconbitmap(script_dir + '/images/hacettepe_icon.ico')

# Create a frame to hold the buttons
button_frame = ttk.Frame(root)
button_frame.pack(side='left', padx=25, pady=10)

# the images and logos and so on

img1 = ImageTk.PhotoImage(Image.open(script_dir + "\\images\\hulogo.png"))
img2 = ImageTk.PhotoImage(Image.open(script_dir + "\\images\\jeomuh.png"))
labelimg1 = tk.Label(button_frame, image=img1)
labelimg1.pack()
labelimg2 = tk.Label(button_frame, image=img2)
labelimg2.pack()

# Button to manually add data
manual_button = tk.Button(button_frame, text="Manually Add Data", command=manual_data_entry, height=5, width=25)
manual_button.pack(side='top', padx=1.5, pady=1.5)

# Button to add data through a CSV file
csv_button = tk.Button(button_frame, text="Add Data through a CSV file", command=csv_data_entry, height=5, width=25)
csv_button.pack(side='top', padx=1.5, pady=1.5)

# Create a frame for the right side
right_frame = ttk.Frame(root)
right_frame.pack(side='right', padx=25, pady=10)

# sex
switch_button = tk.Button(right_frame, text="Histogram/Rose Diagram", command=switch, height=5, width=25)
switch_button.pack(side='top', padx=1.5, pady=1.5)

# Run the application
root.mainloop()
