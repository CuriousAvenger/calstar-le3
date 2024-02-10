from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from serial import Serial
from collections import deque
from threading import Thread
import csv
from os.path import isfile
import time
import os

BUFFER_SIZE = 100
write_buffer = []

class LiveGraphApp:
    def __init__(self, root):
        self.esp32 = Serial(
            port='COM3',
            baudrate=115200
        )

        self.root = root
        self.root.title("Combined Example")

        # Create a frame to hold the graphs
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a Matplotlib figure and a 4x5 grid of subplots
        self.fig, axs = plt.subplots(4, 5, sharex=True, sharey=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a button to start the live updating
        self.start_button = tk.Button(root, text="Start Live Update", command=lambda: self.start_live_update(axs))
        self.start_button.pack(side=tk.TOP)

        # Create six buttons and place them next to each other
        button_names = ['Idle', 'Armed', 'Pressed', 'QD', 'Ignition', 'Hot Fire', 'Abort']
        for i in range(len(button_names)):
            button = tk.Button(root, text=button_names[i], height=5, width=10, command=lambda i=i: self.button_click(i, button_names[i]))
            button.pack(padx=20, pady=20, side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Additional code from the second script
        self.num_plots = 11
        self.data_len = 500
        self.deque_list = [deque(maxlen=self.data_len) for _ in range(self.num_plots + 3)]
        self.x, self.PT_O1, self.PT_O2, self.PT_E1, self.PT_E2, self.PT_C1, self.LC_combined, self.LC1, self.LC2, self.LC3, self.TC1, self.TC2, self.TC3, self.TC4 = self.deque_list
        self.plot_titles = ["PT_O1", "PT_O2", "PT_E1", "PT_E2", "PT_C1", "LC Combined", "TC1", "TC2", "TC3", "TC4", "LCs"]

        # Create an animation for live updating
        self.animation = FuncAnimation(self.fig, self.update_graph, fargs=(axs,), interval=100)

        # Additional variables for data collection
        self.filename = self.setup_filename()
        self.port_num = "/dev/cu.usbserial-0001"  # CHECK YOUR PORT !!!
        self.t1 = Thread(target=self.collection)
        self.t1.start()

    def button_click(self, button_number, button_name):
        print(f"{button_name} clicked!")
        self.esp32.write(str(button_number).encode())

    def start_live_update(self, axs):
        # Create an animation for live updating
        self.animation = FuncAnimation(self.fig, self.update_graph, fargs=(axs,), interval=100)

    def update_graph(self, i, axs):
        # Clear the previous plot
        for ax in axs.flatten():
            ax.clear()

        # Plot the new data on each subplot
        for j, ax in enumerate(axs.flatten()):
            line = ax.plot(x, y, label='Live Data')[0]

            # Set labels and title
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title(f'Live Updating Graph - {self.plot_titles[j]}')

            # Add legend
            ax.legend()

    def setup_filename(self):
        file_base = f"HOTFIRE_{time.strftime('%Y-%m-%d', time.gmtime())}"
        file_ext = ".csv"
        test_num = 1

        while isfile(file_base + f"_test{test_num}" + file_ext):
            test_num += 1

        return file_base + f"_test{test_num}" + file_ext

    def collection(self):
        while True:
            data = self.esp32.readline()
            try:
                decoded_bytes = data[:len(data) - 2].decode("utf-8")
                values = decoded_bytes.split(" ")
                print(values)

                write_buffer.append(values)

                if len(values) == 20:
                    self.x.append(float(values[0]) / 1000)
                    self.PT_O1.append(float(values[1]))
                    self.PT_O2.append(float(values[2]))
                    self.PT_E1.append(float(values[3]))
                    self.PT_E2.append(float(values[4]))
                    self.PT_C1.append(float(values[5]))
                    self.LC1.append(float(values[6]))
                    self.LC2.append(float(values[7]))
                    self.LC3.append(float(values[8]))
                    self.LC_combined.append(
                        -0.31888 * (float(values[6]) + float(values[7]) + float(values[8])) + 52501.829)
                    self.TC1.append(float(values[9]))
                    self.TC2.append(float(values[10]))
                    self.TC3.append(float(values[11]))
                    self.TC4.append(float(values[12]))

                if len(write_buffer) >= BUFFER_SIZE:
                    with open(self.filename, "a", newline='') as f:
                        writer = csv.writer(f, delimiter=",")
                        writer.writerows(write_buffer)
                    write_buffer.clear()

            except:
                continue

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveGraphApp(root)
    root.mainloop()
