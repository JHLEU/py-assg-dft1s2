import tkinter as tk

class Login_function:
    def __init__(self):
        window = tk.Tk()
        window.state("zoomed")
        window.title("FitQuest")
        window.attributes('-topmost', True)
        window.lift()
        window.focus_force()
        window.mainloop()
        

if __name__ == "__main__":
    Login_function()




