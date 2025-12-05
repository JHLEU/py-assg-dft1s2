import customtkinter as ctk
from PIL import Image
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "system", "dark", "light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

def click():
    print("Button clicked!")

# Creating the window
window = ctk.CTk()
window.geometry("1200x700")  # Adjusted for better layout
window.title("FitQuest")

# Configure grid layout for better positioning
window.grid_columnconfigure(0, weight=1)

# Create a frame for better organization
main_frame = ctk.CTkFrame(window)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Create a label widget with modern styling
welcome = ctk.CTkLabel(
    main_frame,
    text="Welcome to FitQuest!",
    font=("Arial", 40, "bold"),
    text_color="#FFFFFF"
)

welcome_note = ctk.CTkLabel(
    main_frame,
    text="Please answer the following questions truthfully to get the best results.",
    font=("Arial", 20),
    text_color="#CCCCCC",
    wraplength=800  # Wrap text if too long
)

# Create a modern button
button = ctk.CTkButton(
    main_frame,
    text="Next",
    command=click,
    font=("Arial", 18, "bold"),
    height=40,
    width=120,
    corner_radius=10,
    fg_color="#1f6aa5",  # Custom color
    hover_color="#144870"  # Darker shade on hover
)

# If you want to use images with CustomTkinter
try:
    # For CustomTkinter, use CTkImage which supports PNG with transparency
    photo = ctk.CTkImage(
        light_image=Image.open(r"C:\\TARUMT\\Python\\Assignment\\resourse\\fitness.png"),
        dark_image=Image.open(r"C:\\TARUMT\\Python\\Assignment\\resourse\\fitness.png"),
        size=(100, 100)  # Resize image
    )
    
    # Create a label with image
    image_label = ctk.CTkLabel(main_frame, image=photo, text="")
    image_label.pack(pady=10)
    
except ImportError:
    print("PIL (Pillow) is required for images. Install with: pip install pillow")
except FileNotFoundError:
    print("Image file not found. Continuing without image.")

# Alternative layout using pack (centered)
welcome.pack(pady=(50, 10))
welcome_note.pack(pady=10)
button.pack(pady=30)

# Alternative layout using grid if you prefer more control:
# welcome.grid(row=0, column=0, pady=(50, 10), sticky="n")
# welcome_note.grid(row=1, column=0, pady=10, sticky="n")
# button.grid(row=2, column=0, pady=30, sticky="n")

# If you need the window icon, CustomTkinter has limited icon support
# You might need to use window.after() to set icon if needed

# Start the main loop
window.mainloop()