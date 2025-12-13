import tkinter as tk
import customtkinter as ctk
import os
from login import Login_function

class Signup:
    def __init__(self):
        #initialize window setup
        window = tk.Tk()
        window.state("zoomed")
        window.title("FitQuest")
        window.attributes('-topmost', True)
        window.lift()
        window.focus_force()

        #load icon files
        icon_path = os.path.join(os.path.dirname(__file__), 'resource', 'fitness.png')
        icon = tk.PhotoImage(file = icon_path)
        window.config(background="#FFFFFF")
        window.iconphoto(True,icon)

        #load a image
        fit_photo_path = os.path.join(os.path.dirname(__file__), 'resource', 'mike_fit.png')
        photo = tk.PhotoImage(file = fit_photo_path)

        # display tittle signup
        signup_text = ctk.CTkLabel(
            window,
            text="Sign Up",
            font=("Arial", 35, "bold"),
            fg_color="transparent",
            text_color="black"
        )
        
        #signup text placement
        signup_text.place(
                        relx=0.5, 
                        rely=0.2, 
                        anchor = "center"
                        ) 
        
        #signup box size
        signup_box = tk.Frame(
            window,
            width = 600,
            height = 506,
            bg = "gray",
            #border
            highlightbackground="black",  
            highlightthickness=0
        )

        #signup box placement
        signup_box.place(
            relx=0.6,
            rely=0.5,
            anchor="center"
        )
        signup_box.pack_propagate(False)

        #photo placement
        self.photo = photo
        fit_photo = tk.Label(
            window,
            image=self.photo,
        )
        fit_photo.place(relx=0.353, rely=0.5, anchor="center")

        #Text box for user input

        #Username
        tk.Label(signup_box, 
                 text="Username                 :", 
                 bg="gray",                  
                 font=("Arial", 12, 'bold'),
                 ).place(relx = 0.02, rely = 0.2)
        
        tk.Entry(signup_box, 
                 width=30, 
                 font=("Arial", 13)
                 ).place(relx = 0.3, rely = 0.2)
        
        #Password
        tk.Label(signup_box, 
                 text="Password                 :", 
                 bg="gray",                  
                 font=("Arial", 12, 'bold')
                 ).place(relx = 0.02, rely = 0.3)
        
        tk.Entry(signup_box, 
                 width=30, 
                 show="*", 
                 font=("Arial", 13)
                 ).place(relx = 0.3, rely = 0.3)
        
        tk.Label(signup_box, 
                 text="Confirm Password :", 
                 bg="gray",                  
                 font=("Arial", 12, 'bold')
                 ).place(relx = 0.02, rely = 0.4)
        
        tk.Entry(signup_box, width=30, 
                 show="*", 
                 font=("Arial", 13)
                 ).place(relx = 0.3, rely = 0.4)
        
        def go_to_login(self):
            tk.messagebox.showinfo("","Sign Up successfully !")
            window.destroy()
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
            command=lambda: (go_to_login(self), ) #add command here !!!
        ).place(relx=0.9, rely=0.9, anchor="se")

        #cancel button
        ctk.CTkButton(
            master=signup_box,
            text="Cancel",
            width=150,              
            height=36,              
            fg_color="transparent",   
            hover_color="#0400e0",
            text_color="white",
            font=("Arial", 11, "bold"),
            command=lambda: () #add command here !!!
        ).place(relx=0.3, rely=0.9, anchor="se")
        window.mainloop()

       

if __name__ == "__main__":
    Signup()




