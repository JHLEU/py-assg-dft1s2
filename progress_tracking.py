import customtkinter as ctk
import calendar
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
import os

# ------------------ Set theme style ------------------
ctk.set_appearance_mode("light")  # light / dark / system

# ------------------ Create main window ------------------
app = tk.Tk()
app.title("FitQuest")
app.geometry("700x750")

icon_path = os.path.join(os.path.dirname(__file__), 'resource', 'fitness.png')
icon = tk.PhotoImage(file = icon_path)
app.config(background="#FFFFFF")
app.iconphoto(True,icon)



label_title = ctk.CTkLabel(app, text="CALENDAR", font=("Arial", 30, "bold"))
label_title.pack(pady=10)


# ------------------ Current year and month ------------------
current_year = datetime.now().year
current_month = datetime.now().month

alreadyfit = {
    '12-1': 'jianshen',
    '12-3': '不知道',
    '12-5': '不想动',
    '12-7': '放弃中',
    '12-9': '放弃吧'
}

# ------------------ Click a day (calendar) ------------------
def day_clicked(day):
    if day != 0:
        activity = alreadyfit.get(f"{current_month}-{day}", "no do any sports")
        popup = tk.Toplevel(app)
        popup.geometry("300x150")
        label = tk.Label(popup,
                         text=f"you click: {current_year}-{current_month}-{day}\n\n{activity}",
                         font=("Arial", 14),
                         justify="center",
                         anchor="center")
        label.pack(expand=True)
        btn = tk.Button(popup, text="comfirm", command=popup.destroy)
        btn.pack(pady=10)

# ------------------ Update and draw calendar ------------------
def update_calendar():
    for widget in frame_days.winfo_children():
        widget.destroy()

    label_month.configure(text=f"{calendar.month_name[current_month]} {current_year}")
    month_data = calendar.monthcalendar(current_year, current_month)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day_name in enumerate(weekdays):
        lbl = ctk.CTkLabel(frame_days, text=day_name, font=("Arial", 14, "bold"))
        lbl.grid(row=0, column=i, padx=5, pady=5)

    for row_idx, week in enumerate(month_data):
        for col_idx, day in enumerate(week):
            if day == 0:
                lbl = ctk.CTkLabel(frame_days, text="", width=40)
                lbl.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)
            else:
                activity = alreadyfit.get(f"{current_month}-{day}", "")
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

# ------------------ Previous / Next month buttons ------------------
def prev_month():
    global current_month, current_year
    current_month -= 1
    if current_month == 0:
        current_month = 12
        current_year -= 1
    update_calendar()

def next_month():
    global current_month, current_year
    current_month += 1
    if current_month == 13:
        current_month = 1
        current_year += 1
    update_calendar()

# ------------------ Top frame for month switch ------------------
frame_top = ctk.CTkFrame(app)
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

# ------------------ Calendar frame ------------------
frame_days = ctk.CTkFrame(app)
frame_days.pack(pady=10)

update_calendar()

# ------------------ Weekly progress tracking ------------------
today = datetime.now()
today_weekday = today.strftime("%a")  # Mon, Tue...

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
today_index = weekdays.index(today_weekday)

weekly_tasks = {
    "Mon": "",
    "Tue": "",
    "Wed": "",
    "Thu": "",
    "Fri": "",
    "Sat": "",
    "Sun": "",
}

sports_list = [
    "Push-up",
    "Sit-up",
    "Squat",
    "Plank",
    "Pull-up",
    "Lunge"
]

def week_day_clicked(day_name):
    popup = ctk.CTkToplevel(app)
    popup.title(f"{day_name} Activity")
    popup.geometry("300x200")

    lbl = ctk.CTkLabel(popup, text=f"Select activity for {day_name}", font=("Arial", 14))
    lbl.pack(pady=10)

    selected_sport = tk.StringVar(value=weekly_tasks.get(day_name, "Rest"))

    option_menu = ctk.CTkOptionMenu(
        popup,
        values=sports_list,
        variable=selected_sport
    )
    option_menu.pack(pady=10)

    def save_task():
        weekly_tasks[day_name] = selected_sport.get()
        popup.destroy()
        draw_week_progress()   

    btn_save = ctk.CTkButton(popup, text="Save", command=save_task)
    btn_save.pack(pady=10)


def draw_week_progress():
    for widget in frame_week.winfo_children():
        widget.destroy()

    for idx, day_name in enumerate(weekdays):
        cell_frame = ctk.CTkFrame(frame_week, fg_color="transparent", width=90, height=100)
        cell_frame.grid(row=0, column=idx, padx=5, pady=5)

        # highlight today
        if day_name == today_weekday:
            cell_frame.configure(border_width=2, border_color="#FE0161")

        # check can click or not
        is_past_day = idx < today_index

        btn = ctk.CTkButton(
            cell_frame,
            text=day_name,
            width=80,
            height=40,
            font=("Arial", 14, "bold"),
            state="disabled" if is_past_day else "normal",
            command=lambda d=day_name: week_day_clicked(d)
        )
        btn.pack(pady=(5, 2))

        lbl_task = ctk.CTkLabel(
            cell_frame,
            text=weekly_tasks.get(day_name, ""),
            font=("Arial", 12)
        )
        lbl_task.pack()

# ------------------ Title ------------------
label_progress_title = ctk.CTkLabel(app, text="Progress Tracking", font=("Arial", 20, "bold"))
label_progress_title.pack(pady=10)

# ------------------ Weekly frame ------------------
frame_week = ctk.CTkFrame(app)
frame_week.pack(pady=10)

draw_week_progress()


# ------------------ Main loop ------------------
app.mainloop()
