import tkinter as tk
from tkinter import ttk
import random
import serial
import time
import re

def list_serial_ports():
    """List available serial ports."""
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def parse_data(data_string):
    """Parse the data string into a dictionary."""
    # Define the regex pattern for extracting key-value pairs
    pattern = r"(\w+): ([\d.-]+)"
    
    # Find all matches in the data string
    matches = re.findall(pattern, data_string)
    
    # Convert matches to a dictionary
    data_dict = {key: float(value) if '.' in value or 'e' in value else int(value) for key, value in matches}
    
    return data_dict

class SerialDataApp:
    def __init__(self, root):
        self.root = root
        self.data_labels = {}

        # Create a frame for the serial port and baud rate selection
        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and place widgets for serial port selection
        self.port_label = ttk.Label(frame, text="Select Serial Port:")
        self.port_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.port_combo = ttk.Combobox(frame, values=list_serial_ports())
        self.port_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Create and place widgets for baud rate selection
        self.baudrate_label = ttk.Label(frame, text="Select Baud Rate:")
        self.baudrate_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.baudrate_combo = ttk.Combobox(frame, values=[9600, 115200])
        self.baudrate_combo.grid(row=1, column=1, padx=5, pady=5)
        self.baudrate_combo.set(9600)  # Default baud rate
        
        self.connect_button = ttk.Button(frame, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5)

        self.boxApp = Box3DAxisApp(root)

        self.update_interval = 100  # Update interval in milliseconds

    def connect_serial(self):
        """Connect to the selected serial port and start reading data."""
        selected_port = self.port_combo.get()
        baud_rate = int(self.baudrate_combo.get())
        if not selected_port:
            return
        
        # Initialize serial communication
        try:
            self.ser = serial.Serial(selected_port, baud_rate, timeout=1)
        except serial.SerialException as e:
            self.update_status(f"Error opening serial port: {e}")
            return
        
        self.update_status(f"Listening on port {selected_port} at baud rate {baud_rate}...")
        self.read_serial_data()

    def update_status(self, message):
        """Update the status label with the given message."""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
        else:
            self.status_label = ttk.Label(self.root, text=message, foreground="red")
            self.status_label.grid(row=2, column=0, padx=5, pady=5)
    
    def read_serial_data(self):
        """Read data from the serial port and update the display."""
        try:
            if self.ser.in_waiting > 0:  # Check if there's data waiting
                raw_data = self.ser.readline().decode('utf-8', errors='replace').strip()  # Read and decode data
                if raw_data:
                    parsed_data = parse_data(raw_data)
                    if parsed_data:  # Only update if there's actual parsed data
                        self.update_data_display(parsed_data)
                        self.boxApp.update_box(parsed_data)  # Update box position with parsed data
        except serial.SerialException as e:
            self.update_status(f"Serial error: {e}")
            self.ser.close()
            return
        
        # Schedule the next read
        self.root.after(self.update_interval, self.read_serial_data)

    def update_data_display(self, data):
        """Update the GUI to display the new data."""
        for key, value in data.items():
            if key not in self.data_labels:
                label = ttk.Label(self.root, text=f"{key}:")
                value_label = ttk.Label(self.root, text=f"{value}")
                label.grid(row=len(self.data_labels)+3, column=0, padx=5, pady=5, sticky=tk.W)
                value_label.grid(row=len(self.data_labels)+3, column=1, padx=5, pady=5, sticky=tk.W)
                self.data_labels[key] = value_label
            else:
                self.data_labels[key].config(text=f"{value}")

class Box3DAxisApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=1, column=0, padx=5, pady=5)

        # Initial coordinates and box size
        self.x, self.y, self.z = 0, 0, 0
        self.box_size = 50

        # Draw the initial axis
        self.draw_axis()

        # Draw the initial box
        self.box_id = self.draw_box(self.x, self.y, self.box_size)

    def draw_axis(self):
        # Draw X, Y, Z axes
        self.canvas.create_line(50, 200, 350, 200, arrow=tk.LAST, fill="black")  # X-axis
        self.canvas.create_text(355, 200, text="X-axis", anchor=tk.W)  # Label for X-axis

        self.canvas.create_line(200, 350, 200, 50, arrow=tk.LAST, fill="black")  # Y-axis
        self.canvas.create_text(200, 45, text="Y-axis", anchor=tk.S)  # Label for Y-axis

        self.canvas.create_line(200, 200, 350, 50, arrow=tk.LAST, fill="black")  # Z-axis
        self.canvas.create_text(355, 45, text="Z-axis", anchor=tk.S)  # Label for Z-axis

    def draw_box(self, x, y, size):
        # Draw a blue box at the given coordinates
        return self.canvas.create_rectangle(200 + x, 200 - y, 200 + x + size, 200 - y - size, outline="blue", fill="lightblue")

    def update_box(self, coordinates):
        """Update box position and size based on new coordinates from ESP32."""
        # Delete the previous box
        self.canvas.delete(self.box_id)

        # Extract and update the box coordinates
        self.x = coordinates.get('Xval', 0)
        self.y = coordinates.get('Yval', 0)
        self.z = coordinates.get('Zval', 0)

        # Update box size based on z-axis
        if self.z >= 0:
            new_size = self.box_size - self.z
        else:
            new_size = self.box_size + abs(self.z)

        # Draw updated box
        self.box_id = self.draw_box(self.x, self.y, new_size)


if __name__ == "__main__":
    root = tk.Tk()
    app = SerialDataApp(root)
    root.mainloop()
