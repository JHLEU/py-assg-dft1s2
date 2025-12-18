import tkinter as tk

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from mainpage import Mainpage
from Survey import PinkThemedFitnessQuestionn

class HealthReport:

    def __init__(self, root):
        self.root = root
        self.root.title("Health Report")
        self.root.state("zoomed")
        self.root.configure(bg="#F5F6FA")

        # =========================
        # Exercise Data
        # =========================
        self.exercise_data = {
            "Push-up Program": 7,
            "Sit-up Challenge": 5,
            "Squat Mastery": 8,
            "Plank Progression": 7.5,
            "Pull-up Training": 12,
            "Lunge Program": 7
        }
        self.exercise_vars = {}

        # =========================
        # Fonts
        # =========================
        self.title_font = ("Segoe UI Semibold", 16)
        self.label_font = ("Segoe UI", 12)
        self.bold_font = ("Segoe UI", 14)

        # =========================
        # Scrollable Layout
        # =========================
        self.canvas = tk.Canvas(root, bg="#F5F6FA", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#F5F6FA")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # =========================
        # Build UI
        # =========================
        self.build_weight_card()
        self.build_bmi_card()
        self.build_exercise_card()
        self.build_summary_card()
        self.build_update_button()

        self.update_values()
       
    # ==================================================
    # UI Helpers
    # ==================================================
    def card(self, master):
        return tk.Frame(master, bg="white", bd=1, relief="solid", padx=15, pady=15)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ==================================================
    # Cards
    # ==================================================
    def build_weight_card(self):
        card = self.card(self.scrollable_frame)
        card.pack(padx=15, pady=10, fill="both")

        tk.Label(card, text="Weight", font=self.title_font, bg="white").pack(anchor="w")

        self.weight_var = tk.StringVar(value="0")
        self.height_var = tk.StringVar(value="0")

        tk.Label(card, text="Current Weight (kg)", font=self.label_font, bg="white").pack(anchor="w")
        tk.Entry(card, textvariable=self.weight_var, font=self.label_font).pack()

        tk.Label(card, text="Height (cm)", font=self.label_font, bg="white", pady=5).pack(anchor="w")
        tk.Entry(card, textvariable=self.height_var, font=self.label_font).pack()

    def build_bmi_card(self):
        card = self.card(self.scrollable_frame)
        card.pack(padx=15, pady=10, fill="both")

        tk.Label(card, text="BMI", font=self.title_font, bg="white").pack(anchor="w")

        self.bmi_label = tk.Label(card, text="0.0", font=self.bold_font, bg="white")
        self.bmi_label.pack()

        self.bmi_bar_container = tk.Frame(card, bg="white")
        self.bmi_bar_container.pack(pady=10)

    def build_exercise_card(self):
        card = self.card(self.scrollable_frame)
        card.pack(padx=15, pady=10, fill="both")

        tk.Label(card, text="Exercise & Calories", font=self.title_font, bg="white").pack(anchor="w")

        for name in self.exercise_data:
            var = tk.BooleanVar()
            self.exercise_vars[name] = var

            tk.Checkbutton(
                card,
                text=f"{name} ({self.exercise_data[name]} kcal/min)",
                variable=var,
                bg="white",
                font=self.label_font
            ).pack(anchor="w")

        tk.Label(
            card,
            text="Exercise Duration (minutes)",
            font=self.label_font,
            bg="white",
            pady=5
        ).pack(anchor="w")

        self.duration_var = tk.StringVar(value="0")
        tk.Entry(card, textvariable=self.duration_var, font=self.label_font).pack()

        self.calories_label = tk.Label(
            card,
            text="Total Calories Burned: 0 kcal",
            font=self.bold_font,
            bg="white"
        )
        self.calories_label.pack(anchor="w", pady=5)

    def build_summary_card(self):
        card = self.card(self.scrollable_frame)
        card.pack(padx=15, pady=10, fill="both")

        tk.Label(card, text="Summary", font=self.title_font, bg="white").pack(anchor="w")
        self.summary_label = tk.Label(card, text="", font=self.label_font, bg="white", justify="left")
        self.summary_label.pack(anchor="w")

    def show_mainpage(self):
        self.root.destroy()              
        new_window = tk.Tk()              
        PinkThemedFitnessQuestionn(new_window)
        new_window.mainloop()


    def build_update_button(self):
        card = self.card(self.scrollable_frame)
        card.pack(padx=20, pady=15, fill="x")
        
        tk.Button(
            card,
            text="Calculate",
            command=self.update_values,
            bg="#0066FF",
            fg="white",
            activebackground="#0050D4",
            font=("Segoe UI", 12),
            bd=0,
            padx=350,
            pady=10
        ).pack( side="left")

        tk.Button(
            card,
            text="Exit",
            command=self.show_mainpage,
            bg="#0066FF",
            fg="white",
            activebackground="#0050D4",
            font=("Segoe UI", 12),
            bd=0,
            padx=330,
            pady=10
        ).pack(side ="left" , padx = 10)
        
    # ==================================================
    # Logic
    # ==================================================
    def update_values(self):
        weight = float(self.weight_var.get())
        height = float(self.height_var.get())

        # ---------- BMI ----------
        bmi = 0
        if height > 0:
            bmi = weight / ((height / 100) ** 2)

        self.bmi_label.config(text=f"{bmi:.1f}")

        for widget in self.bmi_bar_container.winfo_children():
            widget.destroy()

        fig = self.create_bmi_bar(bmi)
        canvas = FigureCanvasTkAgg(fig, master=self.bmi_bar_container)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # ---------- Exercise ----------
        duration = float(self.duration_var.get())
        total_rate = 0
        selected = []

        for name, var in self.exercise_vars.items():
            if var.get():
                selected.append(name)
                total_rate += self.exercise_data[name]

        total_calories = duration * total_rate
        self.calories_label.config(text=f"Total Calories Burned: {total_calories:.0f} kcal")

        # ---------- Summary ----------
        if selected and duration > 0:
            summary = (
                f"Weight: {weight} kg\n"
                f"Height: {height} cm\n"
                f"BMI: {bmi:.1f}\n\n"
                f"Selected exercises: {', '.join(selected)}\n"
                f"Calories per minute: {total_rate} kcal\n"
                f"Duration: {duration:.0f} minutes\n"
                f"Total burned: {total_calories:.0f} kcal"
            )
        else:
            summary = (
                f"Weight: {weight} kg\n"
                f"Height: {height} cm\n"
                f"BMI: {bmi:.1f}\n\n"
                f"No exercise selected."
            )

        self.summary_label.config(text=summary)

    def create_bmi_bar(self, bmi):
        colors = ['#3457D5', '#00B2B2', '#00D27F', '#FFB340', '#FF5A5A']
        bmi_range = [15, 16, 18.5, 25, 30, 40]

        fig, ax = plt.subplots(figsize=(5, 1))

        for i, color in enumerate(colors):
            ax.barh(0, bmi_range[i + 1] - bmi_range[i], left=bmi_range[i], color=color)

        bmi = max(15, min(bmi, 40))
        ax.axvline(bmi, color="black", linewidth=3)
        ax.set_xlim(15, 40)
        ax.axis("off")

        return fig
    
    

# ==================================================
# Run App
# ==================================================

root = tk.Tk()
app = HealthReport(root)
root.mainloop()
