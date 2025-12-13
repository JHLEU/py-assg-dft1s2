import tkinter as tk
import customtkinter as ctk
import os
from tkinter import messagebox
import json # <-- Add import

# Global variable to store the username of the logged-in user
LOGGED_IN_USER = None

class Login_function:
    def __init__(self):
        global LOGGED_IN_USER
        LOGGED_IN_USER = None # Reset on window creation

        #initialize window setup
        self.window = tk.Tk()
        self.window.state("zoomed")
        self.window.title("FitQuest - Login")
        self.window.attributes('-topmost', True)
        self.window.lift()
        self.window.focus_force()

        #load icon files
        icon_path = os.path.join(os.path.dirname(__file__), 'resource', 'fitness.png')
        icon = tk.PhotoImage(file = icon_path)
        self.window.config(background="#FFFFFF")
        self.window.iconphoto(True,icon)

        #load a image
        fit_photo_path = os.path.join(os.path.dirname(__file__), 'resource', 'mike_fit.png')
        photo = tk.PhotoImage(file = fit_photo_path)

        # display tittle login
        login_text = ctk.CTkLabel(
            self.window,
            text="Login",
            font=("Arial", 35, "bold"),
            fg_color="transparent",
            text_color="black"
        )
        login_text.place(relx=0.5, rely=0.2, anchor = "center") 
        
        #login box
        login_box = tk.Frame(
            self.window,
            width = 600,
            height = 506,
            bg = "gray",
            highlightbackground="black",  
            highlightthickness=0
        )
        login_box.place(relx=0.6, rely=0.5, anchor="center")
        login_box.pack_propagate(False)

        #photo placement
        self.photo = photo
        fit_photo = tk.Label(self.window, image=self.photo)
        fit_photo.place(relx=0.353, rely=0.5, anchor="center")

        #Username
        tk.Label(login_box, text="Username :", bg="gray", font=("Arial", 12, 'bold')).place(relx = 0.02, rely = 0.2)
        self.username_entry = tk.Entry(login_box, width=30, font=("Arial", 13))
        self.username_entry.place(relx = 0.3, rely = 0.2)
        
        #Password
        tk.Label(login_box, text="Password  :", bg="gray", font=("Arial", 12, 'bold')).place(relx = 0.02, rely = 0.3)
        self.password_entry = tk.Entry(login_box, width=30, show="*", font=("Arial", 13))
        self.password_entry.place(relx = 0.3, rely = 0.3)
        
        #login button
        ctk.CTkButton(
            master=login_box,
            text="Login",
            width=150,              
            height=36,              
            fg_color="#FE0161",   
            hover_color="#0400e0",
            text_color="white",
            font=("Arial", 11, "bold"),
            command=self.handle_login
        ).place(relx=0.9, rely=0.9, anchor="se")

        #cancel button
        ctk.CTkButton(
            master=login_box,
            text="Cancel",
            width=150,              
            height=36,              
            fg_color="transparent",   
            hover_color="#0400e0",
            text_color="white",
            font=("Arial", 11, "bold"),
            command=self.window.destroy
        ).place(relx=0.3, rely=0.9, anchor="se")

        # "Forget Password?" button - Placed below the password entry
        ctk.CTkButton(
            master=login_box,
            text="Forget Password?",
            width=50,
            fg_color="transparent",
            hover=False,
            text_color="cyan",
            font=("Arial", 10, "underline"),
            command=self.handle_forget_password
        ).place(relx=0.76, rely=0.3) # Adjusted position

        # "Not a member" button/link to call signup - Reverted to bottom center
        ctk.CTkButton(
            master=login_box,
            text="Not a member yet? Sign up now!",
            fg_color="transparent",
            hover=False,
            text_color="white",
            font=("Arial", 10, "underline"),
            command=self.go_to_signup
        ).place(relx=0.5, rely=0.41, anchor="s") # Adjusted position

        self.window.mainloop()

    def handle_login(self):
        """Handles the login logic by validating against users.json."""
        global LOGGED_IN_USER
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Login Error", "No users have signed up yet.")
            return

        # Validate credentials
        if username in users and users[username] == password:
            LOGGED_IN_USER = username
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def handle_forget_password(self):
        """Asks for a username and shows the password."""
        username = tk.simpledialog.askstring("Forget Password", "Enter your username to retrieve password:", parent=self.window)

        if not username:
            return # User cancelled

        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "User database not found.")
            return
        
        # Find user and display password
        if username in users:
            password = users[username]
            messagebox.showinfo("Password Recovery", f"The password for '{username}' is: {password}")
        else:
            messagebox.showerror("Not Found", f"The username '{username}' was not found.")

    def go_to_signup(self):
        """Destroys the login window and opens the signup window."""
        from signup import Signup
        self.window.destroy()
        Signup()


if __name__ == "__main__":
    Login_function()
    # After the window closes, you can check the status
    if LOGGED_IN_USER:
        # Corrected the variable name from LOG_IN_USER to LOGGED_IN_USER
        print(f"The program can now proceed with user: {LOGGED_IN_USER}")
    else:
        print("Login was cancelled or failed.")




