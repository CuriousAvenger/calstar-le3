import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def update_graph(i, ax):
    # Generate some example data (you can replace this with your live data)
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + i / 10.0)

    # Clear the previous plot
    ax.clear()

    # Plot the new data
    ax.plot(x, y, label='Live Data')

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Live Updating Graph')

    # Add legend
    ax.legend()

class LiveGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Combined Example")

        # Create a frame to hold the graph
        self.graph_frame = ttk.Frame(root)
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a Matplotlib figure and axis
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a button to start the live updating
        self.start_button = ttk.Button(root, text="Start Live Update", command=self.start_live_update)
        self.start_button.pack(side=tk.TOP)

        # Create six buttons and place them next to each other
        for i in range(1, 7):
            button = tk.Button(root, text=f"Button {i}", height=10, width=20)
            button.pack(side=tk.LEFT, padx=20, pady=20)

    def start_live_update(self):
        # Create an animation for live updating
        self.animation = FuncAnimation(self.fig, update_graph, fargs=(self.ax,), interval=100)

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveGraphApp(root)
    root.mainloop()
