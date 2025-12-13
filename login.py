import tkinter as tk
import customtkinter as ctk

class Login_function:
    def __init__(self):
        window = tk.Tk()
        window.state("zoomed")
        window.title("FitQuest")
        window.attributes('-topmost', True)
        window.lift()
        window.focus_force()


        tk.Label(text="login", 
                 bg="gray",                  
                 font=("Arial", 12, 'bold'),
                 ).place(relx = 0.02, rely = 0.2)
        
        window.mainloop()
        

if __name__ == "__main__":
    Login_function()




