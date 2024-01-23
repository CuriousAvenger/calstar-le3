import tkinter as tk

def button_click(button_number):
    print(f"Button {button_number} clicked!")

root = tk.Tk()
root.title("Six Buttons Example")

# Create six buttons and place them next to each other
for i in range(1, 7):
    button = tk.Button(root, text=f"Button {i}", height=10, width=20)
    button.pack(side=tk.LEFT, padx=20, pady=20)

root.mainloop()
