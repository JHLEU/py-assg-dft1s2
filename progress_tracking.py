import customtkinter as ctk
import calendar
from datetime import datetime
import tkinter as tk
import os

class ProgressTrackingApp:
    def __init__(self):
        # ------------------ Window Setup ------------------
        self.root = tk.Tk()
        self.root.state("zoomed")
        self.root.title("FitQuest - Calendar")
        self.root.attributes('-topmost', True)
        self.root.lift()
        self.root.focus_force()

        # ------------------ Icon ------------------
        self._set_icon()

        # ------------------ Data ------------------
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.alreadyfit = {
            '12-1': 'Push-up',
            '12-2': 'Sit-up',
            '12-3': 'Squat',
            '12-4': 'Plank',
            '12-5': 'Pull-up',
            '12-6': 'Lunge',
            '12-7': '',
            '12-8': 'Push-up',
            '12-9': 'Sit-up',
            '12-10': 'Squat',
            '12-11': 'Plank',
            '12-12': 'Pull-up',
            '12-13': 'Lunge',
        }   

        self.weekly_tasks = {
            "Mon": "",
            "Tue": "",
            "Wed": "",
            "Thu": "",
            "Fri": "",
            "Sat": "",
            "Sun": "",
        }

        self.sports_list = [
            "Push-up",
            "Sit-up",
            "Squat",
            "Plank",
            "Pull-up",
            "Lunge"
        ]

        # ------------------ Title ------------------
        label_title = tk.Label(self.root, text="CALENDAR", font=("Arial", 20, "bold"))
        label_title.pack(pady=0)

        # ------------------ Month Switch Frame ------------------
        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack(pady=0)

        self.btn_prev = tk.Button(self.frame_top,
                                  text="<",
                                  bg="white",
                                  fg="#FE0161",
                                  font=("Arial", 14, "bold"),
                                  width=5,
                                  borderwidth=2,
                                  relief="solid",
                                  command=self.prev_month)
        self.btn_prev.grid(row=0, column=0, padx=10)

        self.label_month = tk.Label(self.frame_top, 
                                    text="", 
                                    font=("Arial", 24, "bold"))
        self.label_month.grid(row=0, column=1, padx=10)

        self.btn_next = tk.Button(self.frame_top,
                                  text=">",
                                  bg="white",
                                  fg="#FE0161",
                                  font=("Arial", 14, "bold"),
                                  width=5,
                                  borderwidth=2,
                                  relief="solid",
                                  command=self.next_month)
        self.btn_next.grid(row=0, column=2, padx=10)

        # ------------------ Calendar Frame ------------------
        self.frame_days = tk.Frame(self.root)
        self.frame_days.pack(pady=0)

        self.update_calendar()

        # ------------------ Weekly Progress ------------------
        label_progress_title = tk.Label(self.root, text="Progress Tracking", font=("Arial", 20, "bold"))
        label_progress_title.pack(pady=10)

        self.frame_week = tk.Frame(self.root)
        self.frame_week.pack(pady=0)

        self.draw_week_progress()

        # ------------------ Mainloop ------------------
        self.root.mainloop()

    def _set_icon(self):
        import os, tkinter as tk
        # Adjust filenames to what you actually have in the project
        base = os.path.dirname(os.path.abspath(__file__))
        png_path = os.path.join(base, "fitness.png")
        ico_path = os.path.join(base, "fitness.ico")
        try:
            if os.path.exists(png_path):
                # IMPORTANT: bind image to the same root and keep a reference
                self._icon_img = tk.PhotoImage(file=png_path, master=self.root)
                self.root.iconphoto(True, self._icon_img)
                return
        except Exception:
            pass
        # Fallback for Windows .ico
        try:
            if os.path.exists(ico_path):
                self.root.iconbitmap(default=ico_path)
        except Exception:
            pass

    # ------------------ Calendar Methods ------------------
    def update_calendar(self):
        """
        function for update_calendar
        """
        for widget in self.frame_days.winfo_children():
            widget.destroy()

        self.label_month.configure(text=f"{calendar.month_name[self.current_month]} {self.current_year}") # Update month label

        month_data = calendar.monthcalendar(self.current_year, self.current_month) # Get calendar data
       
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for i, week_name in enumerate(weekdays):
            lbl = tk.Label(self.frame_days, 
                               text=week_name, 
                               font=("Arial", 14, "bold"))
            lbl.grid(row=0, column=i, padx=5, pady=5)

        # 日期按钮
        for row_idx, week in enumerate(month_data):
            for col_idx, day in enumerate(week):
                if day == 0:
                    lbl = tk.Label(self.frame_days, text="", width=10)
                    lbl.grid(row=row_idx + 1, column=col_idx, padx=10, pady=5)
                else:
                    key = f"{self.current_month}-{day}"
                    activity = self.alreadyfit.get(key, "")
                    btn_text = f"{day}\n\n{activity}" if activity else f"{day}"
                    btn = tk.Button(self.frame_days,
                                        text=btn_text,
                                        width=10,
                                        height=4,
                                        bg="white",
                                        fg="#FE0161",
                                        font=("Arial", 12, "bold"),
                                        borderwidth=2,
                                        relief="solid",
                                        anchor="n",
                                        command=lambda d=day: self.day_clicked(d))
                    btn.grid(row=row_idx + 1, column=col_idx, padx=10, pady=5)

    def day_clicked(self, day):
        """
        function for day_clicked
        """
        if day == 0:
            return
        key = f"{self.current_month}-{day}"
        activity = self.alreadyfit.get(key, "no do any sports")
        popup = tk.Toplevel(self.root)
        popup.geometry("300x150")
        popup.title("Day Info")
        popup.attributes('-topmost', True)
        label = tk.Label(popup, 
                         text=f"{self.current_year}-{self.current_month}-{day}\n\n{activity}",
                         font=("Arial", 14), justify="center")
        label.pack(expand=True)

        btn = tk.Button(popup, text="Confirm", command=popup.destroy)
        btn.pack(pady=10)

    def prev_month(self):
        """
        Docstring for prev_month
        """
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        """
        Docstring for next_month
        """
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

    # ------------------ Weekly Progress ------------------
    def draw_week_progress(self):
        """
        Docstring for draw_week_progress
        """
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        today_index = weekdays.index(datetime.now().strftime("%a")) # Get today's index

        for widget in self.frame_week.winfo_children():
            widget.destroy()

        for idx, day_name in enumerate(weekdays):
            cell_frame = tk.Frame(self.frame_week, width=90, height=180)
            cell_frame.grid_propagate(False)
            cell_frame.grid(row=0, column=idx, padx=5, pady=5)

            # highlight today in week progress
            if idx == today_index:
                cell_frame.configure(
                    relief="solid",
                    highlightthickness=2,
                    highlightbackground="#FE0161")


            # past day disable button
            is_past_day = idx < today_index
            btn = tk.Button(cell_frame,
                                text=day_name,
                                width=5,
                                height=2,
                                font=("Arial", 14, "bold"),
                                state="disabled" if is_past_day else "normal",
                                command=lambda d=day_name: self.week_day_clicked(d))
            btn.pack(pady=(5, 2))

            lbl_task = tk.Label(cell_frame, text=self.weekly_tasks.get(day_name, ""), font=("Arial", 12))
            lbl_task.pack()

    def week_day_clicked(self, day_name):
        """
        Docstring for week_day_clicked
        """
        popup = tk.Toplevel(self.root)
        popup.title(f"{day_name} Activity")
        popup.geometry("300x200")
        popup.grab_set()
        popup.attributes('-topmost', True)
        popup.lift()
        popup.focus_force()

        lbl = tk.Label(popup, text=f"Select activity for {day_name}", font=("Arial", 14))
        lbl.pack(pady=10)

        selected_sport = tk.StringVar(value=self.weekly_tasks.get(day_name, "Rest"))

        option_menu = tk.OptionMenu(popup, selected_sport, *self.sports_list)
        option_menu.pack(pady=10)

        def save_task():
            """
            Docstring for save_task
            """
            self.weekly_tasks[day_name] = selected_sport.get()
            popup.destroy()
            self.draw_week_progress()

            self.root.after(10, lambda: self.root.state("zoomed"))
            self.draw_week_progress()
        
        popup.protocol("WM_DELETE_WINDOW", save_task)

        btn_save = tk.Button(popup, text="Save", command=save_task)
        btn_save.pack(pady=10)

# ------------------ Run App ------------------
if __name__ == "__main__":
    app = ProgressTrackingApp()
