import tkinter as tk
import time
import os
from PIL import ImageGrab

class ImageSnipper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.configure(cursor="cross")
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.coords = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline='red', width=2
        )

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        
        # Calculate bounding box
        left = int(min(self.start_x, end_x))
        top = int(min(self.start_y, end_y))
        right = int(max(self.start_x, end_x))
        bottom = int(max(self.start_y, end_y))
        
        self.coords = (left, top, right, bottom)
        self.root.quit() # Stop the UI loop

def run_snipper():
    print("🖥️ Starting Image Snipper...")
    print("🖱️ Click and drag a box over the button you want to save.")
    
    snipper = ImageSnipper()
    snipper.root.mainloop()
    
    coords = snipper.coords
    snipper.root.destroy() # Completely close the gray overlay window
    
    if not coords or (coords[2]-coords[0]) == 0 or (coords[3]-coords[1]) == 0:
        print("⚠️ Invalid selection. Cancelled.")
        return

    # Wait a fraction of a second for the gray overlay to visually disappear from your monitor
    time.sleep(0.3) 
    
    # Take the screenshot of those exact coordinates
    screenshot = ImageGrab.grab(bbox=coords)
    
    # Ask you what to name it directly in the terminal
    filename = input("\n📝 Enter a name for this image (e.g., attack_button): ")
    
    # Auto-add .png if you forgot to type it
    if not filename.endswith('.png'):
        filename += '.png'
        
    # Ensure the images folder exists, then save it
    os.makedirs('images', exist_ok=True)
    filepath = os.path.join('images', filename)
    screenshot.save(filepath)
    
    print(f"✅ Saved successfully to: {filepath}")

if __name__ == "__main__":
    run_snipper()