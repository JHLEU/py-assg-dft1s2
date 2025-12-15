import os
import customtkinter as ctk
import calendar
from datetime import datetime
from tkinter import messagebox
import tkinter as tk

# ------------------ initialize window setup ------------------
window = tk.Tk()
window.title("FitQuest")
window.state("zoomed")  # Maximize window
window.title("FitQuest - Login")
window.attributes('-topmost', True)
window.lift()
window.focus_force()
ctk.set_appearance_mode("light")  # Or "Dark"/"Light"
ctk.set_default_color_theme("blue")  # Your theme
ctk.set_widget_scaling(1.0)  # Base scaling; adjust if needed (e.g., 1.2 for higher DPI)
ctk.set_window_scaling(1.0)  # Window scaling

#------------------ Load and set icon ------------------

icon_path = os.path.join(os.path.dirname(__file__), 'resource', 'fitness.png')
icon = tk.PhotoImage(file = icon_path)
window.config(background="#FFFFFF")
window.iconphoto(True,icon)


# ------------------ get current year and month ------------------
current_year = datetime.now().year
current_month = datetime.now().month

# ------------------ Sample data for days with activities ------------------
alreadyfit = {
    '12-1': 'jianshen',
    '12-3': '不知道',
    '12-5': '不想动',
    '12-7': '放弃中',
    '12-9': '放弃吧'
}

# ------------------ Click day function ------------------
def day_clicked(day):
    """Handle day button click event."""

    # if the day does not have activity, do nothing
    if day != 0:
        
        activity = alreadyfit.get(f"{current_month}-{day}", "no do any sports") # get activity if exists
        
        # create popup window
        popup = tk.Toplevel(window) 
        popup.geometry("300x150") 
        popup.attributes('-topmost', True)
        label = tk.Label(popup,
                         text=f"你点击了：{current_year}-{current_month}-{day}\n\n{activity}",
                         font=("Arial", 14),
                         justify="center",
                         anchor="center")
        label.pack(expand=True)
        btn = tk.Button(popup, text="确定", command=popup.destroy)
        btn.pack(pady=10)

# ------------------ Update and draw calendar function ------------------
def update_calendar():
    """Update the calendar display bases on variable month and year."""
    for widget in frame_days.winfo_children():
        widget.destroy()

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]   
    calendar_data = calendar.monthcalendar(current_year, current_month) # get month data bases on year and month
    
    # ------------------------------- weekday labels -------------------------------
    for i, day_name in enumerate(weekdays):
        lbl = ctk.CTkLabel(frame_days, text=day_name, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=i, padx=5, pady=5)

    # ------------------------------- Display day buttons -------------------------------
    for row_idx, week in enumerate(calendar_data):
        for col_idx, day in enumerate(week):
            if day == 0: # if day is 0, create empty label
                lbl = ctk.CTkLabel(frame_days, text="", width=40)
                lbl.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

            else: # if day is not 0, create button with day number and activity
                
                activity = alreadyfit.get(f"{current_month}-{day}", "") # get activity if exists

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
                    font=("Arial", 16, "bold"),
                    anchor="n",
                    command=lambda d=day: day_clicked(d)
                )
                btn.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

# ------------------ Previous / Next month buttons command ------------------
def prev_month():
    """Go to previous month."""
    global current_month, current_year
    current_month -= 1
    if current_month == 0:
        current_month = 12
        current_year -= 1
    update_calendar()

def next_month():
    """Go to next month."""
    global current_month, current_year
    current_month += 1
    if current_month == 13:
        current_month = 1
        current_year += 1
    update_calendar()


# ------------------ Weekly progress tracking ------------------
today = datetime.now()
today_weekday = today.strftime("%a")  # from datetime change to weekday string
today_date = today.day # get today's date

weekly_tasks = {
    "Mon": "Push-up",
    "Tue": "Run",
    "Wed": "Rest",
    "Thu": "Yoga",
    "Fri": "Leg Day",
    "Sat": "Swim",
    "Sun": "Rest",
}

def week_day_clicked(day_name):
    task = weekly_tasks.get(day_name, "No task")
    messagebox.showinfo("任务", f"任务是：{task}")

def draw_week_progress():
    """Draw week progress"""
    for widget in frame_week.winfo_children():
        widget.destroy()

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for idx, day_name in enumerate(weekdays):
        cell_frame = ctk.CTkFrame(frame_week, fg_color="transparent", width=90, height=100)
        cell_frame.grid(row=0, column=idx, padx=5, pady=5)

        if day_name == today_weekday:
            cell_frame.configure(border_width=2, border_color="#FE0161")

        btn = ctk.CTkButton(
            cell_frame,
            text=day_name,
            width=80,
            height=40,
            font=("Arial", 14, "bold"),
            command=lambda d=day_name: week_day_clicked(d)
        )
        btn.pack(pady=(5, 2))

        lbl_task = ctk.CTkLabel(cell_frame, text=weekly_tasks.get(day_name, ""), font=("Arial", 12))
        lbl_task.pack()

# ------------------ Title ------------------
label_title = ctk.CTkLabel(window, text="Progress Tracking", font=("Arial", 20, "bold"))
label_title.pack(pady=10)

# =================================================== Top frame  ===========================================================

# ------------------ Top frame for month switch ------------------
frame_top = ctk.CTkFrame(window)
frame_top.pack(pady=15)

btn_prev = ctk.CTkButton(frame_top,
                         border_color="#FE0161",
                         border_width=2,
                         fg_color="#FFFFFF",
                         text_color="#FE0161",
                         hover_color="#FFB6C1",
                         text="<",
                         width=50,
                         command=prev_month)
btn_prev.grid(row=0, column=0, padx=10)

label_month = ctk.CTkLabel(frame_top, text="", font=("Arial", 24, "bold"))
label_month.configure(text=f"{calendar.month_name[current_month]} {current_year}")  # update month label
label_month.grid(row=0, column=1, padx=10)

btn_next = ctk.CTkButton(frame_top,
                         border_color="#FE0161",
                         border_width=2,
                         fg_color="#FFFFFF",
                         text_color="#FE0161",
                         hover_color="#FFB6C1",
                         text=">",
                         width=50,
                         command=next_month)
btn_next.grid(row=0, column=2, padx=10)

# ==================================================== centrel frame =================================================================

# ------------------ Calendar frame ------------------
frame_days = ctk.CTkFrame(window)
frame_days.pack(pady=10)

update_calendar()
# ================================================= lower frame ====================================================================
# ------------------ Weekly progress frame ------------------
frame_week = ctk.CTkFrame(window)
frame_week.pack(pady=10)

draw_week_progress()

# ================= Main loop ====================
window.mainloop()
