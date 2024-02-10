from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from serial import Serial

def update_graph(i, axs):
    # Generate some example data (you can replace this with your live data)
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + i / 10.0)

    # Clear the previous plot
    for ax in axs:
        ax.clear()

    # Plot the new data on each subplot
    for ax in axs:
        ax.plot(x, y, label='Live Data')

        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Live Updating Graph')

        # Add legend
        ax.legend()

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

    def button_click(self, button_number, button_name):
        print(f"{button_name} clicked!")
        self.esp32.write(str(button_number).encode())

        
    def start_live_update(self, axs):
        # Create an animation for live updating
        self.animation = FuncAnimation(self.fig, update_graph, fargs=(axs,), interval=100)

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveGraphApp(root)
    root.mainloop()
