import customtkinter as ctk
import calendar
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
import PIL 


# ------------------ Set theme style ------------------
ctk.set_appearance_mode("light")          # light / dark / system

# ------------------ Create main window ------------------
app = tk.Tk()
app.title("FitQuest")
app.geometry("500x550")

icon = tk.PhotoImage(file="C:\\Users\\leong\\Desktop\\assignment\\py-assg-dft1s2\\resourse\\logo.ico")
app.iconphoto(True, icon)

# ------------------ Get current year and month ------------------
current_year = datetime.now().year
current_month = datetime.now().month

# ------------------ Click a day (button) function ------------------
def day_clicked(day):
    if day != 0:
        activity = alreadyfit.get(f"{current_month}-{day}", "no do any sports")
        
        # Create a custom popup
        popup = tk.Toplevel(app)
        popup.title(f"{current_year}-{current_month}-{day}")
        popup.geometry("300x150")
        
        label = tk.Label(popup, 
                         text=f"You clicked: {current_year}-{current_month}-{day}\n\n{activity}",
                         font=("Arial", 14),
                         justify="center",  # center multiple lines
                         anchor="center")
        label.pack(expand=True)
        
        # Confirm button
        btn = tk.Button(popup, text="OK", command=popup.destroy)
        btn.pack(pady=10)

# ------------------ Update and draw calendar ------------------
def update_calendar():
    """
    Clear old widgets and redraw the calendar whenever the month changes
    """
    # Clear old day widgets
    for widget in frame_days.winfo_children():
        widget.destroy()

    # Update top label (e.g., "November 2025")
    label_month.configure(text=f"{calendar.month_name[current_month]} {current_year}")

    # Get month data (2D array, each week is a row)
    month_data = calendar.monthcalendar(current_year, current_month)

    # Weekday header
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day_name in enumerate(weekdays):
        lbl = ctk.CTkLabel(frame_days, text=day_name, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=i, padx=5, pady=5)

    # Create day buttons
    for row_idx, week in enumerate(month_data):
        for col_idx, day in enumerate(week):

            if day == 0:
                # Empty cell
                lbl = ctk.CTkLabel(frame_days, text="", width=40)
                lbl.grid(row=row_idx+1, column=col_idx, padx=5, pady=5)
            else:
                # Get activity
                activity = alreadyfit.get(f"{current_month}-{day}", "")

                # Button text, show day + activity on separate lines
                btn_text = f"{day}\n\n{activity}" if activity else f"{day}"

                btn = ctk.CTkButton(
                    frame_days,
                    border_color="#FE0161",
                    border_width=2,
                    fg_color="#FFFFFF",
                    text_color="#FE0161",
                    hover_color="#FFB6C1",
                    text=btn_text,
                    width=100,
                    height=100,
                    font=("Arial", 16,"bold"),
                    anchor="n",
                    command=lambda d=day: day_clicked(d)
                )
                btn.grid(row=row_idx+1, column=col_idx, padx=5, pady=5)

# ------------------ Previous / Next month buttons ------------------
def prev_month():
    """
    Switch to previous month.
    If current month is January, go to December of previous year
    """
    global current_month, current_year
    current_month -= 1
    if current_month == 0:
        current_month = 12
        current_year -= 1
    update_calendar()  # Refresh display


def next_month():
    """
    Switch to next month.
    If current month is December, go to January of next year
    """
    global current_month, current_year
    current_month += 1
    if current_month == 13:
        current_month = 1
        current_year += 1
    update_calendar()  # Refresh display

# ------------------ Top frame for month switch ------------------
frame_top = ctk.CTkFrame(app)
frame_top.pack(pady=15)

# Previous month button
btn_prev = ctk.CTkButton(frame_top, 
                         border_color="#FE0161",
                         border_width=2,
                         fg_color ="#FFFFFF",
                         text_color="#FE0161",
                         hover_color="#FFB6C1",
                         text="<", 
                         width=50, 
                         command=prev_month
                         )
btn_prev.grid(row=0, column=0, padx=10)

# Current month label
label_month = ctk.CTkLabel(frame_top, text="", font=("Arial", 24, "bold"))
label_month.grid(row=0, column=1, padx=10)

# Next month button
btn_next = ctk.CTkButton(frame_top, 
                         border_color="#FE0161",
                         border_width=2,
                         fg_color ="#FFFFFF",
                         text_color="#FE0161",
                         hover_color="#FFB6C1",
                         text=">", 
                         width=50, 
                         command=next_month)
btn_next.grid(row=0, column=2, padx=10)

# ------------------ Calendar frame ------------------
frame_days = ctk.CTkFrame(app)
frame_days.pack(pady=10)

# Generate calendar for the first time
update_calendar()

# ------------------ Main loop ------------------
app.mainloop()
