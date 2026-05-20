import tkinter as tk
import pyperclip

class RegionPicker:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        
        # Make it full screen and slightly transparent so you can see the game behind it
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.configure(cursor="cross") # Changes mouse to a crosshair

        # Create a canvas to draw the red box on
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        # Bind mouse events (Click, Drag, Release)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        # Record starting coordinates when mouse is clicked
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # Create the initial rectangle
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline='red', width=3, fill='gray'
        )

    def on_drag(self, event):
        # Update the rectangle size as the mouse moves
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        # Record final coordinates when mouse is released
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        # Do the math to get Top-Left X/Y, Width, and Height
        left = int(min(self.start_x, end_x))
        top = int(min(self.start_y, end_y))
        width = int(abs(end_x - self.start_x))
        height = int(abs(end_y - self.start_y))

        # Format exactly how it looks in your strategies.py
        region_str = f"({left}, {top}, {width}, {height})"
        
        print(f"\n🎯 Selected Region: {region_str}")
        
        # Auto-copy to clipboard!
        pyperclip.copy(region_str)
        print("📋 Copied to clipboard! Just press Ctrl+V in your code.")
        
        # Close the overlay
        self.root.destroy()

if __name__ == "__main__":
    print("🖥️ Starting Region Picker...")
    print("🖱️ Click and drag a box over your target area.")
    picker = RegionPicker()
    picker.root.mainloop()