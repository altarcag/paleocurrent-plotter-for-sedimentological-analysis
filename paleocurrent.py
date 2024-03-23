import customtkinter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as fnt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk, Image
import os
import webbrowser

data = []

canvas1 = 0
canvas2 = 0
toolbar = 0

manual_button_clicked = False

def manual_data_entry():
    if manual_data_entry.been_pressed:
        return
    else:
        manual_data_entry.been_pressed = True

    global data
    data = []

    def update_data_display():
        last_entries = data[-3:]  # Get the last 3 data entries
        label31sj = [int(entry) for entry in last_entries]
        data_display_label.configure(text="Last 3 Data Entries: " + ", ".join(map(str, label31sj)))

        # Update the total count label
        total_count_label.configure(text="Total Data Count: " + str(len(data)))

    def add_data_point(event):
        entry = data_entry_var.get().strip()
        try:
            value = int(entry)

            if value < 0 or value > 360:
                warning_label.configure(text="Invalid value!\nThe data should be in azimuth degrees!")
                root.after(5000, clear_warning)
                data_entry_var.set("")  # clear after return
                return  # in order to not include the data to the dataset
            data.append(float(entry))
            data_entry_var.set("")  # clear the entry for next data point

        except ValueError:
            warning_label.configure(text="Invalid input!\nInsert a valid numeric value")
            root.after(5000, clear_warning)
        data_entry_var.set("")  # clear the entry for nbext data point

        update_data_display()

    def clear_warning():
        warning_label.configure(text="")  # Clear the warning label

    def finish_data_entry():
        root.bind('<Return>', None)  # Unbind the Enter key
        plot_histogram_and_rose(data)

    def reset_data():
        global data
        data = []
        update_data_display()

    data_entry_var = customtkinter.StringVar()
    data_entry_field = customtkinter.CTkEntry(button_frame, textvariable=data_entry_var, width=180)
    data_entry_field.pack(pady=2)
    data_entry_field.focus()  # Set focus on the data entry field
    data_entry_field.bind('<Return>', add_data_point)  # Bind Enter key to add_data_point function

    # Button to finish data entry and plot
    finish_button = customtkinter.CTkButton(button_frame, text="Finish and Plot", command=finish_data_entry,
                                            height=32, width=180)
    finish_button.pack(padx=2, pady=2)

    # Button to reset data
    reset_button = customtkinter.CTkButton(button_frame, text="Reset Data", command=reset_data,
                                           height=32, width=180)
    reset_button.pack(padx=2, pady=2)

    # Warning label to display error messages
    warning_label = customtkinter.CTkLabel(button_frame, text="")
    warning_label.pack(pady=2)

    # Data display label to show the last data entries
    data_display_label = customtkinter.CTkLabel(button_frame, text="")
    data_display_label.pack()

    # total count label
    total_count_label = customtkinter.CTkLabel(button_frame, text=" ")
    total_count_label.pack()

    # Update the data display label initially
    update_data_display()
    total_count_label.configure(text="Total Data Count: " + str(len(data)))

manual_data_entry.been_pressed = False

def csv_data_entry():
    global data

    csv_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    data = pd.read_csv(csv_path, header=None).values.flatten()
    plot_histogram_and_rose(data)


def plot_histogram_and_rose(data, i=30):
    global canvas1
    global canvas2
    global toolbar

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.hist(data, np.arange(0, 361, i))
    ax.set_xlim(0, 360)
    plt.xticks(np.arange(0, 361, i))

    ax.set_title("Histogram")
    plt.xlabel("Azimuth Degrees", fontsize=15)
    plt.ylabel("Frequency", fontsize=15)

    bins = np.arange(0, 361, i)
    hist, _ = np.histogram(data, bins=bins)
    hist = np.array(hist)
    midpoints = bins[:-1] + np.diff(bins) / 2

    # Add labels to the bars that doesn't match the y-axis tick values
    for bar, height in zip(ax.patches, hist):
        if height not in ax.get_yticks():
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05, str(height), ha='center', va='bottom')

    fig2 = plt.figure(figsize=(6, 6))
    ax = fig2.add_subplot(111, projection='polar')
    ax.bar(np.deg2rad(midpoints), hist, width=np.deg2rad(i), edgecolor='white')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.set_title('Rose Diagram')
    ax.set_thetagrids(np.arange(0, 360, i), labels=np.arange(0, 360, i))
    ax.set_rlabel_position(135)
    ax.set_yticks(hist)
    ax.set_yticklabels(hist)

    #plt.show()

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
    canvas2.get_tk_widget().pack(expand=True, fill='both')

    canvas1 = FigureCanvasTkAgg(fig, master=root)
    canvas1.draw()

    toolbar = NavigationToolbar2Tk(canvas2, root)
    toolbar.pack(fill='both')
    toolbar.update()


# the def for adjusting the degree intervals
    
def adjustdg(i):
    plot_histogram_and_rose(data, i)

interval_buttons_added = False  # Track whether interval buttons are currently added or not
interval_button_frame = None  # Store the frame containing interval buttons

def interval_buttons():
    global interval_buttons_added, interval_button_frame
    
    # If interval buttons are already added, remove them and update the flag
    if interval_buttons_added:
        interval_button_frame.destroy()
        interval_buttons_added = False
    # If interval buttons are not added, add them and update the flag
    else:
        interval_button_frame = customtkinter.CTkFrame(right_frame)
        interval_button_frame.pack(side='top', padx=2, pady=2)
        
        intervals = [15, 20, 30, 45]
        for interval in intervals:
            button = customtkinter.CTkButton(interval_button_frame, text=str(interval), height=32, width=41,
                                             command=lambda i=interval: adjustdg(i))
            button.pack(side='left', padx=2, pady=2)
        interval_buttons_added = True

#key
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
        canvas1.get_tk_widget().pack(expand=True, fill='both')
        switchKey = False
    else:
        canvas1.get_tk_widget().pack_forget()
        toolbar.pack_forget()
        toolbar = NavigationToolbar2Tk(canvas2, root)
        toolbar.update()
        canvas2.get_tk_widget().pack(expand=True, fill='both')
        switchKey = True

def callback(url):
    webbrowser.open_new(url)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Paleocurrent Plotter for Sedimentological Analysis v1.31")
root.geometry("1280x720")
script_dir = os.path.dirname(__file__)
root.iconbitmap(script_dir + '/images/hacettepe_icon.ico')

# Create a frame to hold the buttons on the left side
button_frame = customtkinter.CTkFrame(root)
button_frame.pack(side='left', padx=25, pady=10)

# the images and logos and so on

#img1 = customtkinter.CTkImage(Image.open(script_dir + "\\images\\hulogo.png"), size=(200, 57))
img2 = customtkinter.CTkImage(Image.open(script_dir + "\\images\\jeomuh.png"), size=(200, 200))
#labelimg1 = customtkinter.CTkLabel(button_frame, image=img1, text="")
#labelimg1.pack(padx=6, pady=1)
labelimg2 = customtkinter.CTkLabel(button_frame, image=img2, text="")
labelimg2.pack(pady=10, padx=12)
labelimg2.bind("<Button-1>", lambda e: callback("https://jeomuh.hacettepe.edu.tr/"))


# Create a frame for the right side
right_frame = customtkinter.CTkFrame(root)
right_frame.pack(side='right', padx=25, pady=10)

# Button to manually add data
manual_button = customtkinter.CTkButton(button_frame, text="Manually Add Data", command=lambda: manual_data_entry(),
                                        height=32, width=180)
manual_button.pack(side='top', padx=2, pady=2)

# Button to add data through a CSV file
csv_button = customtkinter.CTkButton(button_frame, text="Add Data through a CSV file", command=lambda: csv_data_entry(),
                                     height=32, width=180)
csv_button.pack(side='top', padx=2, pady=2)


# linksx
link1 = customtkinter.CTkLabel(right_frame, text="github.com/altarcag", cursor="hand2")
link1.pack(padx=2, pady=2)
link1.bind("<Button-1>", lambda e: callback("https://github.com/altarcag"))

# sx
switch_button = customtkinter.CTkButton(right_frame, text="Histogram/Rose Diagram", command=lambda: switch(),
                                        height=32, width=180)
switch_button.pack(side='top', padx=2, pady=2)

# button for adjusting the degree intervals
interval_button = customtkinter.CTkButton(right_frame, text="Adjust Degree Intervals", height=32, width=180,
                                          command=interval_buttons)
interval_button.pack(side='top', padx=2, pady=2)

root.mainloop()
