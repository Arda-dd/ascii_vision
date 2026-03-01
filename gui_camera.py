import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Character density ramp (dark to light)
CHAR_SET = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunfjt1{}[?-_+~<>i!lI;:,\"^`'. "

def generate_ascii_canvas(frame, cols=110):
    """Converts an image frame into an ASCII art drawn on a black canvas."""
    height, width = frame.shape[:2]
    
    # Calculate character dimensions
    char_width = width // cols
    char_height = int(char_width / 0.52)
    rows = height // char_height
    
    # Downsample the image to match the ASCII grid
    downsampled_frame = cv2.resize(frame, (cols, rows))
    
    # Create a blank black canvas (Same size as original frame)
    ascii_canvas = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Dinamik font boyutu (Kutuya tam oturması için)
    font_scale = char_width / 12.0 
    
    # Map pixels to characters and draw them on the canvas
    for y in range(rows):
        for x in range(cols):
            b, g, r = downsampled_frame[y, x]
            
            # ITU-R 601 Luma transform
            luminance = int(0.299*r + 0.587*g + 0.114*b)
            char_index = int(luminance * (len(CHAR_SET) - 1) / 255)
            character = CHAR_SET[char_index]
            
            # Render the character
            cv2.putText(ascii_canvas, character, (x * char_width, y * char_height + char_height - 2), 
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (int(b), int(g), int(r)), 1)
            
    return ascii_canvas

class AsciiCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live ASCII Camera Feed - Widescreen Edition")
        # Pencereyi çok daha geniş yapıyoruz (1350x700)
        self.root.geometry("1350x700")
        self.root.configure(bg="#2c3e50")
        
        self.is_camera_running = False
        self.video_capture = None
        
        self._setup_ui()

    def _setup_ui(self):
        """Initializes the user interface components."""
        self.button_frame = tk.Frame(self.root, bg="#2c3e50")
        self.button_frame.pack(pady=20)
        
        self.btn_start = tk.Button(self.button_frame, text="▶ Start Feed", font=("Arial", 14, "bold"), 
                                   bg="#27ae60", fg="white", width=15, command=self.start_camera)
        self.btn_start.grid(row=0, column=0, padx=10)
        
        self.btn_stop = tk.Button(self.button_frame, text="⏹ Stop Feed", font=("Arial", 14, "bold"), 
                                  bg="#c0392b", fg="white", width=15, command=self.stop_camera)
        self.btn_stop.grid(row=0, column=1, padx=10)
        
        self.display_frame = tk.Frame(self.root, bg="#2c3e50")
        self.display_frame.pack(pady=10)
        
        # Label'ların içindeki text tabanlı boyutlandırmayı kaldırdık, 
        # böylece resim gelince kutular resmin gerçek boyutunu (640x480) alacak.
        self.lbl_standard_feed = tk.Label(self.display_frame, bg="black", text="Camera Ready...", fg="white", font=("Arial", 16))
        self.lbl_standard_feed.grid(row=0, column=0, padx=15)
        
        self.lbl_ascii_feed = tk.Label(self.display_frame, bg="black", text="ASCII Engine Ready...", fg="white", font=("Arial", 16))
        self.lbl_ascii_feed.grid(row=0, column=1, padx=15)

    def start_camera(self):
        """Initializes the video capture and starts the update loop."""
        if not self.is_camera_running:
            self.video_capture = cv2.VideoCapture(0)
            self.is_camera_running = True
            self.update_frame()

    def stop_camera(self):
        """Releases the video capture and clears the displays."""
        self.is_camera_running = False
        if self.video_capture:
            self.video_capture.release()
            
        self.lbl_standard_feed.config(image='', text="Camera Stopped")
        self.lbl_ascii_feed.config(image='', text="Engine Stopped")

    def update_frame(self):
        """Reads a frame, processes it, and updates the GUI."""
        if self.is_camera_running:
            success, frame = self.video_capture.read()
            if success:
                # Çözünürlüğü eski haline (640x480) çıkarıyoruz! Daha büyük ve net olacak.
                frame = cv2.resize(frame, (640, 480))
                
                # ASCII işlemini daha fazla sütunla (110) yapıyoruz ki detaylar kaybolmasın.
                ascii_frame = generate_ascii_canvas(frame, cols=110)
                
                img_standard = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                img_ascii = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(ascii_frame, cv2.COLOR_BGR2RGB)))
                
                self.lbl_standard_feed.imgtk = img_standard
                self.lbl_standard_feed.config(image=img_standard, text="")
                
                self.lbl_ascii_feed.imgtk = img_ascii
                self.lbl_ascii_feed.config(image=img_ascii, text="")
                
            self.root.after(30, self.update_frame)

def on_app_closing():
    """Ensures camera is released when the window is closed."""
    app.stop_camera()
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AsciiCameraApp(root)
    root.protocol("WM_DELETE_WINDOW", on_app_closing)
    root.mainloop()