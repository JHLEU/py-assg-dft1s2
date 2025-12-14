import tkinter as tk
import customtkinter as ctk
import os
from tkinter import messagebox
import json


# Global variable to store the username of the logged-in user
LOGGED_IN_USER = None
IS_LOGGED_IN = False  # global login status (True after successful login)

class Login_function:
    def __init__(self, show_skip: bool = True):
        self.show_skip = show_skip

        global LOGGED_IN_USER
        LOGGED_IN_USER = None # Reset on window creation

        #initialize window setup
        self.window = tk.Tk()
        self.window.state("zoomed")
        self.window.title("FitQuest - Login")
        self.window.attributes('-topmost', True)
        self.window.lift()
        self.window.focus_force()
        ctk.set_appearance_mode("Dark")  # Or "Dark"/"Light"
        ctk.set_default_color_theme("blue")  # Your theme
        ctk.set_widget_scaling(1.0)  # Base scaling; adjust if needed (e.g., 1.2 for higher DPI)
        ctk.set_window_scaling(1.0)  # Window scaling

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
        login_text.pack(pady=(100,0), anchor = "center") 
        
        # Container frame for photo + login box
        LoginBox_container = tk.Frame(self.window, bg = "white")
        LoginBox_container.pack(anchor = "center", pady = (50,0))

        #photo placement
        self.photo = photo
        fit_photo = tk.Label(LoginBox_container, image=self.photo,)
        fit_photo.pack(side="left")

        #login box
        login_box = tk.Frame(
            LoginBox_container,
            width = 600,
            height = 506,
            bg = "gray",
            highlightbackground="black",  
            highlightthickness=0
        )
        login_box.pack(side="right", pady=20)
        login_box.pack_propagate(False)

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
            command=self.handle_login #go to handle login funtion to process user input credential
        ).place(relx=0.9, rely=0.9, anchor="se")

        # "Forget Password?" button
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

        # "Not a member" button/link to call signup
        ctk.CTkButton(
            master=login_box,
            text="Not a member yet? Sign up now!",
            fg_color="transparent",
            hover=False,
            text_color="white",
            font=("Arial", 10, "underline"),
            command=self.go_to_signup
        ).place(relx=0.5, rely=0.41, anchor="s") # Adjusted position

        # Show Skip only on first launch
        if self.show_skip:
            tk.Button(
                login_box,
                text="Skip",
                width=15,
                bg="gray",
                fg="white",
                font=("Arial", 11, "bold"),
                command=self.handle_skip
            ).place(relx=0.1, rely=0.9, anchor="sw")

        # Show Cancel only when called by others
        if not self.show_skip:
            tk.Button(
                login_box,
                text="Cancel",
                width=15,
                bg="gray",
                fg="white",
                font=("Arial", 11, "bold"),
                command=self.window.destroy
            ).place(relx=0.3, rely=0.9, anchor="se")

        self.window.mainloop()

    def handle_login(self):
        global LOGGED_IN_USER, IS_LOGGED_IN
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
            IS_LOGGED_IN = True
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.window.destroy()
            from Assignment import PinkThemedFitnessQuestionn
            root = tk.Tk()
            app = PinkThemedFitnessQuestionn(root)
            root.mainloop()
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

    def handle_skip(self):
        global LOGGED_IN_USER, IS_LOGGED_IN
        LOGGED_IN_USER = None
        IS_LOGGED_IN = False
        self.window.destroy()
        
        from Assignment import PinkThemedFitnessQuestionn
        root = tk.Tk()
        app = PinkThemedFitnessQuestionn(root)
        root.mainloop()


# Use when running directly (first time):
if __name__ == "__main__":
    Login_function(show_skip=True)

# Called from other files:
# from login import Login_function
# Login_function(show_skip=False)




