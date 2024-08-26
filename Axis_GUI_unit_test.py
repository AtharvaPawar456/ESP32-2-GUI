import tkinter as tk
import random


class Box3DAxisApp:

    def __init__(self, root):
        self.root = root
        self.root.title("3D Axis Box Manipulation")

        # Canvas to draw the axis and box
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Initial coordinates and box size
        self.x, self.y, self.z = 0, 0, 0
        self.box_size = 50

        # Draw the initial axis
        self.draw_axis()

        # Draw the initial box
        self.box_id = self.draw_box(self.x, self.y, self.box_size)

        # Start updating box position
        self.update_box()

    def draw_axis(self):
        # Draw X, Y, Z axes
        self.canvas.create_line(50, 200, 350, 200, arrow=tk.LAST,
                                fill="black")  # X-axis
        self.canvas.create_text(355, 200, text="X-axis",
                                anchor=tk.W)  # Label for X-axis

        self.canvas.create_line(200, 350, 200, 50, arrow=tk.LAST,
                                fill="black")  # Y-axis
        self.canvas.create_text(200, 45, text="Y-axis",
                                anchor=tk.S)  # Label for Y-axis

        self.canvas.create_line(200, 200, 350, 50, arrow=tk.LAST,
                                fill="black")  # Z-axis
        self.canvas.create_text(355, 45, text="Z-axis",
                                anchor=tk.S)  # Label for Z-axis

    def draw_box(self, x, y, size):
        # Draw a blue box at the given coordinates
        return self.canvas.create_rectangle(200 + x,
                                            200 - y,
                                            200 + x + size,
                                            200 - y - size,
                                            outline="blue",
                                            fill="lightblue")

    def update_box(self):
        # Delete the previous box
        self.canvas.delete(self.box_id)

        # Generate random movements for X, Y, Z axes
        self.x += random.randint(-20, 20)
        self.y += random.randint(-20, 20)
        self.z = random.randint(-10, 10)

        # Update box size based on z-axis
        if self.z >= 0:
            new_size = self.box_size - self.z
        else:
            new_size = self.box_size + abs(self.z)

        # Draw updated box
        print(self.x, self.y, new_size)
        self.box_id = self.draw_box(self.x, self.y, new_size)

        # Repeat the update every 500ms
        self.root.after(500, self.update_box)


if __name__ == "__main__":
    root = tk.Tk()
    app = Box3DAxisApp(root)
    root.mainloop()
