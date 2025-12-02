import customtkinter as ctk
import tkinter as tk
from PIL import *

ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue") # Themes: "blue" (default), "dark-blue", "green"

app = ctk.CTk()
app.title("User SignUp")

ctk_entry = ctk.CTkEntry(
    app,
    width=200,
    height=40,
    corner_radius=10,
    placeholder_text="Enter text here...",
    font=("Roboto", 14),
    text_color="white",
    placeholder_text_color="gray",
    fg_color=("gray75", "gray25") # Outer and inner background colors
)
ctk_entry.pack(pady=20)




app.mainloop()
    