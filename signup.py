import tkinter as tk
import customtkinter as ctk
import os
import json

class Signup:
    def __init__(self):
        #initialize window setup
        self.window = tk.Tk()
        self.window.state("zoomed")
        self.window.title("FitQuest")
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

        ctk.CTkLabel(self.window,
                    text="Sign Up",
                    font=("Arial",35, "bold"), 
                    fg_color="white", 
                    text_color="black"
                    ).pack(anchor="center", pady=(50,0), )
                    
        # Container frame for photo + signupbox
        signupbox_container = tk.Frame(self.window, bg = "white")
        signupbox_container.pack(anchor = "center", pady = (100,0))

        #photo placement
        self.photo = photo
        fit_photo = tk.Label(signupbox_container, image=self.photo,)
        fit_photo.pack(side="left")

        #signup box
        signup_box = tk.Frame(
            signupbox_container,
            width = 600,
            height = 506,
            bg = "gray",
            highlightbackground="black",  
            highlightthickness=0
        )
        signup_box.pack(side="right", pady=20)
        signup_box.pack_propagate(False)



        #Text box for user input

        #Username display
        tk.Label(signup_box, 
                 text="Username                 :", 
                 bg="gray",                  
                 font=("Arial", 12, 'bold'),
                 ).place(relx = 0.02, rely = 0.2)
        #username entry
        self.username_entry = tk.Entry(signup_box, 
                 width=30, 
                 font=("Arial", 13)
                 )
        self.username_entry.place(relx = 0.3, rely = 0.2)
        
        
        #Password display
        tk.Label(signup_box, 
                 text="Password                 :", 
                 bg="gray",                  
                 font=("Arial", 12, 'bold')
                 ).place(relx = 0.02, rely = 0.3)
        #password entry
        self.password_entry = tk.Entry(signup_box, 
                 width=30, 
                 show="*", 
                 font=("Arial", 13)
                 )
        self.password_entry.place(relx = 0.3, rely = 0.3)
        

        #confirm password display
        tk.Label(signup_box, 
                 text="Confirm Password :", 
                 bg="gray",                  
                 font=("Arial", 12, 'bold')
                 ).place(relx = 0.02, rely = 0.4)
        #confirm password entry
        self.confirm_entry = tk.Entry(signup_box, width=30, 
                 show="*", 
                 font=("Arial", 13)
                 )
        self.confirm_entry.place(relx = 0.3, rely = 0.4)
        
        def go_to_login():
            # Get values from entries
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            confirm = self.confirm_entry.get()
            
            # --- VALIDATION ---
            if not username or not password:
                tk.messagebox.showwarning("Missing", "Please fill all fields")
                return
            
            if password != confirm:
                tk.messagebox.showerror("Error", "Passwords don't match")
                return

            # --- SAVE USER DATA TO JSON ---
            try:
                with open('users.json', 'r') as f:
                    users = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                users = {} # Create new if file doesn't exist or is empty

            if username in users:
                tk.messagebox.showerror("Error", "This username is already taken.")
                return

            users[username] = password # Add new user
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4) # Save updated data

            # --- PROCEED TO LOGIN ---
            tk.messagebox.showinfo("Success", "Sign Up successfully!")
            from login import Login_function
            self.window.destroy()
            Login_function()

        #signup button
        ctk.CTkButton(
            master=signup_box,
            text="Sign Up",
            width=150,              
            height=36,              
            fg_color="#FE0161",   
            hover_color="#0400e0",
            text_color="white",
            font=("Arial", 11, "bold"),
            command=lambda: (go_to_login(), )
        ).place(relx=0.9, rely=0.9, anchor="se")

        #cancel button
        def go_back_to_login():
            self.window.destroy()
            from login import Login_function
            Login_function()

        ctk.CTkButton(
            master=signup_box,
            text="Cancel",
            width=150,              
            height=36,              
            fg_color="transparent",   
            hover_color="#0400e0",
            text_color="white",
            font=("Arial", 11, "bold"),
            command=go_back_to_login
        ).place(relx=0.3, rely=0.9, anchor="se")

        self.window.mainloop()

       

if __name__ == "__main__":
    Signup()




