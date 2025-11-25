from customtkinter import *
from tkinter import *
import os
#widgets = GUI elemnets: buttons, textboxes, images
#window = serves as a container to hold or contain these widgets
def click():
    print("Button clicked!")
#Creating the window
window = Tk()

#Creating a button widget
button = Button(window, text="Next")
button.config(command=click)
button.config(font=('Ink Free',20,'bold'))
button.config(bg='#ff6200')
button.config(fg='#fffb1f')
button.config(activebackground = '#FF0000')
button.config(activeforeground = "#fffb1f")

#photo image
photo = PhotoImage(file = r"C:\\TARUMT\\Assignment\\resourse\\fitness.png")
photo = photo.subsample(3,3) #resize image
#window size
window.geometry("420x420") #width x height 
#window title
window.title("FitQuest ")

#displaying an icon
icon = PhotoImage(file="C:\\TARUMT\\Assignment\\resourse\\logo.png")
window.iconphoto(True, icon)

#background color
window.config(background="white")

# Create a label widget
welcome = Label(window, text = "Welcome to FitQuest!",
                 font=("Arial",40,"bold"),
                 fg="black",
                 bg="white",
                 relief=RAISED,
                 bd=10,
                 padx=20,
                 pady=20,
                 image = photo,
                 compound='left') #compound to place text in relation to image

welcomeNote = Label(window, text = "Please answer the following questions truthfully to get the best results.",
                 font=("Arial",20),
                 fg="black",
                 bg="white",
                 relief=RAISED,
                 bd=10,
                 padx=20,
                 pady=20)

# Shoving it onto the screen
welcome.pack(expand=True)
welcome.place(x=400, y=100)
welcomeNote.place(x=310, y=500)
button.place(x=1137, y=600)


#place window on computer screen and listen for events
window.mainloop() 
