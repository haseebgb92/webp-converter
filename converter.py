import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import sys

class WebPConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Advertpreneur JPG to WebP Converter")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Set minimum window size
        self.root.minsize(800, 600)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "advertpreneur-64x64.png")
        if os.path.exists(icon_path):
            self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("Custom.TButton",
                           padding=10,
                           font=("Helvetica", 10))
        self.style.configure("Custom.TLabelframe",
                           background="#f0f0f0",
                           padding=15)
        self.style.configure("Custom.TLabelframe.Label",
                           font=("Helvetica", 11, "bold"),
                           background="#f0f0f0")
        
        # Create main container
        self.main_container = ttk.Frame(self.root, style="TFrame")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create and configure GUI elements
        self.setup_gui()
        
        # Set icon (if running as executable)
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        # Create images directory if it doesn't exist
        images_dir = os.path.join(application_path, "images")
        os.makedirs(images_dir, exist_ok=True)

    def setup_gui(self):
        # Title with custom styling
        title_frame = ttk.Frame(self.main_container, style="TFrame")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(title_frame,
                             text="Advertpreneur",
                             font=("Helvetica", 24, "bold"),
                             fg="#FF8C00",  # Orange color matching the logo
                             bg="#f0f0f0")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                text="JPG to WebP Converter",
                                font=("Helvetica", 14),
                                fg="#0066CC",  # Blue color matching the logo
                                bg="#f0f0f0")
        subtitle_label.pack()

        # Settings frame
        settings_frame = ttk.LabelFrame(self.main_container,
                                      text="Conversion Settings",
                                      style="Custom.TLabelframe")
        settings_frame.pack(fill="x", pady=(0, 20))

        # Quality control
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.pack(fill="x", pady=10)
        
        self.quality_var = tk.IntVar(value=80)
        quality_label = ttk.Label(quality_frame,
                                text="Quality:",
                                font=("Helvetica", 10))
        quality_label.pack(side="left", padx=(0, 10))
        
        self.quality_display = ttk.Label(quality_frame,
                                       text="80%",
                                       font=("Helvetica", 10, "bold"))
        self.quality_display.pack(side="right", padx=(10, 0))
        
        quality_slider = ttk.Scale(quality_frame,
                                 from_=1,
                                 to=100,
                                 variable=self.quality_var,
                                 orient="horizontal",
                                 command=self.update_quality_display)
        quality_slider.pack(fill="x", padx=5)

        # Method selection with modern radio buttons
        method_frame = ttk.Frame(settings_frame)
        method_frame.pack(fill="x", pady=10)
        
        self.method_var = tk.StringVar(value="files")
        method_label = ttk.Label(method_frame,
                               text="Select conversion method:",
                               font=("Helvetica", 10))
        method_label.pack(anchor="w", pady=(0, 5))
        
        files_radio = ttk.Radiobutton(method_frame,
                                    text="Convert Individual Files",
                                    variable=self.method_var,
                                    value="files")
        files_radio.pack(anchor="w")
        
        folder_radio = ttk.Radiobutton(method_frame,
                                     text="Convert Entire Folder",
                                     variable=self.method_var,
                                     value="folder")
        folder_radio.pack(anchor="w")

        # Convert button with modern styling
        convert_button = ttk.Button(self.main_container,
                                  text="Start Conversion",
                                  style="Custom.TButton",
                                  command=self.start_conversion)
        convert_button.pack(pady=20)

        # Progress frame
        progress_frame = ttk.LabelFrame(self.main_container,
                                      text="Progress",
                                      style="Custom.TLabelframe")
        progress_frame.pack(fill="x")

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          variable=self.progress_var,
                                          maximum=100,
                                          mode="determinate")
        self.progress_bar.pack(fill="x", pady=10)

        # Status text with modern styling
        self.status_text = tk.Text(progress_frame,
                                 height=8,
                                 font=("Helvetica", 9),
                                 wrap=tk.WORD,
                                 bg="white",
                                 relief="flat")
        self.status_text.pack(fill="both", expand=True)
        
        # Add scrollbar to status text
        scrollbar = ttk.Scrollbar(progress_frame,
                                orient="vertical",
                                command=self.status_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.config(state=tk.DISABLED)

    def update_quality_display(self, *args):
        self.quality_display.config(text=f"{self.quality_var.get()}%")

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()

    def convert_image(self, input_path):
        try:
            output_path = os.path.splitext(input_path)[0] + '.webp'
            with Image.open(input_path) as img:
                # Convert RGBA images to RGB to avoid transparency issues
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background

                # Get original file size
                original_size = os.path.getsize(input_path)

                # Save with specified quality
                img.save(output_path, 'WEBP', quality=self.quality_var.get(), method=6)

                # Get new file size
                new_size = os.path.getsize(output_path)
                
                percentage = (new_size / original_size) * 100
                savings = ((original_size - new_size) / original_size) * 100

                self.update_status(
                    f"✓ Converted: {os.path.basename(input_path)}\n"
                    f"   Original: {original_size/1024/1024:.1f}MB → New: {new_size/1024/1024:.1f}MB\n"
                    f"   Space saved: {savings:.1f}%\n"
                )
                return True
        except Exception as e:
            self.update_status(f"❌ Error converting {os.path.basename(input_path)}: {str(e)}")
            return False

    def start_conversion(self):
        if self.method_var.get() == "files":
            files = filedialog.askopenfilenames(
                title="Select JPG files",
                filetypes=[("JPEG files", "*.jpg *.jpeg")]
            )
        else:
            folder = filedialog.askdirectory(title="Select Folder with JPG Images")
            if folder:
                files = []
                for root, _, filenames in os.walk(folder):
                    for filename in filenames:
                        if filename.lower().endswith(('.jpg', '.jpeg')):
                            files.append(os.path.join(root, filename))

        if not files:
            return

        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)

        total_files = len(files)
        successful = 0

        for i, file_path in enumerate(files, 1):
            if self.convert_image(file_path):
                successful += 1
            self.progress_var.set((i / total_files) * 100)
            self.root.update()

        self.progress_var.set(100)
        self.update_status(f"\n✨ Conversion complete! Successfully converted {successful} out of {total_files} files.")
        messagebox.showinfo("Complete", f"Converted {successful} out of {total_files} files!")

def main():
    root = tk.Tk()
    app = WebPConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
